# -*- coding: utf-8 -*-

from pagador.envio.serializacao import EntidadeSerializavel, Atributo


class Pedido(EntidadeSerializavel):
    _atributos = ["FraudId", "Reference", "Currency", "RequestDate",
                  "Price", "DiscountPercent", "DiscountValue", "IncreasePercent", "IncreaseValue",
                  "IsGift", "PaymentType", "Buyer", "Shipping", "Items"]
    atributos = [
        Atributo(atributo, eh_serializavel=(atributo == "Buyer" or atributo == "Shipping"), eh_lista=(atributo == "Items"))
        for atributo in _atributos
    ]


class Comprador(EntidadeSerializavel):
    atributos = [
        Atributo("Name"), Atributo("Ip"), Atributo("IsFirstPurchase"), Atributo("IsReliable"),
        Atributo("BuyerType"), Atributo("Email"),
        Atributo("Documents", eh_lista=True),
        Atributo("Phones", eh_lista=True),
        Atributo("AdditionalInfo", eh_lista=True),
        Atributo("Address", eh_serializavel=True)
    ]


class DocumentoDeComprador(EntidadeSerializavel):
    atributos = [Atributo("Key"), Atributo("Value")]


class InformacoesDeComprador(EntidadeSerializavel):
    atributos = [Atributo("Key"), Atributo("Value")]


class Telefone(EntidadeSerializavel):
    atributos = [Atributo("AreaCode"), Atributo("Number"), Atributo("PhoneType")]


class Endereco(EntidadeSerializavel):
    atributos = [
        Atributo("City"),
        Atributo("State"),
        Atributo("Country"),
        Atributo("District"),
        Atributo("Street"),
        Atributo("Number"),
        Atributo("Complement"),
        Atributo("ZipCode"),
        Atributo("AddressType")
    ]


class FormaEnvio(EntidadeSerializavel):
    atributos = [
        Atributo("Price"),
        Atributo("DeliveryDate"),
        Atributo("ShippingType"),
        Atributo("Address", eh_serializavel=True)
    ]


class Item(EntidadeSerializavel):
    atributos = [
        Atributo("Reference"),
        Atributo("Description"),
        Atributo("Category"),
        Atributo("Quantity"),
        Atributo("Price"),
        Atributo("Attributes", eh_lista=True)
    ]


class AtributoDeItem(EntidadeSerializavel):
    atributos = [Atributo("Key"), Atributo("Value")]
