from flask_restplus import Resource
from peewee import IntegrityError
from json import dumps, loads

from core.server import server
from core.models import Ativo as AtivoModel
from utils.clever_generics import CleverGenerics
from service.ativos import Ativos

app = server.app
api = server.api
clever_generics = CleverGenerics()

parametros = ['simbolo', 'pais']
parametros_obrigatorios = ['simbolo']


@api.route('/ativos')
class Ativo(Resource):
    @staticmethod
    def post():
        request = api.payload

        err = clever_generics.valida_parametros_obrigatorios(request=request, parametros=parametros_obrigatorios)

        if err is not None:
            return err

        simbolo = request['simbolo']

        pais = None
        if 'pais' in request:
            pais = request['pais']

        pesquisa = Ativos().pesquisa(ativo=simbolo, pais=pais)

        if isinstance(pesquisa, str):
            return pesquisa

        ativoModel = AtivoModel()
        if isinstance(pesquisa, list):
            for ativo in pesquisa:
                ativoModel = AtivoModel(
                    simbolo = ativo.symbol,
                    nome = ativo.name,
                    pais = ativo.country
                )

        try:
            ativoModel.save()
        except IntegrityError:
            return clever_generics.gera_resposta(clever_generics.err04)

        return clever_generics.model_to_json(ativoModel, AtivoModel)
        