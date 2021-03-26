from investpy import search_quotes

from utils.clever_generics import CleverGenerics
from core.models import Ativo as AtivoModel


class Ativos():
    def __init__(self) -> None:
        self.pais = 'Brazil'
        self.generics = CleverGenerics()


    def pesquisa(self, ativo, pais = None):
        if pais is not None:
            if pais is not isinstance(pais, str):
                return self.generics.gera_resposta(mensagem=self.generics.err04+'país especificado inválido')
            else:
                self.pais = pais
        
        if ativo is None:
            return self.generics.gera_resposta(mensagem=self.generics.err02, parametro='ativo')

        try:
            dados = search_quotes(text=ativo, countries=[self.pais])
        except ValueError:
            return self.generics.gera_resposta(self.generics.err03+'Ativo '+ ativo +' não encontrado')
        except RuntimeError as e:
            return self.generics.gera_resposta('{0}'.format(e))

        return dados


    def all_ativos_banco(self, to_dict=True):
        if to_dict:
            return (AtivoModel().select()).dicts()
        return AtivoModel().select()