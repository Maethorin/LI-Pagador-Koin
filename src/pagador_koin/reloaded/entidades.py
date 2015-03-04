# -*- coding: utf-8 -*-
from decimal import Decimal

from pagador.reloaded import entidades
from pagador_koin.reloaded import cadastro

CODIGO_GATEWAY = 9


class KoinInvalido(Exception):
    pass


class ChaveValor(entidades.BaseParaPropriedade):
    _chaves_alternativas_para_serializacao = {'key': 'Key', 'value': 'Value'}

    # def __init__(self, key, value):
    #     self.key = key
    #     self.value = value


class Item(entidades.BaseParaPropriedade):
    _chaves_alternativas_para_serializacao = {
        'reference': 'Reference',
        'description': 'Description',
        'category': 'Category',
        'quantity': 'Quantity',
        'price': 'Price',
        'attributes': 'Attibutes'
    }

    # def __init__(self, reference, description, category, quantity, price, attributes):
    #     self.reference = reference
    #     self.description = description
    #     self.category = category
    #     self.quantity = quantity
    #     self.price = price
    #     self.attributes = attributes


class FormaEnvio(entidades.BaseParaPropriedade):
    _chaves_alternativas_para_serializacao = {
        'price': 'Price', 'delivery_date': 'DeliveryDate', 'shipping_type': 'ShippingType', 'address': 'Address'
    }

    # def __init__(self, price, delivery_date, shipping_type=1, address=None):
    #     self.price = price
    #     self.delivery_date = delivery_date
    #     self.shipping_type = shipping_type
    #     self.address = address


class Telefone(entidades.BaseParaPropriedade):
    _chaves_alternativas_para_serializacao = {'area_code': 'AreaCode', 'number': 'Number', 'phone_type': 'PhoneType'}

    # def __init__(self, number, phone_type):
    #     numero = self.formatador.converte_tel_em_tupla_com_ddd(number)
    #     self.area_code = numero[0]
    #     self.number = numero[1]
    #     self.phone_type = phone_type


class Endereco(entidades.BaseParaPropriedade):
    _chaves_alternativas_para_serializacao = {
        'city': 'City',
        'state': 'State',
        'country': 'Country',
        'district': 'District',
        'street': 'Street',
        'number': 'Number',
        'complement': 'Complement',
        'zip_code': 'ZipCode',
        'address_type': 'AddressType',
    }

    # def __init__(self, **dados):
    #     self.city = dados['city']
    #     self.state = dados['state']
    #     self.country = dados['country']
    #     self.district = dados['district']
    #     self.street = dados['street']
    #     self.number = dados['number']
    #     self.complement = dados['complement']
    #     self.zip_code = dados['zip_code']
    #     self.address_type = dados['address_type']


class Comprador(entidades.BaseParaPropriedade):
    _chaves_alternativas_para_serializacao = {
        'name': 'Name',
        'ip': 'Ip',
        'is_first_purchase': 'IsFirstPurchase',
        'is_reliable': 'IsReliable',
        'buyer_type': 'BuyerType',
        'email': 'Email',
        'address': 'Address',
        'documentos': 'Documents',
        'phones': 'Phones',
        'addtionanal_info': 'AdditionalInfo'
    }


class Malote(entidades.Malote):
    _chaves_alternativas_para_serializacao = {
        'fraud_id': 'FraudId',
        'reference': 'Reference',
        'currency': 'Currency',
        'request_date': 'RequestDate',
        'price': 'Price',
        'discount_percent': 'DiscountPercent',
        'discount_value': 'DiscountValue',
        'increase_percent': 'IncreasePercent',
        'increase_value': 'IncreaseValue',
        'is_gift': 'IsGift',
        'payment_type': 'PaymentType',
        'buyer': 'Buyer',
        'shipping': 'Shipping',
        'items': 'Items'
    }
    
    def __init__(self, configuracao):
        super(Malote, self).__init__(configuracao)
        self.fraud_id = None
        self.reference = None
        self.currency = 'BRL'
        self.request_date = None
        self.price = Decimal('0.00')
        self.is_gift = False,
        self.payment_type = 21,
        self.buyer = None
        self.shipping = None
        self.items = []

    def tipo(self, tipo):
        tipos = {'PF': 1, 'PJ': 2}
        return tipos[tipo]

    def monta_conteudo(self, pedido, parametros_contrato=None, dados=None):
        try:
            self.fraud_id = dados['fraud_id']
        except KeyError:
            raise KoinInvalido(u'Não foi enviado o fraud id para esse pagamento')
        self.reference = '{:03d}'.format(pedido.numero)
        self.request_date = self.formatador.formata_data(pedido.data_criacao)
        self.price = self.formatador.formata_decimal(pedido.valor_total)
        self.buyer = Comprador(
            name=self.formatador.trata_unicode_com_limite(pedido.cliente['nome']),
            ip=dados['ip'],
            is_first_purchase=pedido.eh_primeira_compra_cliente,
            is_reliable=False,
            buyer_type=self.tipo(pedido.endereco_cliente['tipo']),
            email=pedido.cliente['email'],
            documents=self.documento_de_comprador(pedido),
            additional_info=self.informacao_adicional_de_comprador(pedido),
            phones=self.telefones(pedido),
            address=Endereco(
                city=self.formatador.trata_unicode_com_limite(pedido.endereco_cliente['cidade']),
                state=pedido.endereco_cliente['estado'],
                country='Brasil',
                district=self.formatador.trata_unicode_com_limite(pedido.endereco_cliente['bairro']),
                street=self.formatador.trata_unicode_com_limite(pedido.endereco_cliente['endereco']),
                number=pedido.endereco_cliente['numero'],
                complement=self.formatador.trata_unicode_com_limite(pedido.endereco_cliente['complemento']),
                zip_code=pedido.endereco_cliente['cep'],
                address_type=self.tipo(pedido.endereco_cliente['tipo'])
            )
        )
        self.shipping = FormaEnvio(
            price=self.formatador.formata_decimal(pedido.valor_envio),
            delivery_date=self.formatador.formata_data(pedido.provavel_data_entrega),
            shipping_type=1,
            address=Endereco(
                city=self.formatador.trata_unicode_com_limite(pedido.endereco_entrega['cidade']),
                state=pedido.endereco_entrega['estado'],
                country='Brasil',
                district=self.formatador.trata_unicode_com_limite(pedido.endereco_entrega['bairro']),
                street=self.formatador.trata_unicode_com_limite(pedido.endereco_entrega['endereco']),
                number=pedido.endereco_entrega['numero'],
                complement=self.formatador.trata_unicode_com_limite(pedido.endereco_entrega['complemento']),
                zip_code=pedido.endereco_entrega['cep'],
                address_type=self.tipo(pedido.endereco_entrega['tipo'])
            )
        )
        self.items = self.monta_itens(pedido)

    def documento_de_comprador(self, pedido):
        if pedido.endereco_cliente['tipo'] == "PF":
            return [ChaveValor(key="CPF", value=pedido.endereco_cliente['cpf'])]
        return [ChaveValor(key="CNPJ", value=pedido.endereco_cliente['cnpj'])]

    def informacao_adicional_de_comprador(self, pedido):
        if pedido.endereco_cliente['tipo'] == "PF":
            return [ChaveValor(key="Birthday", value=self.formatador.formata_data(pedido.cliente['data_nascimento'], hora=False))]
        return [ChaveValor(key="RazaoSocial", value=self.formatador.trata_unicode_com_limite(pedido.endereco_cliente['razao_social']))]

    def telefones(self, pedido):
        _telefones = []
        if pedido.cliente['telefone_principal']:
            numero = self.formatador.converte_tel_em_tupla_com_ddd(pedido.cliente['telefone_principal'])
            _telefones.append(Telefone(area_code=numero[0], number=numero[1], phone_type=2))
        if pedido.cliente['telefone_comercial']:
            numero = self.formatador.converte_tel_em_tupla_com_ddd(pedido.cliente['telefone_comercial'])
            _telefones.append(Telefone(area_code=numero[0], number=numero[1], phone_type=3))
        if pedido.cliente['telefone_celular']:
            numero = self.formatador.converte_tel_em_tupla_com_ddd(pedido.cliente['telefone_celular'])
            _telefones.append(Telefone(area_code=numero[0], number=numero[1], phone_type=4))
        return _telefones

    def monta_itens(self, pedido):
        return [
            Item(
                reference=self.formatador.trata_unicode_com_limite(item.sku),
                description=self.formatador.trata_unicode_com_limite(item.nome),
                quantity=self.formatador.formata_decimal(item.quantidade),
                category="Desconhecida",
                price=self.formatador.formata_decimal(item.preco_venda)
            )
            for item in pedido.itens
        ]


class ConfiguracaoMeioPagamento(entidades.ConfiguracaoMeioPagamento):
    _campos = ['ativo', 'token', 'senha']
    _codigo_gateway = CODIGO_GATEWAY

    def __init__(self, loja_id, codigo_pagamento=None):
        super(ConfiguracaoMeioPagamento, self).__init__(loja_id, codigo_pagamento)
        self.preencher_do_gateway(self._codigo_gateway, self._campos)
        self.formulario = cadastro.FormularioKoin()
