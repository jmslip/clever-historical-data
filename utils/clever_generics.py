from datetime import date, datetime
from json import dumps, loads

from peewee import DoesNotExist

from core.models import CleverBaseModel, HistoricalData, Ativo as AtivoModel
from core.serializable import HistoricoSerializable, AtivoSerializable


class CleverGenerics:

    def __init__(self) -> None:
        self.err01 = 'ERR#01: Campo obrigatório'
        self.err02 = 'ERR#02: Valor não pode ser nulo'
        self.err03 = 'ERR#03: Registro não encontrado'
        self.err04 = 'ERR#04: Erro ao processar'
        self.err05 = 'ERR#05: Resgistro duplicado'
        self.suc201 = ''
        self.http_response_200 = 200
        self.http_response_201 = 201
        self.http_response_204 = 204
        self.http_response_400 = 400

    def gera_resposta(self, mensagem, parametro=None, id=None):
        response = {}
        status = self.http_response_200
        if mensagem is None:
            status = self.http_response_400
            mensagem = self.err04
        elif isinstance(mensagem, str):
            if mensagem.startswith(self.err01) or mensagem.startswith(self.err02):
                status = self.http_response_400
            elif mensagem.startswith(self.err03):
                status = self.http_response_204
            elif "sucesso".lower() in mensagem:
                status = self.http_response_201
            else:
                status = self.http_response_400
        else:
            status = self.http_response_400

        if parametro is not None:
            mensagem = mensagem + ": Parametro obrigatório"
        
        response['status'] = status
        response['resposta'] = mensagem

        if parametro is not None:
            response['parametro'] = parametro

        if id is not None:
            response['id'] = id
        
        return response, status


    def valida_parametros_obrigatorios(self, request, parametros):
        for param in parametros:
            return self.valida_campo_requisicao(request=request, campo=param)


    def valida_campo_requisicao(self, request, campo):
        if campo not in request:
            return self.gera_resposta(self.err01, campo)


    def convert_model_to_json(self, model: CleverBaseModel):
        if isinstance(model, HistoricalData):
            historico = HistoricoSerializable(model)
            return historico.to_json()
        elif isinstance(model, AtivoModel):
            ativo = AtivoSerializable(model)
            return ativo.to_json()


    def model_to_json(self, modelResult, model: CleverBaseModel):
        strResult: str
        try:
            strResult = dumps(modelResult.select().where(model.id == modelResult.id).dicts().get(), default=self.dt_parser)
        except DoesNotExist as e:
            print("Erro ao buscar informações do Ativo: ", e)
            return self.gera_resposta(self.err04)

        return loads(strResult)


    def list_model_to_json(self, dados_model: CleverBaseModel, chave_dicionario=None):
        dados = []
        for dado in dados_model:
            dados.append(self.convert_model_to_json(dado))

        if chave_dicionario is not None:
            dados_dict = dict()
            dados_dict[chave_dicionario] = dados

            return dados_dict

        return dados


    def dt_parser(self, dt):
        if isinstance(dt, datetime) or isinstance(dt, date):
            return dt.isoformat()
        elif isinstance(dt, float):
            return round(dt, 2)


    def data_formato_br(self, dt):
        if isinstance(dt, datetime) or isinstance(dt, date):
            return dt.strftime("%d/%m/%Y")
