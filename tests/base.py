# -*- coding: utf-8 -*-
import unittest
from api_pagador import urls
from api_pagador import app

urls.registrar_reloaded()


class TestBase(unittest.TestCase):
    def setUp(self):
        super(TestBase, self).setUp()
        app.autenticacao.define_valor('chave_aplicacao', 'CHAVE-TESTE')
        self.app = app.app_pagador_reloaded.test_client()
