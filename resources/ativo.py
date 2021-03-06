from flask_restplus import Resource
from peewee import IntegrityError, fn

from core.server import server
from core.models import Ativo as AtivoModel
from utils.clever_generics import CleverGenerics
from service.ativos import Ativos

app = server.app
api = server.api
clever_generics = CleverGenerics()
ativosService = Ativos()

parametros = ['simbolo', 'pais', 'nome']
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

        pesquisa = ativosService.pesquisa(ativo=simbolo, pais=pais)

        if isinstance(pesquisa, str):
            return pesquisa

        nome = None
        if 'nome' in request:
            nome = request['nome']

        ativoModel = AtivoModel()
        if nome is None:
            nome = pesquisa.name


        try:
            ativoModel = AtivoModel(
                id = pesquisa.id_,
                simbolo = pesquisa.symbol,
                nome = nome,
                pais = pesquisa.country
            )

            ativoModel.save(force_insert=True)
        except IntegrityError as e:
            print("Erro ao salvar Ativo: ", e)
            error = e.args
            for err in error:
                if 'duplicate key' in err:
                    return clever_generics.gera_resposta(clever_generics.err05, id=ativoModel.get_id())
            return clever_generics.gera_resposta(clever_generics.err04)
        except AttributeError as ae:
            print("Erro ao salvar Ativo: ", ae)
            return clever_generics.gera_resposta(clever_generics.err04)

        return clever_generics.model_to_json(ativoModel, AtivoModel), 201
        

    @staticmethod
    def get():
        request = api.payload
        simbolo = pais = clever = None
        pesquisa_simbolo = pesquisa_pais = pesquisa_clever = False
        lista_simbolos_clever = list()

        if request is not None:
            if 'simbolo' in request:
                simbolo = request['simbolo']
                pesquisa_simbolo = True

            if 'pais' in request:
                pais = request['pais']
                pesquisa_pais = True

            if 'clever' in request:
                pesquisa_clever = True

        if pesquisa_clever:
            ativos = AtivoModel().select().where(AtivoModel.inflacao != 'S')
            return clever_generics.list_model_to_json(dados_model=ativos, chave_dicionario='ativos')


        if pesquisa_simbolo and pesquisa_pais:
            ativos = AtivoModel().select().where(fn.LOWER(AtivoModel.simbolo) == fn.LOWER(simbolo), fn.LOWER(AtivoModel.pais) == fn.LOWER(pais))
        elif pesquisa_simbolo and not pesquisa_pais:
            ativos = AtivoModel().select().where(fn.LOWER(AtivoModel.simbolo) == fn.LOWER(simbolo))
        elif not pesquisa_simbolo and pesquisa_pais:
            ativos = AtivoModel().select().where(fn.LOWER(AtivoModel.pais) == fn.LOWER(pais))
        else:
            ativos = ativosService.all_ativos_banco(to_dict=False)         
        
        return clever_generics.list_model_to_json(dados_model=ativos, chave_dicionario='ativos')
        