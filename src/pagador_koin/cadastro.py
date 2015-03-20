# -*- coding: utf-8 -*-

from li_common.padroes import cadastro


class FormularioKoin(cadastro.Formulario):
    ativo = cadastro.CampoFormulario('ativo', 'Pagamento ativo?', tipo=cadastro.TipoDeCampo.boleano, ordem=1)
    consumer_key = cadastro.CampoFormulario('token', 'Consumer Key', requerido=True, tamanho_max=128, ordem=2, formato=cadastro.FormatoDeCampo.ascii)
    secret_key = cadastro.CampoFormulario('senha', 'Secret Key', requerido=True, tamanho_max=128, ordem=3, formato=cadastro.FormatoDeCampo.ascii)
