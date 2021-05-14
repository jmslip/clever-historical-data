from flask_restplus import Resource

from core.server import server
from service.calculos import Calculos as CalculosService

api = server.api
calculosService = CalculosService()

@api.route('/calculos')
class Calculos(Resource):
    @staticmethod
    def get():
        calculosService.covariancia(['XINA11', 'BOVA11'])