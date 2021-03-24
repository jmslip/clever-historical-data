from datetime import datetime
from json import dumps, loads


class CleverGenerics:

    def __init__(self) -> None:
        self.err01 = 'ERR#01'
        self.err02 = 'ERR#02'
        self.err03 = 'ERR#03'
        self.err04 = 'ERR#04: Erro ao processar'
        self.http_response_200 = 200
        self.http_response_204 = 204
        self.http_response_400 = 400

    def gera_resposta(self, mensagem, parametro=None):
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
        
        return response, status


    def valida_parametros_obrigatorios(self, request, parametros):
        for param in parametros:
            return self.valida_campo_requisicao(request=request, campo=param)


    def valida_campo_requisicao(self, request, campo):
        if campo not in request:
            return self.gera_resposta(self.err01, campo)


    def model_to_json(self, modelResult, model):
        strResult = dumps(modelResult.select().where(model.id == modelResult.id).dicts().get(), default=self.dt_parser)

        return loads(strResult)


    def dt_parser(self, dt):
        if isinstance(dt, datetime):
            return dt.isoformat()
