from flask_restplus import Resource

from service.historico import HistoricoService
from utils.clever_generics import CleverGenerics
from core.server import server

app = server.app
api = server.api
clever_generics = CleverGenerics()

parametros = ['simbolo', 'tipo', 'data_inicio', 'data_fim']
parametros_obrigatorios = ['simbolo']

@api.route('/historico')
class Historico(Resource):
    @staticmethod
    def get():
        response = api.payload
        
        err = clever_generics.valida_parametros_obrigatorios(request=response, parametros=parametros_obrigatorios)

        if err is not None:
            return err

        simbolo = response['simbolo']

        tipo = 'recente'

        if 'tipo' in response:
            tipo = response['tipo']

        if tipo == 'recente':
            return HistoricoService().recente(simbolo)
        elif tipo == 'passado':
            err = clever_generics.valida_parametros_obrigatorios(request=response, parametros=parametros)

            if err is not None:
                return err

            data_inicio = response['data_inicio']
            data_fim = response['data_fim']

            return HistoricoService().passado(ativo=simbolo, from_date=data_inicio, to_date=data_fim)

            # TODO necessário criar estrutura else caso não seja tipo recente ou passado.