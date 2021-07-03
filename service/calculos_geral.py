from datetime import datetime, timedelta

import pandas as pd

from service.historico import HistoricoService
from utils.clever_generics import CleverGenerics

class CalculosGeral:

    def __init__(self) -> None:
        self.historico_service = HistoricoService()
        self.clever_generics = CleverGenerics()
        self.key_carteria = 'Carteira'

    def rd_default(self, ativos, from_date, to_date):
        historico = self.get_historico(
            ativos=ativos, from_date=from_date, to_date=to_date)

        desvio_padrao = self.calcula_desvio_padrao(historico=historico)

        desvio_normalizado = desvio_padrao.apply(self.normalize)
        soma_desvio_normalizado = self.get_soma_desvio(desvio_normalizado)

        rd = dict()
        for chave, item in desvio_normalizado.iteritems():
            rd[chave] = self.calcula_rd(item[0], soma_desvio_normalizado)

        return rd

    def get_historico(self, ativos, from_date, to_date) -> dict:
        historico = dict()
        for ativo in ativos:
            historico_ativo = self.historico_service.passado(
                ativo, to_date=to_date, from_date=from_date, model_to_json=True)
            if len(historico_ativo['historico']) > 0:
                historico[ativo] = historico_ativo
            else:
                historico[ativo] = {'historico': [{'variacao': '0.0'}]}

        return historico

    def calcula_desvio_padrao(self, historico: dict):
        historico_variacao = dict()
        for ativo in historico:
            variacao = []
            for item in historico[ativo]['historico']:
                variacao.append(float(item['variacao']))
            historico_variacao[ativo] = variacao

        self.iguala_tamanho_listas_historico(historico_variacao)

        df = pd.DataFrame(historico_variacao)
        dp = df.std()
        return pd.DataFrame(dp).transpose()

    def iguala_tamanho_listas_historico(self, historico_variacao: dict):
        maior = 0
        for chave in historico_variacao:
            aux = len(historico_variacao[chave])
            if (aux > maior):
                maior = aux

        for chave in historico_variacao:
            if len(historico_variacao[chave]) < maior:
                for i in range(maior - len(historico_variacao[chave])):
                    historico_variacao[chave].append(0.0)

    def get_soma_desvio(self, desvio):
        soma_desvio_series = desvio.sum(axis=0)
        soma_desvio = soma_desvio_series.values
        return soma_desvio[0]

    def calcula_rd(self, desvio_normalizado, soma_desvio_normalizado):
        return (desvio_normalizado / soma_desvio_normalizado)

    def normalize(self, x):
        if x.item() == 0.0:
            return 0.0
        return 1/x

    def get_from_and_to_date(self):
        from_date = self.clever_generics.data_formato_banco(
            (datetime.today() + timedelta(days=-365*2)))
        to_date = self.clever_generics.data_formato_banco(datetime.today())

        return from_date, to_date