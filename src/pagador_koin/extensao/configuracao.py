# -*- coding: utf-8 -*-

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
    mensagem_aguarde = Script(tipo=TipoScript.html, conteudo=u'<p class="koin-mensagem alert alert-warning">Comunicando com a Koin. Por favor aguarde...</p>')

    @property
    def function_enviar(self):
        script = Script(tipo=TipoScript.javascript, eh_template=True)
        script.adiciona_linha('{% load filters %}')
        script.adiciona_linha('$(function() {')
        script.adiciona_linha('    GetKoinFraudID(function(guid) {')
        script.adiciona_linha('        var $koinMensagem = $(".koin-mensagem");')
        script.adiciona_linha('        $koinMensagem.text("Comunicação estabelecida! Enviando seu pedido");')
        script.adiciona_linha('        $.getJSON("{% url_loja "checkout_pagador" pedido.numero pagamento.id %}?fraud-id=" + guid + "&ip={% get_client_ip %}")')
        script.adiciona_linha('            .done(function(data) {')
        script.adiciona_linha('                  if (data.sucesso) {')
        script.adiciona_linha('                      $koinMensagem.toggleClass("alert-warning alert-success", 600);')
        script.adiciona_linha('                  }')
        script.adiciona_linha('                  else {')
        script.adiciona_linha('                      $koinMensagem.toggleClass("alert-warning alert-danger", 600);')
        script.adiciona_linha('                  }')
        script.adiciona_linha('                  console.log(data); $koinMensagem.text(data.mensagem);')
        script.adiciona_linha('            });')
        script.adiciona_linha('    });')
        script.adiciona_linha('});')
        return script

    def to_dict(self):
        return [
            self.source_fraud_id.to_dict(),
            self.function_enviar.to_dict(),
            self.mensagem_aguarde.to_dict()
        ]