# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac

import mox

from pagador_koin.koin import autenticador


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
        utc_now.timetuple().AndReturn("12333")
        autenticador.datetime.utcnow().AndReturn(utc_now)
        autenticador.time.mktime("12333").AndReturn("12333")

    def test_deve_retornar_o_timestamp_utc(self):
        self.mox.ReplayAll()
        self.credenciador.timestamp.should.be.equal(12333)

    def test_deve_retornar_corpo_para_hmac(self):
        self.mox.ReplayAll()
        self.credenciador.corpo_hmac.should.be.equal("REQUES_URL12333")

    def test_deve_retornar_base64(self):
        self.mox.StubOutWithMock(autenticador, 'base64')
        self.mox.StubOutWithMock(autenticador, 'hashlib')
        self.mox.StubOutWithMock(autenticador, 'hmac')

        autenticador.hashlib.sha512 = "SHA512"
        new_hmac = self.mox.CreateMockAnything()
        new_hmac.digest().AndReturn("DIGEST")
        autenticador.hmac.new("SECRET_KEY", "REQUES_URL12333", "SHA512").AndReturn(new_hmac)
        autenticador.base64.b64encode("DIGEST").AndReturn("HASH")
        self.mox.ReplayAll()
        self.credenciador.hash.should.be.equal("HASH")

    def test_deve_retornar_o_valor_completo_da_credencial(self):
        self.mox.StubOutWithMock(autenticador, 'base64')
        self.mox.StubOutWithMock(autenticador, 'hashlib')
        self.mox.StubOutWithMock(autenticador, 'hmac')

        autenticador.hashlib.sha512 = "SHA512"
        new_hmac = self.mox.CreateMockAnything()
        new_hmac.digest().AndReturn("DIGEST")
        autenticador.hmac.new("SECRET_KEY", "REQUES_URL12333", "SHA512").AndReturn(new_hmac)
        autenticador.base64.b64encode("DIGEST").AndReturn("HASH")

        utc_now = self.mox.CreateMockAnything()
        utc_now.timetuple().AndReturn("12333")
        autenticador.datetime.utcnow().AndReturn(utc_now)
        autenticador.time.mktime("12333").AndReturn("12333")

        self.mox.ReplayAll()
        self.credenciador.obter_credenciais().should.be.equal("CONSUMER_KEY,HASH,12333")


class TestHashPHP(mox.MoxTestBase):
    def gera_expectativa_datetime(self):
        utc_now = self.mox.CreateMockAnything()
        utc_now.timetuple().AndReturn('TUPLE')
        autenticador.datetime.utcnow().AndReturn(utc_now)
        autenticador.time.mktime('TUPLE').AndReturn(1406729630)

    def setUp(self):
        super(TestHashPHP, self).setUp()
        self.mox.StubOutWithMock(autenticador, 'settings')
        autenticador.settings.REQUEST_URL = "http://api.koin.net.br/V1/TransactionService.svc/Request"
        autenticador.settings.SECRET_KEY = "FEDCBA09876543211234567890ABCDEF"
        autenticador.settings.CONSUMER_KEY = "1234567890ABCDEFFEDCBA0987654321"
        self.mox.StubOutWithMock(autenticador, 'datetime')
        self.mox.StubOutWithMock(autenticador, 'time')
        self.gera_expectativa_datetime()
        self.credenciador = autenticador.Credenciador()

    def test_deve_gerar_o_corpo_hmac_certo(self):
        self.mox.ReplayAll()
        self.credenciador.corpo_hmac.should.be.equal("http://api.koin.net.br/V1/TransactionService.svc/Request1406729630")

    def test_deve_gerar_o_hash_certo(self):
        self.mox.ReplayAll()
        self.credenciador.hash.should.be.equal("bEqg0FSc1pUKaz16WlWwSjwrZfuhrR5oLe0XNrYjEVvnCVwAmkw2JbdrskmWzwQsQpBPMc0yXDdZy2IBNARAuA==")

    def test_deve_gerar_o_mesmo_valor_que_em_php(self):
        self.gera_expectativa_datetime()
        self.mox.ReplayAll()
        self.credenciador.obter_credenciais().should.be.equal("1234567890ABCDEFFEDCBA0987654321,bEqg0FSc1pUKaz16WlWwSjwrZfuhrR5oLe0XNrYjEVvnCVwAmkw2JbdrskmWzwQsQpBPMc0yXDdZy2IBNARAuA==,1406729630")


class TestHashIsolado(mox.MoxTestBase):

    def test_hash_eh_igual(self):
        hash_gerado = hmac.new("FEDCBA09876543211234567890ABCDEF", "http://api.koin.net.br/V1/TransactionService.svc/Request1406729630", hashlib.sha512).hexdigest()
        hash_gerado.should.be.equal("6c4aa0d0549cd6950a6b3d7a5a55b04a3c2b65fba1ad1e682ded1736b623115be7095c009a4c3625b76bb24996cf042c42904f31cd325c3759cb6201340440b8")

    def test_hash_eh_igual_com_binario(self):
        hash_gerado = hmac.new("FEDCBA09876543211234567890ABCDEF", "http://api.koin.net.br/V1/TransactionService.svc/Request1406729630", hashlib.sha512).digest()
        hash_string = base64.b64encode(hash_gerado)
        hash_string.should.be.equal("bEqg0FSc1pUKaz16WlWwSjwrZfuhrR5oLe0XNrYjEVvnCVwAmkw2JbdrskmWzwQsQpBPMc0yXDdZy2IBNARAuA==")
