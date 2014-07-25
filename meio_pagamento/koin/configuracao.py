# -*- coding: utf-8 -*-

from pagador.configuracao.cadastro import CampoFormulario


class MeioPagamentoFormulario(object):
    consumer_key = CampoFormulario("token", "Consumer Key", requerido=True, tamanho_max=128)
    secret_key = CampoFormulario("senha", "Secret Key", requerido=True, tamanho_max=128)

    def to_dict(self):
        return {
            "consumer_key": self.consumer_key.to_dict(),
            "secret_key": self.secret_key.to_dict()
        }


class MeioPagamentoValores(object):
    def __init__(self, model):
        self.model = model

    def to_dict(self):
        return {
            'consumer_key': {
                'campo': 'token',
                'valor': self.model.token
            },
            'secret_key': {
                'campo': 'senha',
                'valor': self.model.senha
            }
        }