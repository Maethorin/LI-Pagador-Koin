# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac

import time
from datetime import datetime
from meio_pagamento import settings


class Credenciador(object):

    @property
    def timestamp(self):
        return time.mktime(datetime.utcnow().timetuple())

    @property
    def corpo_hmac(self):
        return "{}{}".format(settings.REQUEST_URL, self.timestamp)

    @property
    def hash(self):
        digest = hmac.new(settings.SECRET_KEY, self.corpo_hmac, hashlib.sha512).digest()
        return base64.encodestring(digest)

    def obter_credenciais(self, credenciamento=None):
        return "{}{}{}".format(settings.CONSUMER_KEY, self.hash, self.timestamp)