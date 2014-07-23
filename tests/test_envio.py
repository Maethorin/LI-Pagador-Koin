# -*- coding: utf-8 -*-
import mox
from meio_pagamento.koin.envio import Comprador, Pedido, DocumentoDeComprador, InformacoesDeComprador
from meio_pagamento.koin.serializacao import CampoSerializavel, EntidadeSerializavel


class TestCampoJson(mox.MoxTestBase):
    def test_campo_json_simples(self):
        campo = CampoSerializavel("Nome", "Valor")
        campo.to_dict().should.be.equal({"Nome": "Valor"})

    def test_campo_json_com_atribuicao(self):
        campo = CampoSerializavel("Nome")
        campo.valor = "Valor2"
        campo.to_dict().should.be.equal({"Nome": "Valor2"})

    def test_campo_com_campo(self):
        campo1 = CampoSerializavel("Nome", "Valor")
        campo2 = CampoSerializavel("Nome2", campo1)
        campo2.to_dict().should.be.equal({"Nome2": {"Nome": "Valor"}})

    def test_campo_com_campo_com_campo(self):
        campo1 = CampoSerializavel("Nome", "Valor")
        campo2 = CampoSerializavel("Nome2", campo1)
        campo3 = CampoSerializavel("Nome3", campo2)
        campo3.to_dict().should.be.equal({"Nome3": {"Nome2": {"Nome": "Valor"}}})

    def test_campo_com_campo_com_campo_com_campo_hehehehe(self):
        campo1 = CampoSerializavel("Nome", "Valor")
        campo2 = CampoSerializavel("Nome2", campo1)
        campo3 = CampoSerializavel("Nome3", campo2)
        campo4 = CampoSerializavel("Nome4", campo3)
        campo4.to_dict().should.be.equal({"Nome4": {"Nome3": {"Nome2": {"Nome": "Valor"}}}})

    def test_campo_json_com_json_seralizer(self):
        class TesteSerializer(EntidadeSerializavel):
            coisa = CampoSerializavel("Coisa")
            outra_coisa = CampoSerializavel("Outra Coisa")

            def __init__(self):
                self.coisa.valor = "coisa"
                self.outra_coisa.valor = "outra_coisa"

        campo = CampoSerializavel("Grande Coisa", TesteSerializer())
        campo.to_dict().should.be.equal({"Grande Coisa": {"Coisa": "coisa", "Outra Coisa": "outra_coisa"}})


class TestComprador(mox.MoxTestBase):
    def test_to_dict(self):
        comprador = Comprador(name="Nome", ip="IP", is_first_purchase=True, is_reliable=False, buyer_type=1, email="email")
        comprador.to_dict().should.be.equal({"Name": "Nome", "Ip": "IP", "IsFirstPurchase": True, "IsReliable": False, "BuyerType": 1, "Email": "email"})

    def test_valida_tipo_de_documentos(self):
        Comprador.when.called_with(
            name="Nome", ip="IP", is_first_purchase=True, is_reliable=False, buyer_type=1, email="email", documents=["a", "b"]
        ).should.throw(ValueError, u"O parâmetro documents deve ser uma lista de EntidadeSerializavel")

    def test_valida_tipo_de_informacoes(self):
        Comprador.when.called_with(
            name="Nome", ip="IP", is_first_purchase=True, is_reliable=False, buyer_type=1, email="email", additional_info=["a", "b"]
        ).should.throw(ValueError, u"O parâmetro additional_info deve ser uma lista de EntidadeSerializavel")

    def test_to_dict_com_documentos(self):
        documentos = [DocumentoDeComprador("CPF", "000.000.000-00"), DocumentoDeComprador("RG", "00.000.000-0")]
        comprador = Comprador(name="Nome", ip="IP", is_first_purchase=True, is_reliable=False, buyer_type=1, email="email", documents=documentos)
        esperado = {
            "Name": "Nome", "Ip": "IP", "IsFirstPurchase": True, "IsReliable": False, "BuyerType": 1, "Email": "email",
            "Documents": [doc.to_dict() for doc in documentos]
        }
        comprador.to_dict().should.be.equal(esperado)

    # def test_to_dict_com_informacoes(self):
    #     informacoes = [InformacoesDeComprador("Birthday", "data-nascimento"), InformacoesDeComprador("MotherName", "nome-da-mae")]
    #     comprador = Comprador("Nome", "IP", True, False, 1, "email", additional_info=informacoes)
    #     esperado = {
    #         "Name": "Nome", "Ip": "IP", "IsFirstPurchase": True, "IsReliable": False, "BuyerType": 1, "Email": "email",
    #         "AdditionalInfo": [info.to_dict() for info in informacoes]
    #     }
    #     comprador.to_dict().should.be.equal(esperado)


class TestDocumentoDeComprador(mox.MoxTestBase):
    def test_to_dict(self):
        documento = DocumentoDeComprador("CPF", "000.000.000-00")
        documento.to_dict().should.be.equal({"Key": "CPF", "Value": "000.000.000-00"})


class TestInformacoesDeComprador(mox.MoxTestBase):
    def test_to_dict(self):
        informacoes = InformacoesDeComprador("Birthday", "data-nascimeto")
        informacoes.to_dict().should.be.equal({"Key": "Birthday", "Value": "data-nascimeto"})


class TestPedido(mox.MoxTestBase):
    def test_valida_tipo_de_comprador(self):
        Pedido.when.called_with(
            "fraud id", "numero pedido", "BRL", "request date", 100, 10, 0, 0, 0, False, "", buyer=self.mox.CreateMockAnything()
        ).should.throw(ValueError, u"O parâmetro buyer deve ser do tipo EntidadeSerializavel")

    def test_to_dict_sem_comprador(self):
        pedido = Pedido("fraud id", "numero pedido", "BRL", "request date", 100, 10, 0, 0, 0, False, "")
        esperado = {
            "FraudId": "fraud id",
            "Reference": "numero pedido",
            "Currency": "BRL",
            "RequestDate": "request date",
            "Price": 100,
            "DiscountPercent": 10,
            "DiscountValue": 0,
            "IncreasePercent": 0,
            "IncreaseValue": 0,
            "IsGift": False,
            "PaymentType": ""
        }
        pedido.to_dict().should.be.equal(esperado)

    def test_to_dict_com_comprador(self):
        comprador = Comprador("Nome", "IP", True, False, 1, "email")
        pedido = Pedido("fraud id", "numero pedido", "BRL", "request date", 100, 10, 0, 0, 0, False, "", buyer=comprador)
        esperado = {
            "FraudId": "fraud id",
            "Reference": "numero pedido",
            "Currency": "BRL",
            "RequestDate": "request date",
            "Price": 100,
            "DiscountPercent": 10,
            "DiscountValue": 0,
            "IncreasePercent": 0,
            "IncreaseValue": 0,
            "IsGift": False,
            "PaymentType": "",
            "Buyer": comprador.to_dict()
        }
        pedido.to_dict().should.be.equal(esperado)
