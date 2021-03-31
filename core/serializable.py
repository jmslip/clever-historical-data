from json import dumps, loads

from core.models import Ativo as AtivoModel, HistoricalData as HistoricoModel

class AtivoSerializable:

    def __init__(self, ativoModel: AtivoModel) -> None:
        self.data_criacao = ativoModel.created
        self.simbolo = ativoModel.simbolo
        self.nome = ativoModel.nome
        self.pais = ativoModel.pais

    
    def to_json(self):
        dicionario = {
            "data_criacao": self.data_criacao.isoformat(),
            "simbolo": self.simbolo,
            "nome": self.nome,
            "pais": self.pais
        }

        return loads(dumps(dicionario))


class HistoricoSerializable:

    def __init__(self, historicoModel: HistoricoModel) -> None:
        self.data_criacao = historicoModel.created
        self.data_historico = historicoModel.data_historico
        self.ultimo = historicoModel.ultimo
        self.variacao = historicoModel.variacao
        self.ativo = AtivoSerializable(historicoModel.ativo)

    
    def to_json(self):
        dicionario = {
            "data_criacao": self.data_criacao.isoformat(),
            "data_historico": self.data_historico.isoformat(),
            "ultimo": str(self.ultimo),
            "variacao": str(self.variacao),
            "ativo": self.ativo.to_json()
        }

        return loads(dumps(dicionario))
