from datetime import datetime
from json import loads

from service.ativos import Ativos
from core.models import HistoricalData
from core.models import Ativo as AtivoModel
from utils.clever_generics import CleverGenerics


class HistoricoService:

    def __init__(self) -> None:
        self.pais = 'Brazil'
        self.str_yesterday = 'yesterday'
        self.str_today = 'today'
        self.str_var = 'var'
        self.str_close = 'Close'
        self.str_simbolo = 'simbolo'
        self.clever_generics = CleverGenerics()

    def recente_com_var(self, dados, ativo):
        historico = dict()
        var = dict()

        yesterday_key = today_key = ''
        for key, value in dados.items():
            if self.str_yesterday in var:
                today_key = key
                var[self.str_today] = value[self.str_close]
            else:
                yesterday_key = key
                var[self.str_yesterday] = value[self.str_close]

        dados[today_key][self.str_var] = self.calc_var(ultimo=var[self.str_today], ultimo_ontem=var[self.str_yesterday])
        dados.pop(yesterday_key)

        historico[ativo] = dados
        
        return historico


    def recente(self, ativo, to_json=True):
        pesquisa = Ativos().pesquisa(ativo)

        historico = 0

        for hist in pesquisa:
            historico = hist.retrieve_recent_data().tail(2)

        if to_json:
            dados = loads(historico.to_json(orient='index', date_format='iso', compression='gzip'))
            return self.recente_com_var(dados=dados, ativo=ativo)

        return historico

    
    def passado(self, ativo, from_date, to_date, to_json=True):
        # pesquisa = Ativos().pesquisa(ativo)

        # historico = 0

        # for hist in pesquisa:
        #     historico = hist.retrieve_historical_data(from_date=from_date, to_date=to_date)

        # if to_json:
        #     return loads(historico.to_json(orient='index', date_format='iso', compression='gzip'))
        ativo = AtivoModel.select().where(AtivoModel.simbolo == ativo).get()
        hist = HistoricalData().select().where(HistoricalData.data_historico >= from_date, 
                                                    HistoricalData.data_historico <= to_date, 
                                                    HistoricalData.ativo == ativo).get()
        
        return self.clever_generics.convert_model_to_json(hist)
        

    
    def calc_var(self, ultimo, ultimo_ontem):
        return round(((ultimo_ontem - ultimo) / ultimo_ontem), 4) * -1
