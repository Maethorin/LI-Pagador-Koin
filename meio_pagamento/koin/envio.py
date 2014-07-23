# -*- coding: utf-8 -*-
from meio_pagamento.koin.serializacao import CampoSerializavel, EntidadeSerializavel, Atributo

from pagador.envio.entities import PedidoBase


class Pedido(PedidoBase, EntidadeSerializavel):
    fraud_id = "FraudId"
    reference = "Reference"
    currency = "Currency"
    request_date = "RequestDate"
    price = "Price"
    discount_percent = "DiscountPercent"
    discount_value = "DiscountValue"
    increase_percent = "IncreasePercent"
    increase_value = "IncreaseValue"
    is_gift = "IsGift"
    payment_type = "PaymentType"
    buyer = "Buyer"

    def __init__(self, fraud_id, reference, currency, request_date, price, discount_percent, discount_value, increase_percent,
                 increase_value, is_gift, payment_type, buyer=None):
        self.fraud_id = CampoSerializavel(self.fraud_id, fraud_id)
        self.reference = CampoSerializavel(self.reference, reference)
        self.currency = CampoSerializavel(self.currency, currency)
        self.request_date = CampoSerializavel(self.request_date, request_date)
        self.price = CampoSerializavel(self.price, price)
        self.discount_percent = CampoSerializavel(self.discount_percent, discount_percent)
        self.discount_value = CampoSerializavel(self.discount_value, discount_value)
        self.increase_percent = CampoSerializavel(self.increase_percent, increase_percent)
        self.increase_value = CampoSerializavel(self.increase_value, increase_value)
        self.is_gift = CampoSerializavel(self.is_gift, is_gift)
        self.payment_type = CampoSerializavel(self.payment_type, payment_type)
        if buyer:
            if not issubclass(buyer.__class__, EntidadeSerializavel):
                raise ValueError(u"O parâmetro buyer deve ser do tipo EntidadeSerializavel")
            self.buyer = CampoSerializavel(self.buyer, buyer)


class Comprador(EntidadeSerializavel):
    atributos = [
        Atributo("Name"), Atributo("Ip"), Atributo("IsFirstPurchase"), Atributo("IsReliable"),
        Atributo("BuyerType"), Atributo("Email"), Atributo("Documents", eh_lista=True), Atributo("AdditionalInfo", eh_lista=True)
    ]

    # name = "Name"
    # ip = "Ip"
    # is_first_purchase = "IsFirstPurchase"
    # is_reliable = "IsReliable"
    # buyer_type = "BuyerType"
    # email = "Email"
    # documents = "Documents"
    # additional_info = "AdditionalInfo"

    # def __init__(self, *args, **kwargs):#name, ip, is_first_purchase, is_reliable, buyer_type, email, documents=None, additional_info=None):
    #     pass
        # self.name = CampoSerializavel(self.name, name)
        # self.ip = CampoSerializavel(self.ip, ip)
        # self.is_first_purchase = CampoSerializavel(self.is_first_purchase, is_first_purchase)
        # self.is_reliable = CampoSerializavel(self.is_reliable, is_reliable)
        # self.buyer_type = CampoSerializavel(self.buyer_type, buyer_type)
        # self.email = CampoSerializavel(self.email, email)
        # if documents:
        #     self.documents = self.cria_lista_de_campo_serializavel(self.documents, documents)
        # if additional_info:
        #     self.additional_info = self.cria_lista_de_campo_serializavel(self.additional_info, additional_info)


class DocumentoDeComprador(EntidadeSerializavel):
    key = "Key"
    value = "Value"

    def __init__(self, key, value):
        self.key = CampoSerializavel(self.key, key)
        self.value = CampoSerializavel(self.value, value)


class InformacoesDeComprador(EntidadeSerializavel):
    key = "Key"
    value = "Value"

    def __init__(self, key, value):
        self.key = CampoSerializavel(self.key, key)
        self.value = CampoSerializavel(self.value, value)


dados_envio = {
    "FraudId": "cfbec22f99d2f557e1426821c42ed3dd", # Vai vir da página dentro de um json/dicionario - É obrigatório
    "Reference": "NUMEROPEDIDO", # PedidoVenda.numero - É obrigatório
    "Currency": "BRL", # ??? - É obrigatório - A princípio será sempre BRL - É obrigatório
    "RequestDate": "2013-11-01 13:17:00", # PedidoVenda.data_criacao - É obrigatório
    "Price": 100, # PedidoVenda.valor_total - É obrigatório
    "DiscountPercent": 10, # ??? - Não é obrigatório
    "DiscountValue": 0, # PedidoVenda.valor_desconto
    "IncreasePercent": 0, # ??? - Não é obrigatório
    "IncreaseValue": 0, # ??? - Não é obrigatório
    "IsGift": "false", #  ??? - É obrigatório
    "PaymentType": 21, # Está sem uso - Não é obrigatório
    "Buyer": {
        "Name": "Nome do comprador", # PedidoVenda.cliente.nome - É obrigatório
        "Ip": "127.0.0.1", # Vai vir da página dentro de um json/dicionario - É obrigatório
        "IsFirstPurchase": "true", # ??? - Indica se é a primeira compra do cliente na loja - É obrigatório
        "IsReliable": "false", # ??? - Indica se a loja confia no comprador - É obrigatório
        "BuyerType": 1, # PedidoVenda.cliente.enderecos(principal=True).tipo - É obrigatório
        "Email": "emailcomprador@email.com", # PedidoVenda.cliente.email - É obrigatório
        "Documents": [
            {"Key": "CPF", "Value": ""}, # PedidoVenda.cliente.enderecos(principal=True).cpf - É obrigatoório
            {"Key": "CNPJ", "Value": ""}, # PedidoVenda.cliente.enderecos(principal=True).cnpj - É obrigatoório

            {"Key": "RG", "Value": ""}, # PedidoVenda.cliente.enderecos(principal=True).rg - Não é obrigatoório
            {"Key": "StateRegistration", "Value": ""}, # ??? - Não é obrigatoório
            {"Key": "MunicipalRegistration", "Value": ""} # ??? - Não é obrigatoório
        ],
        "AdditionalInfo": [
            {"Key": "Birthday", "Value": "1988-08-02"}, # PedidoVenda.cliente.data_nascimento
            {"Key": "MotherName", "Value": "Fulana de Souza"}, # ??? - Não é obrigatório

            {"Key": "RazaoSocial", "Value": "ABC123"}, # PedidoVenda.cliente.enderecos(principal=True).razao_social
            {"Key": "MotherName", "Value": "Fulana de Souza"} # ??? - Não é obrigatório
        ],
        "Phones": [
            {
                "AreaCode": "11", # PedidoVenda.cliente.telefone_* (extrair o DDD) - É obrigatório
                "Number": "1111-1111", # PedidoVenda.cliente.telefone_* - É obrigatório
                "PhoneType": 3 # PedidoVenda.cliente.telefone_* (de acordo com o nome do campo) - É obrigatório
            }
        ],
        "Address": {
            "City": "São Paulo", # PedidoVenda.cliente.cidade - É obrigatório
            "State": "SP", # PedidoVenda.cliente.estado - É obrigatório
            "Country": "Brasil", # PedidoVenda.cliente. - É obrigatório
            "District": "Santa Cecilia", # PedidoVenda.cliente.bairro - É obrigatório
            "Street": "Rua Dr Albuquerque Lins", # PedidoVenda.cliente.endereco - É obrigatório
            "Number": 1, # PedidoVenda.cliente.numero - É obrigatório
            "Complement": "2 andar, fundos", # PedidoVenda.cliente.complemento - Não é obrigatório
            "ZipCode": "01230-000", # PedidoVenda.cliente.cep - É obrigatório
            "AddressType": 1 # PedidoVenda.cliente.tipo - Não é obrigatório
        }
    },
    "Shipping": {
        "Address": {
            "City": "São Paulo", # PedidoVenda.endereco_entrega.cidade - É obrigatório
            "State": "SP", # PedidoVenda.endereco_entrega.estado - É obrigatório
            "Country": "Brasil", # PedidoVenda.endereco_entrega.pais - É obrigatório
            "District": "Santa Cecilia", # PedidoVenda.endereco_entrega.bairro - É obrigatório
            "Street": "Rua Dr Albuquerque Lins", # PedidoVenda.endereco_entrega.endereco - É obrigatório
            "Number": 1, # PedidoVenda.endereco_entrega.numero - É obrigatório
            "Complement": "2 andar, fundos", # PedidoVenda.endereco_entrega.complemento - Não é obrigatório
            "ZipCode": "01230-000", # PedidoVenda.endereco_entrega.cep - É obrigatório
            "AddressType": 1 # PedidoVenda.endereco_entrega.tipo - Não é obrigatório
        },
        "Price": 100, # PedidoVenda.valor_envio - Não é obrigatório
        "DeliveryDate": "2013-11-07 00:00:00", # Esse campo tem que ser uma data. Sugiro calcular com base no PedidoVenda.prazo_entrega - É obrigatório
        "ShippingType": 1 # PedidoVenda.envio().id (Será sempre 1, pois só aceita os correios) - É obrigatório
    },
    "Items": [
        {
            "Reference": "CODITEM01", # PedidoVenda.itens[x].sku- É obrigatório
            "Description": "TV 43", # PedidoVenda.itens[x].nome- É obrigatório
            "Category": "Eletronico", # Não é obrigatório
            "Quantity": 2, # PedidoVenda.itens[x].quantidade - É obrigatório
            "Price": 100, # PedidoVenda.itens[x].preco_venda - É obrigatório
            "Attributes": [ # - Não é obrigatório
                {"Key": "Cor", "Value": "Azul"}, # PedidoVenda.itens[x].variacao
                {"Key": "Peso", "Value": "7kg"} # PedidoVenda.itens[x].peso
            ]
        }
    ]
}