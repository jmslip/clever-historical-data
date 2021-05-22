from datetime import timedelta, datetime
import pandas as pd
import numpy as np

from service.historico import HistoricoService
from utils.clever_generics import CleverGenerics

class Calculos:
    def __init__(self) -> None:
        self.historicoService = HistoricoService()
        self.clever_generics = CleverGenerics()

    def rd(self, ativos):
        from_date = self.clever_generics.data_formato_br((datetime.today() + timedelta(days=-365*2)))
        to_date = self.clever_generics.data_formato_br(datetime.today())
        historico = dict()
        for ativo in ativos:
            historico[ativo] = self.historicoService.passado(ativo, to_date=to_date, from_date=from_date, model_to_json=True)
        
        desvioPadrao = self.calculaDesvioPadrao(historico=historico)
        
        desvioNormalizado = desvioPadrao.apply(self.normalize)
        somaDesvioNormalizado = self.getSomaDesvio(desvioNormalizado)

        rd = dict()
        for chave, item in desvioNormalizado.iteritems():
            rd[chave] = self.calculaRd(item[0], somaDesvioNormalizado)
        
        return rd

    def calculaDesvioPadrao(self, historico: dict):
        historicoVariacao = dict()
        for ativo in historico:
            variacao = []
            for item in historico[ativo]['historico']:
                variacao.append(float(item['variacao']))
            historicoVariacao[ativo] = variacao

        df = pd.DataFrame(historicoVariacao)
        dp = df.std()
        return  pd.DataFrame(dp).transpose()

    def normalize(self, x):
        return 1/x

    def getSomaDesvio(self, desvio):
        somaDesvioSeries = desvio.sum(axis=1)
        somaDesvio = somaDesvioSeries.values
        return somaDesvio[0]

    def calculaRd(self, desvioNormalizado, somaDesvioNormalizado):
        return (desvioNormalizado / somaDesvioNormalizado)