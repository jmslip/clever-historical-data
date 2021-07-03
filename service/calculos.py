from datetime import timedelta, datetime
from typing import OrderedDict
import pandas as pd
import numpy as np
import array

from pandas.core.frame import DataFrame

from service.historico import HistoricoService
from utils.clever_generics import CleverGenerics


class Calculos:
    def __init__(self) -> None:
        self.historicoService = HistoricoService()
        self.clever_generics = CleverGenerics()
        self.key_carteria = 'Carteira'

    def rd(self, ativos):
        from_date, to_date = self.get_from_and_to_date()

        return self.rd_default(ativos=ativos, from_date=from_date, to_date=to_date)

    def rd_backtest(self, ativos) -> dict:
        from_date = self.clever_generics.data_formato_banco(
            (datetime.today() + timedelta(days=-365*4)))
        to_date = self.clever_generics.data_formato_banco(
            (datetime.today() + timedelta(days=-365*2)))

        return self.rd_default(ativos=ativos, from_date=from_date, to_date=to_date)

    def calculo_carteira_bt(self, ativos):
        rd = self.rd_backtest(ativos=ativos)
        from_date, to_date = self.get_from_and_to_date()
        historico = self.get_historico(
            ativos=ativos, from_date=from_date, to_date=to_date)

        historico_bt = self.normaliza_historico_backtest(historico=historico)

        carteira_df = self.obtem_carteira_historico(rd=rd, historico=historico_bt)
        indice_ipca = self.indicice_ipca(from_date, to_date)
        periodos = self.obtem_quantidade_periodos(historico=historico)
        indice_perfil = round((indice_ipca + 0.12), 4)
        taxa_equivalente = round(((1 + indice_perfil) ** (1/periodos) - 1), 4)
        backtest = self.obtem_inflacao_meta(periodos=periodos, taxa_equivalente=taxa_equivalente, carteira_df=carteira_df).fillna(0.0)

        return backtest.to_dict()

    def obtem_quantidade_periodos(self, historico: dict) -> int:
        for i in historico:
            return len(historico[i]['historico'])
            


    def obtem_inflacao_meta(self, periodos: int, taxa_equivalente: float, carteira_df: DataFrame) -> DataFrame:
        valores_inflacao_meta = dict()
        valores_inflacao_meta_aux = dict()

        i = 0
        for key, row in carteira_df.iteritems():
            if key == self.key_carteria:
                for data_historico in row.keys():
                    if i == 0:
                        valores_inflacao_meta[data_historico] = 0.0
                        valores_inflacao_meta_aux[i] = 0.0
                        i = i + 1
                    else:
                        valores_inflacao_meta[data_historico] = round(((1 + valores_inflacao_meta_aux[i-1]) * (1+taxa_equivalente) - 1), 4)
                        valores_inflacao_meta_aux[i] = valores_inflacao_meta[data_historico]
                        i = i + 1

        inflacao_meta = dict()
        inflacao_meta['Inflacao_meta'] = valores_inflacao_meta
        df_inflacao_meta = pd.DataFrame.from_dict(inflacao_meta)
        carteira_df['Inflacao_meta'] = df_inflacao_meta
        
        return carteira_df


    def obtem_carteira_historico(self, rd: dict, historico:dict) -> DataFrame:
        carteira_df = pd.DataFrame.from_dict(historico)
        carteira = carteira_df.apply(lambda row: self.calc_carteria(row, rd), axis=1)
        carteira_df[self.key_carteria] = carteira

        return carteira_df


    def calc_carteria(self, row, rd: dict):
        calc = 0
        for ativo in rd:
            calc = calc + row[ativo] * rd[ativo]      
        return round(calc, 4)

    def get_from_and_to_date(self):
        from_date = self.clever_generics.data_formato_banco(
            (datetime.today() + timedelta(days=-365*2)))
        to_date = self.clever_generics.data_formato_banco(datetime.today())

        return from_date, to_date

    def normaliza_historico_backtest(self, historico: dict) -> dict:
        historico_bt = dict()
        list_variacao_bt = list()
        for ativo in historico:
            i = 0
            for item in historico[ativo]['historico']:
                if i == 0:
                    historico_bt[ativo] = dict()
                    historico_bt[ativo][item['data_historico']] = 0.0
                    list_variacao_bt.append(0.0)
                    i = i + 1
                else:
                    valor_calculado = self.calculo_historico_backtest(list_variacao_bt[i-1], item['variacao'])
                    historico_bt[ativo][item['data_historico']] = valor_calculado
                    list_variacao_bt.append(valor_calculado)
                    i = i + 1
        return historico_bt

    def calculo_historico_backtest(self, x, y):
        a = 1 + x
        b = 1 + float(y)

        return a * b - 1

    def rd_default(self, ativos, from_date, to_date):
        historico = self.get_historico(
            ativos=ativos, from_date=from_date, to_date=to_date)

        desvio_padrao = self.calculaDesvioPadrao(historico=historico)

        desvio_normalizado = desvio_padrao.apply(self.normalize)
        soma_desvio_normalizado = self.getSomaDesvio(desvio_normalizado)

        rd = dict()
        for chave, item in desvio_normalizado.iteritems():
            rd[chave] = self.calculaRd(item[0], soma_desvio_normalizado)

        return rd

    def get_historico(self, ativos, from_date, to_date) -> dict:
        historico = dict()
        for ativo in ativos:
            historico_ativo = self.historicoService.passado(
                ativo, to_date=to_date, from_date=from_date, model_to_json=True)
            if len(historico_ativo['historico']) > 0:
                historico[ativo] = historico_ativo
            else:
                historico[ativo] = {'historico': [{'variacao': '0.0'}]}

        return historico

    def calculaDesvioPadrao(self, historico: dict):
        historicoVariacao = dict()
        for ativo in historico:
            variacao = []
            for item in historico[ativo]['historico']:
                variacao.append(float(item['variacao']))
            historicoVariacao[ativo] = variacao

        self.igualaTamanhoListasHistorico(historicoVariacao)

        df = pd.DataFrame(historicoVariacao)
        dp = df.std()
        return pd.DataFrame(dp).transpose()

    def igualaTamanhoListasHistorico(self, historicoVariacao: dict):
        maior = 0
        for chave in historicoVariacao:
            aux = len(historicoVariacao[chave])
            if (aux > maior):
                maior = aux

        for chave in historicoVariacao:
            if len(historicoVariacao[chave]) < maior:
                for i in range(maior - len(historicoVariacao[chave])):
                    historicoVariacao[chave].append(0.0)

    def normalize(self, x):
        if x.item() == 0.0:
            return 0.0
        return 1/x

    def getSomaDesvio(self, desvio):
        somaDesvioSeries = desvio.sum(axis=0)
        somaDesvio = somaDesvioSeries.values
        return somaDesvio[0]

    def calculaRd(self, desvioNormalizado, somaDesvioNormalizado):
        return (desvioNormalizado / somaDesvioNormalizado)

    def indicice_ipca(self, data_inicial: str, data_final: str) -> float:
        data_inicial = self.clever_generics.str_data_formato_br(data_inicial, "%Y-%m-%d")
        data_final = self.clever_generics.str_data_formato_br(data_final, "%Y-%m-%d")

        ## 433 == IPCA
        url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json'
        
        if data_inicial is not None and data_final is not None:
            url = url + '&dataInicial=' + data_inicial + '&dataFinal=' + data_final     

        response = pd.read_json(url)

        acumulado = 1.0
        for key, value in response.values:
            acumulado = acumulado * ((value / 100) + 1)

        return round((((100 * acumulado) - 100) / 100), 4)