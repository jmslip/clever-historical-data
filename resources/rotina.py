from datetime import datetime
from flask_restplus import Resource

from core.server import server
from service.rotinas import Rotina as RotinaService
from utils.clever_generics import CleverGenerics

api = server.api
clever_generics = CleverGenerics()
rotinaService = RotinaService()

parametros_obrigatorios = ['simbolo']

@api.route('/rotina')
class Rotina(Resource):
    @staticmethod
    def get():
        RotinaService().atualiza_historico()
        return {}


@api.route('/rotina/retroativo')
class RotinaRetroativa(Resource):
    @staticmethod
    def get():
        request = None
        if api.payload is not None:
            request = api.payload

        simbolo = None

        if request is not None and 'simbolo' in request:
            simbolo = request['simbolo']
            
        data_historico = rotinaService.get_ultima_data_historico(ativo=simbolo)

        if data_historico is None:
            return clever_generics.gera_resposta(clever_generics.err04)

        data_historico = clever_generics.data_formato_br(data_historico)

        today = clever_generics.data_formato_br(datetime.today())

        if data_historico == today:
            return clever_generics.gera_resposta(mensagem='Nada para atualizar')

        if simbolo is None or not isinstance(simbolo, str):
            sucesso = rotinaService.atualiza_historico_por_data(from_date=data_historico, to_date=today)
        else:
            sucesso = rotinaService.atualiza_historico_por_data(from_date=data_historico, to_date=today, ativo=simbolo)

        if sucesso:
            return clever_generics.gera_resposta(clever_generics.http_response_201)
        else:
            return clever_generics.gera_resposta(clever_generics.err04)