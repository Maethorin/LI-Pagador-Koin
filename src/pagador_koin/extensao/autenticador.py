# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac

import time
from datetime import datetime
from pagador_koin import settings


class Credenciador(object):
    def __init__(self, credenciamento):
        self.secret_key = str(credenciamento["senha"])
        self.consumer_key = str(credenciamento["token"])

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