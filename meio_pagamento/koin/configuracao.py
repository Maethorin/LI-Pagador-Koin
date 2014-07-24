# -*- coding: utf-8 -*-

from pagador.configuracao.cadastro import CampoFormulario


class PagamentoConfiguracao(object):
    consumer_key = CampoFormulario("token", "Consumer Key", requerido=True, tamanho_max=128)
    secret_key = CampoFormulario("senha", "Secret Key", requerido=True, tamanho_max=128)