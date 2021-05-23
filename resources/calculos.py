from flask_restplus import Resource
import pandas

from core.server import server
from service.ativos import Ativos
from service.calculos import Calculos as CalculosService
from utils.clever_generics import CleverGenerics

api = server.api
calculosService = CalculosService()
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
        
        ativosParaCalculo = []
        perfil = request['perfil']
        if perfil == '1':
            pesquisa = ativosService.pesquisa(ativo=conservador)
            ativosParaCalculo.append(pesquisa.symbol)
        elif perfil == '3':
            pesquisa = ativosService.pesquisa(ativo=agressivo)
            ativosParaCalculo.append(pesquisa.symbol)
        else:
            for ativo in moderado:
                pesquisa = ativosService.pesquisa(ativo=ativo)
                ativosParaCalculo.append(pesquisa.symbol)


        ativos = request['ativos']
        for ativo in ativos:
            ativosParaCalculo.append(ativo)

        return calculosService.rd(ativos=ativosParaCalculo)
        