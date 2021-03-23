from investpy import search_quotes

from utils.clever_generics import CleverGenerics


class Ativos():
    def __init__(self) -> None:
        self.pais = 'Brazil'
        self.generics = CleverGenerics()

    def pesquisa(self, ativo, pais = None):
        if pais is not None and not isinstance(pais, str):
            return self.generics.gera_resposta(mensagem=self.generics.err04+'país especificado inválido')
        
        if ativo is None:
            return self.generics.gera_resposta(mensagem=self.generics.err02, parametro='ativo')

        try:
            dados = search_quotes(text=ativo, countries=[self.pais])
        except ValueError:
            return self.generics.gera_resposta(self.generics.err03+'Ativo '+ ativo +' não encontrado')
        
        return dados