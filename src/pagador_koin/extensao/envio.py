# -*- coding: utf-8 -*-

from pagador.envio.serializacao import EntidadeSerializavel


class Pedido(EntidadeSerializavel):
    _atributos = ["FraudId", "Reference", "Currency", "RequestDate", "Price", "DiscountPercent", "DiscountValue", "IncreasePercent", "IncreaseValue", "IsGift", "PaymentType"]
    _atributos_serializaveis = ["Buyer", "Shipping"]
    _atributos_lista = ["Items"]


class Comprador(EntidadeSerializavel):
    _atributos_lista = ["Documents", "Phones", "AdditionalInfo"]
    _atributos_serializaveis = ["Address"]
    _atributos = ["Name", "Ip", "IsFirstPurchase", "IsReliable", "BuyerType", "Email"]


class DocumentoDeComprador(EntidadeSerializavel):
    _atributos = ["Key", "Value"]


class InformacoesDeComprador(EntidadeSerializavel):
    _atributos = ["Key", "Value"]


class Telefone(EntidadeSerializavel):
    _atributos = ["AreaCode", "Number", "PhoneType"]


class Endereco(EntidadeSerializavel):
    _atributos = ["City", "State", "Country", "District", "Street", "Number", "Complement", "ZipCode", "AddressType"]


class FormaEnvio(EntidadeSerializavel):
    _atributos_serializaveis = ["Address"]
    _atributos = ["Price", "DeliveryDate", "ShippingType"]


class Item(EntidadeSerializavel):
    _atributos_lista = ["Attributes"]
    _atributos = ["Reference", "Description", "Category", "Quantity", "Price"]


class AtributoDeItem(EntidadeSerializavel):
    _atributos = ["Key", "Value"]
