from datetime import timedelta, datetime

from service.historico import HistoricoService

class Calculos:
    def __init__(self) -> None:
        self.historicoService = HistoricoService()
    
    def covariancia(self, ativos):
        historico = 0
        to_date = (datetime.today() + timedelta(days=-365*2))
        from_date = datetime.today

        for ativo in ativos:
            historico = self.historicoService.passado(ativo, to_date=to_date, from_date=from_date)

