# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac

import time
from datetime import datetime
from pagador.seguranca.autenticador import TipoAutenticacao
from pagador_koin import settings
from pagador.seguranca import autenticador


class Credenciador(autenticador.Credenciador):
    def __init__(self, configuracao):
        self.secret_key = str(getattr(configuracao, "senha", ""))
        self.consumer_key = str(getattr(configuracao, "token", ""))
        self.tipo = TipoAutenticacao.cabecalho_http

    @property
    def chaves_credenciamento(self):
        return ["senha", "token"]

    @property
    def timestamp(self):
        return int(time.mktime(datetime.utcnow().timetuple()))

    @property
    def corpo_hmac(self):
        return "{}{}".format(settings.REQUEST_URL, self.timestamp)

    @property
    def hash(self):
        digest = hmac.new(self.secret_key, self.corpo_hmac, hashlib.sha512).digest()
        return base64.b64encode(digest)

    def obter_credenciais(self):
        return "{},{},{}".format(self.consumer_key, self.hash, self.timestamp)