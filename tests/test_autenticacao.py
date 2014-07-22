# -*- coding: utf-8 -*-


import mox

from meio_pagamento.koin import autenticador


class TestMontaCredenciais(mox.MoxTestBase):
    def setUp(self):
        super(TestMontaCredenciais, self).setUp()
        self.mox.StubOutWithMock(autenticador, 'settings')
        autenticador.settings.REQUEST_URL = "REQUES_URL"
        autenticador.settings.SECRET_KEY = "SECRET_KEY"
        autenticador.settings.CONSUMER_KEY = "CONSUMER_KEY"
        self.mox.StubOutWithMock(autenticador, 'datetime')
        self.mox.StubOutWithMock(autenticador, 'time')
        self.credenciador = autenticador.Credenciador()
        utc_now = self.mox.CreateMockAnything()
        utc_now.timetuple().AndReturn("TIMETUPLE")
        autenticador.datetime.utcnow().AndReturn(utc_now)
        autenticador.time.mktime("TIMETUPLE").AndReturn("TIMESTAMP")

    def test_deve_retornar_o_timestamp_utc(self):
        self.mox.ReplayAll()
        self.credenciador.timestamp.should.be.equal("TIMESTAMP")

    def test_deve_retornar_corpo_para_hmac(self):
        self.mox.ReplayAll()
        self.credenciador.corpo_hmac.should.be.equal("REQUES_URLTIMESTAMP")

    def test_deve_retornar_base64(self):
        self.mox.StubOutWithMock(autenticador, 'base64')
        self.mox.StubOutWithMock(autenticador, 'hashlib')
        self.mox.StubOutWithMock(autenticador, 'hmac')

        autenticador.hashlib.sha512 = "SHA512"
        new_hmac = self.mox.CreateMockAnything()
        new_hmac.digest().AndReturn("DIGEST")
        autenticador.hmac.new("SECRET_KEY", "REQUES_URLTIMESTAMP", "SHA512").AndReturn(new_hmac)
        autenticador.base64.encodestring("DIGEST").AndReturn("HASH")
        self.mox.ReplayAll()
        self.credenciador.hash.should.be.equal("HASH")

    def test_deve_retornar_o_valor_completo_da_credencial(self):
        self.mox.StubOutWithMock(autenticador, 'base64')
        self.mox.StubOutWithMock(autenticador, 'hashlib')
        self.mox.StubOutWithMock(autenticador, 'hmac')

        autenticador.hashlib.sha512 = "SHA512"
        new_hmac = self.mox.CreateMockAnything()
        new_hmac.digest().AndReturn("DIGEST")
        autenticador.hmac.new("SECRET_KEY", "REQUES_URLTIMESTAMP", "SHA512").AndReturn(new_hmac)
        autenticador.base64.encodestring("DIGEST").AndReturn("HASH")

        utc_now = self.mox.CreateMockAnything()
        utc_now.timetuple().AndReturn("TIMETUPLE")
        autenticador.datetime.utcnow().AndReturn(utc_now)
        autenticador.time.mktime("TIMETUPLE").AndReturn("TIMESTAMP")

        self.mox.ReplayAll()
        self.credenciador.obter_credenciais().should.be.equal("CONSUMER_KEYHASHTIMESTAMP")