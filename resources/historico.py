from flask_restplus import Resource

from service.historico import HistoricoService
from utils.clever_generics import CleverGenerics
from core.server import server

app = server.app
api = server.api

@api.route('/historico')
class Historico(Resource):
    @staticmethod
    def get():
        response = api.payload
        
        if 'ativo' not in response:
            return CleverGenerics().gera_resposta(CleverGenerics().err01, 'ativo')
            
        ativo = response['ativo']

        return HistoricoService().recente(ativo)