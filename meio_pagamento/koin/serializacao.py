# -*- coding: utf-8 -*-
import re


class Atributo(object):
    def __init__(self, nome, eh_lista=False, eh_serializavel=False):
        self.nome = nome
        self.eh_lista = eh_lista
        self.eh_serializavel = eh_serializavel


class CampoSerializavel(object):
    def __init__(self, nome, valor=None):
        self.nome = nome
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, valor):
        self._valor = valor

    def to_dict(self):
        if hasattr(self.valor, "to_dict"):
            return {self.nome: self.valor.to_dict()}
        if type(self.valor) is list:
            return {self.nome: [valor.to_dict() for valor in self.valor]}
        return {self.nome: self.valor}


class EntidadeSerializavel(object):
    atributos = []

    def __init__(self, *args, **kwargs):
        for atributo in self.atributos:
            if type(atributo) is Atributo:
                self.define_valor_de_atributo(atributo, kwargs)

    def define_valor_de_atributo(self, atributo, kwargs):
        nome_python = self.nome_de_atributo_python(atributo.nome)
        if nome_python in kwargs:
            if atributo.eh_serializavel and not issubclass(kwargs[nome_python].__class__, EntidadeSerializavel):
                raise ValueError(u"O parâmetro {} deve ser do tipo EntidadeSerializavel".format(nome_python))
            if atributo.eh_lista:
                valor = self.cria_lista_de_campo_serializavel(atributo.nome, kwargs[nome_python])
                setattr(self, nome_python, valor)
            else:
                setattr(self, nome_python, CampoSerializavel(atributo.nome, kwargs[nome_python]))

    def to_dict(self):
        retorno = {}
        for nome_atributo in dir(self):
            atributo = getattr(self, nome_atributo)
            if type(atributo) is CampoSerializavel:
                retorno.update(atributo.to_dict())
        return retorno

    def nome_de_atributo_python(self, atributo):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', atributo)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def cria_lista_de_campo_serializavel(self, parametro, lista):
        if not type(lista) is list:
            lista = [lista]
        for item in lista:
            if not issubclass(item.__class__, EntidadeSerializavel):
                raise ValueError(u"O parâmetro {} deve ser uma lista de EntidadeSerializavel".format(self.nome_de_atributo_python(parametro)))
        return CampoSerializavel(parametro, lista)