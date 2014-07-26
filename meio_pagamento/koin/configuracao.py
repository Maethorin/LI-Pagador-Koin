# -*- coding: utf-8 -*-

from pagador.configuracao.cadastro import CampoFormulario
from pagador.envio.cliente import Script, TipoScript


class MeioPagamentoFormulario(object):
    consumer_key = CampoFormulario("token", "Consumer Key", requerido=True, tamanho_max=128)
    secret_key = CampoFormulario("senha", "Secret Key", requerido=True, tamanho_max=128)

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
    texto_pronto = Script(tipo=TipoScript.html, conteudo=u'<p>Seu pagamento está pronto pra ser efetuado. Clique no botão abaixo para enviar os dados para a Koin!</p>')
    btn_pagador = Script(tipo=TipoScript.html, eh_template=True, conteudo='{% load filters %}<a href="{% url_loja "checkout_pagador" pedido.numero %}" id="btnPagador" class="botao principal btn-koin">Pagar com a <img src="{{ STATIC_URL }}img/formas-de-pagamento/{{ pagamento.codigo }}-logo.png" /></a>')

    @property
    def script_enviar(self):
        script = Script(tipo=TipoScript.javascript, eh_template=True)
        script.adiciona_linha('{% load filters %}')
        script.adiciona_linha('    $(function() {')
        script.adiciona_linha('        $("body").on("click", "#btnPagador", function() {')
        script.adiciona_linha('            var $this = $(this);')
        script.adiciona_linha('            if ($this.data("querystring")) {')
        script.adiciona_linha('                var href = $this.attr("href");')
        script.adiciona_linha('                $this.attr("href", href + "?" + $this.data("querystring") + "&" + "ip={% get_client_ip %}");')
        script.adiciona_linha('                console.log($this.attr("href"));')
        script.adiciona_linha('            }')
        script.adiciona_linha('        });')
        script.adiciona_linha('    });')
        return script

    @property
    def function_fraud_id(self):
        script = Script(tipo=TipoScript.javascript)
        script.adiciona_linha('$(function() {')
        script.adiciona_linha('    var $btn = $("#btnPagador");')
        script.adiciona_linha('    var btnHtml = $btn.html();')
        script.adiciona_linha('    $btn.html("Aguarde...");')
        script.adiciona_linha('    GetKoinFraudID(function(guid) {')
        script.adiciona_linha('        $btn.html(btnHtml);')
        script.adiciona_linha('        $btn.data("querystring", "fraud-id=" + guid);')
        script.adiciona_linha('    });')
        script.adiciona_linha('});')
        return script

    def to_dict(self):
        return [
            self.source_fraud_id.to_dict(),
            self.function_fraud_id.to_dict(),
            self.texto_pronto.to_dict(),
            self.btn_pagador.to_dict(),
            self.script_enviar.to_dict()
        ]