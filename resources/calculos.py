from flask_restplus import Resource
import pandas

from core.server import server
from service.ativos import Ativos
from service.calculos import Calculos as CalculosService
from service.calculos_backtest import CalculosBackTest as CalculosBTService
from utils.clever_generics import CleverGenerics

api = server.api
calculosService = CalculosService()
calculosBtService = CalculosBTService()
clever_generics = CleverGenerics()
ativosService = Ativos()

parametros_obrigatorios = ['ativos', 'perfil']

conservador = 'B5P211'
agressivo = 'IMAB11'
moderado = [conservador, agressivo]

@api.route('/calculos')
class Calculos(Resource):
    @staticmethod
    def get():
        request = api.payload

        err = clever_generics.valida_parametros_obrigatorios(request=request, parametros=parametros_obrigatorios)

        if err is not None:
            return err
        
        ativos_para_calculo = []
        risco = 0.0
        perfil = request['perfil']
        if perfil == '1':
            pesquisa = ativosService.pesquisa(ativo=conservador)
            ativos_para_calculo.append(pesquisa.symbol)
            risco = 0.02
        elif perfil == '3':
            pesquisa = ativosService.pesquisa(ativo=agressivo)
            ativos_para_calculo.append(pesquisa.symbol)
            risco = 0.06
        else:
            for ativo in moderado:
                pesquisa = ativosService.pesquisa(ativo=ativo)
                ativos_para_calculo.append(pesquisa.symbol)
            risco = 0.04


        ativos = request['ativos']
        for ativo in ativos:
            ativos_para_calculo.append(ativo)

        is_backtest = False;
        if 'backtest' in request:
            is_backtest = request['backtest']

        if is_backtest:
            return calculosBtService.calculo(ativos=ativos_para_calculo, percentual_risco=risco)

        return calculosService.calculo(ativos=ativos_para_calculo)
