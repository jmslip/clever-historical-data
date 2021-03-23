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

        if parametro is not None:
            mensagem = mensagem + ": Parametro obrigatório"
        
        response['status'] = status
        response['resposta'] = mensagem

        if parametro is not None:
            response['parametro'] = parametro
        
        return response
