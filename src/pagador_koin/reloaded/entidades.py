# -*- coding: utf-8 -*-

from pagador.reloaded import entidades
from pagador_koin.reloaded import cadastro


class ConfiguracaoMeioPagamento(entidades.ConfiguracaoMeioPagamento):
    _campos = ['ativo', 'token', 'senha']
    _codigo_gateway = 9

    def __init__(self, loja_id):
        super(ConfiguracaoMeioPagamento, self).__init__(loja_id)
        self.preencher_do_gateway(self._codigo_gateway, self._campos)
        self.formulario = cadastro.FormularioKoin()
