# -*- coding: utf-8 -*-
import unittest
from pagador_koin.reloaded import cadastro


class FormularioKoin(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(FormularioKoin, self).__init__(*args, **kwargs)
        self.formulario = cadastro.FormularioKoin()

    def test_deve_ter_ativo(self):
        self.formulario.ativo.nome.should.be.equal('ativo')
        self.formulario.ativo.ordem.should.be.equal(1)
        self.formulario.ativo.label.should.be.equal('Pagamento ativo?')
        self.formulario.ativo.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.boleano)

    def test_deve_ter_consumer_key(self):
        self.formulario.consumer_key.nome.should.be.equal('token')
        self.formulario.consumer_key.ordem.should.be.equal(2)
        self.formulario.consumer_key.label.should.be.equal('Consumer Key')
        self.formulario.consumer_key.tamanho_max.should.be.equal(128)
        self.formulario.consumer_key.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.texto)
        self.formulario.consumer_key.formato.should.be.equal(cadastro.cadastro.FormatoDeCampo.ascii)

    def test_deve_ter_secret_key(self):
        self.formulario.secret_key.nome.should.be.equal('senha')
        self.formulario.secret_key.ordem.should.be.equal(3)
        self.formulario.secret_key.label.should.be.equal('Secret Key')
        self.formulario.secret_key.tamanho_max.should.be.equal(128)
        self.formulario.secret_key.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.texto)
        self.formulario.secret_key.formato.should.be.equal(cadastro.cadastro.FormatoDeCampo.ascii)
