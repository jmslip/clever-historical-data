from flask_restplus import Resource

from core.server import server
from service.rotinas import Rotina as RotinaService

api = server.api

@api.route('/rotina')
class Rotina(Resource):
    @staticmethod
    def get():
        RotinaService().atualiza_historico()
        return {}

    
    def post(self):
        # TODO implementar atualização de dados retroativos
        ...