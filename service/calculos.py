from datetime import timedelta, datetime
from pandas import DataFrame

from service.historico import HistoricoService
from utils.clever_generics import CleverGenerics

class Calculos:
    def __init__(self) -> None:
        self.historicoService = HistoricoService()
        self.clever_generics = CleverGenerics()
    
    def covariancia(self, ativos):
        historico = 0
        from_date = self.clever_generics.data_formato_br((datetime.today() + timedelta(days=-365*2)))
        to_date = self.clever_generics.data_formato_br(datetime.today())

        for ativo in ativos:
            historico = self.historicoService.passado(ativo, to_date=to_date, from_date=from_date, model_to_json=True)
            
        
            df = DataFrame(historico)
            print(df)

