# -*- coding: utf-8 -*-
import os

from pagador.configuracao.cadastro import CampoFormulario
from pagador.envio.cliente import Script, TipoScript


class MeioPagamentoFormulario(object):
    consumer_key = CampoFormulario("token", "Consumer Key", requerido=True, tamanho_max=128, ordem=1)
    secret_key = CampoFormulario("senha", "Secret Key", requerido=True, tamanho_max=128, ordem=2)

    def define_valores_em_model(self, model, valores):
        model.ativo = valores["ativo"]
        model.token = valores["token"]
        model.senha = valores["senha"]
        return model

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


class MeioPagamentoScript(object):
    source_fraud_id = Script(tipo=TipoScript.source, conteudo="//resources.koin.net.br/scripts/koin.min.js")

    def _caminho_do_arquivo(self, arquivo):
        diretorio = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(diretorio, "templates", arquivo)

    @property
    def css(self):
        return Script(tipo=TipoScript.css, caminho_arquivo=self._caminho_do_arquivo("style.css"))

    @property
    def function_enviar(self):
        return Script(tipo=TipoScript.javascript, eh_template=True, caminho_arquivo=self._caminho_do_arquivo("javascript.js"))

    @property
    def mensagens(self):
        return Script(tipo=TipoScript.html, caminho_arquivo=self._caminho_do_arquivo("mensagens.html"))

    def to_dict(self):
        return [
            self.css.to_dict(),
            self.source_fraud_id.to_dict(),
            self.function_enviar.to_dict(),
            self.mensagens.to_dict()
        ]