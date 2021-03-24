from datetime import datetime
from json import loads

from service.ativos import Ativos
from core.models import HistoricalData
from core.models import Ativo as AtivoModel


class HistoricoService:

    def __init__(self) -> None:
        self.pais = 'Brazil'

    def recente(self, ativo, to_json=True):
        pesquisa = Ativos().pesquisa(ativo)

        historico = 0

        for hist in pesquisa:
            historico = hist.retrieve_recent_data().tail(2)

        if to_json:
            return loads(historico.to_json(orient='index', date_format='iso', compression='gzip'))

        return historico

    
    def passado(self, ativo, from_date, to_date, to_json=True):
        # pesquisa = Ativos().pesquisa(ativo)

        # historico = 0

        # for hist in pesquisa:
        #     historico = hist.retrieve_historical_data(from_date=from_date, to_date=to_date)

        # if to_json:
        #     return loads(historico.to_json(orient='index', date_format='iso', compression='gzip'))
        ativo = AtivoModel.select().where(AtivoModel.simbolo == ativo).get()
        HistoricalData().select().where(HistoricalData.data_historico >= from_date, HistoricalData.data_historico <= to_date, HistoricalData.ativo == ativo).get()
        pass