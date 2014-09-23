# -*- coding: utf-8 -*-
import os

from pagador.configuracao.cadastro import CampoFormulario, FormularioBase, CadastroBase, SelecaoBase
from pagador.configuracao.cliente import Script, TipoScript
from pagador_koin import settings


def caminho_do_arquivo_de_template(arquivo):
    diretorio = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(diretorio, "templates", arquivo)


class MeioPagamentoCadastro(CadastroBase):
    @property
    def descricao_para_lojista(self):
        script = Script(tipo=TipoScript.html, nome="descricao")
        script.adiciona_linha('<p>A <a href="http://www.koin.com.br" target="_blank">Koin</a> é um novo modelo de negócio para suas vendas online.</p>')
        script.adiciona_linha('<p>Proporcione ao seu cliente a experiência do pós-pago. Ofereça o benefício de pagar pelo pedido só depois de receber!</p>')
        script.adiciona_linha('<p>Vendas sem o risco da inadimplência e fraude, a Koin assume todos os riscos.</p>')
        script.adiciona_linha('<p>Para credenciar sua loja, <a href="http://www.koin.com.br/home/integracao" target="_blank">clique aqui</a>.</p>')
        return script

    @property
    def registro(self):
        script = Script(tipo=TipoScript.html, nome="registro")
        script.adiciona_linha(u'Envie dados para credenciar sua loja junto à Koin.<br/>')
        script.adiciona_linha('<a href="http://www.koin.com.br/home/integracao" title="Acessar Site da Koin" class="btn btn-info btn-xs" target="_blank">Acesse</a>')
        return script

    def to_dict(self):
        return {
            "html": [
                self.descricao_para_lojista.to_dict(),
                self.registro.to_dict()
            ]
        }


class Formulario(FormularioBase):
    consumer_key = CampoFormulario("token", "Consumer Key", requerido=True, tamanho_max=128, ordem=2)
    secret_key = CampoFormulario("senha", "Secret Key", requerido=True, tamanho_max=128, ordem=3)


class MeioPagamentoEnvio(object):
    source_fraud_id = Script(tipo=TipoScript.source, conteudo="//resources.koin.{}.br/scripts/koin.min.js".format(("net" if settings.DEBUG else "com")))

    @property
    def css(self):
        return Script(tipo=TipoScript.css, caminho_arquivo=caminho_do_arquivo_de_template("style.css"))

    @property
    def function_enviar(self):
        return Script(tipo=TipoScript.javascript, eh_template=True, caminho_arquivo=caminho_do_arquivo_de_template("javascript.js"))

    @property
    def mensagens(self):
        return Script(tipo=TipoScript.html, caminho_arquivo=caminho_do_arquivo_de_template("mensagens.html"))

    def to_dict(self):
        return [
            self.css.to_dict(),
            self.source_fraud_id.to_dict(),
            self.function_enviar.to_dict(),
            self.mensagens.to_dict()
        ]


class MeioPagamentoSelecao(SelecaoBase):
    selecao = Script(tipo=TipoScript.html, nome="selecao", caminho_arquivo=caminho_do_arquivo_de_template("selecao.html"), eh_template=True)

    def to_dict(self):
        return [
            self.selecao.to_dict()
        ]
