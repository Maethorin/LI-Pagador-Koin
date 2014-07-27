# -*- coding: utf-8 -*-
import mox
from meio_pagamento.koin.pedido import Comprador, Pedido, DocumentoDeComprador, InformacoesDeComprador, Telefone, Endereco, FormaEnvio, Item, AtributoDeItem
from meio_pagamento.koin.serializacao import CampoSerializavel, EntidadeSerializavel

DADOS_DE_ENVIO_MODELO = {
    "FraudId": "fraud id", # Vai vir da página dentro de um json/dicionario - É obrigatório
    "Reference": "numero pedido", # PedidoVenda.numero - É obrigatório
    "Currency": "BRL", # ??? - É obrigatório - A princípio será sempre BRL - É obrigatório
    "RequestDate": "request date", # PedidoVenda.data_criacao - É obrigatório
    "Price": 100, # PedidoVenda.valor_total - É obrigatório
    "DiscountPercent": 10, # ??? - Não é obrigatório
    "DiscountValue": 0, # PedidoVenda.valor_desconto
    "IncreasePercent": 0, # ??? - Não é obrigatório
    "IncreaseValue": 0, # ??? - Não é obrigatório
    "IsGift": False, #  ??? - É obrigatório
    "PaymentType": "", # Está sem uso - Não é obrigatório
    "Buyer": {
        "Name": "Nome do comprador", # PedidoVenda.cliente.nome - É obrigatório
        "Ip": "127.0.0.1", # Vai vir da página dentro de um json/dicionario - É obrigatório
        "IsFirstPurchase": True, # ??? - Indica se é a primeira compra do cliente na loja - É obrigatório
        "IsReliable": False, # ??? - Indica se a loja confia no comprador - É obrigatório
        "BuyerType": 1, # PedidoVenda.cliente.enderecos(principal=True).tipo - É obrigatório
        "Email": "emailcomprador@email.com", # PedidoVenda.cliente.email - É obrigatório
        "Documents": [
            {"Key": "CPF", "Value": "000.000.000-00"}, # PedidoVenda.cliente.enderecos(principal=True).cpf - É obrigatoório
            {"Key": "RG", "Value": "00.000.000-0"}, # PedidoVenda.cliente.enderecos(principal=True).rg - Não é obrigatoório
        ],
        "AdditionalInfo": [
            {"Key": "Birthday", "Value": "1988-08-02"}, # PedidoVenda.cliente.data_nascimento
            {"Key": "MotherName", "Value": "Fulana de Souza"}, # ??? - Não é obrigatório
        ],
        "Phones": [
            {
                "AreaCode": "11", # PedidoVenda.cliente.telefone_* (extrair o DDD) - É obrigatório
                "Number": "1111-1111", # PedidoVenda.cliente.telefone_* - É obrigatório
                "PhoneType": 3 # PedidoVenda.cliente.telefone_* (de acordo com o nome do campo) - É obrigatório
            }
        ],
        "Address": {
            "City": u"São Paulo", # PedidoVenda.cliente.cidade - É obrigatório
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
            "City": u"São Paulo", # PedidoVenda.endereco_entrega.cidade - É obrigatório
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

    def test_valida_tipo_de_telefones(self):
        Comprador.when.called_with(
            name="Nome", ip="IP", is_first_purchase=True, is_reliable=False, buyer_type=1, email="email", phones=["a", "b"]
        ).should.throw(ValueError, u"O parâmetro phones deve ser uma lista de EntidadeSerializavel")

    def test_valida_tipo_de_endereco(self):
        Comprador.when.called_with(
            name="Nome", ip="IP", is_first_purchase=True, is_reliable=False, buyer_type=1, email="email", address="a"
        ).should.throw(ValueError, u"O parâmetro address deve ser do tipo EntidadeSerializavel")

    def test_to_dict_com_documentos(self):
        documentos = [DocumentoDeComprador(key="CPF", value="000.000.000-00"), DocumentoDeComprador(key="RG", value="00.000.000-0")]
        comprador = Comprador(name="Nome", ip="IP", is_first_purchase=True, is_reliable=False, buyer_type=1, email="email", documents=documentos)
        esperado = {
            "Name": "Nome", "Ip": "IP", "IsFirstPurchase": True, "IsReliable": False, "BuyerType": 1, "Email": "email",
            "Documents": [doc.to_dict() for doc in documentos]
        }
        comprador.to_dict().should.be.equal(esperado)

    def test_to_dict_com_informacoes(self):
        informacoes = [InformacoesDeComprador(key="Birthday", value="data-nascimento"), InformacoesDeComprador(key="MotherName", value="nome-da-mae")]
        comprador = Comprador(name="Nome", ip="IP", is_first_purchase=True, is_reliable=False, buyer_type=1, email="email", additional_info=informacoes)
        esperado = {
            "Name": "Nome", "Ip": "IP", "IsFirstPurchase": True, "IsReliable": False, "BuyerType": 1, "Email": "email",
            "AdditionalInfo": [info.to_dict() for info in informacoes]
        }
        comprador.to_dict().should.be.equal(esperado)

    def test_to_dict_com_telefones(self):
        telefones = [Telefone(area_code="11", number="1111-2222", phone_type=1),  Telefone(area_code="11", number="1111-1111", phone_type=3)]
        comprador = Comprador(name="Nome", ip="IP", is_first_purchase=True, is_reliable=False, buyer_type=1, email="email", phones=telefones)
        esperado = {
            "Name": "Nome", "Ip": "IP", "IsFirstPurchase": True, "IsReliable": False, "BuyerType": 1, "Email": "email",
            "Phones": [tel.to_dict() for tel in telefones]
        }
        comprador.to_dict().should.be.equal(esperado)

    def test_to_dict_com_endereco(self):
        endereco = Endereco(city=u"São Paulo", state="SP", country="Brasil", district="Santa Cecilia", street="Rua Dr Albuquerque Lins",
                            number=1, complement="2 andar, fundos", zip_code="01230-000", address_type=1)
        comprador = Comprador(name="Nome", ip="IP", is_first_purchase=True, is_reliable=False, buyer_type=1, email="email", address=endereco)
        esperado = {
            "Name": "Nome", "Ip": "IP", "IsFirstPurchase": True, "IsReliable": False, "BuyerType": 1, "Email": "email",
            "Address": {
                "City": u"São Paulo",
                "State": "SP",
                "Country": "Brasil",
                "District": "Santa Cecilia",
                "Street": "Rua Dr Albuquerque Lins",
                "Number": 1,
                "Complement": "2 andar, fundos",
                "ZipCode": "01230-000",
                "AddressType": 1
            }
        }
        comprador.to_dict().should.be.equal(esperado)


class TestDocumentoDeComprador(mox.MoxTestBase):
    def test_to_dict(self):
        documento = DocumentoDeComprador(key="CPF", value="000.000.000-00")
        documento.to_dict().should.be.equal({"Key": "CPF", "Value": "000.000.000-00"})


class TestTelefone(mox.MoxTestBase):
    def test_to_dict(self):
        telefone = Telefone(area_code="11", number="1111-1111", phone_type=1)
        telefone.to_dict().should.be.equal({
            "AreaCode": "11",
            "Number": "1111-1111",
            "PhoneType": 1
        })


class TestEndereco(mox.MoxTestBase):
    def test_to_dict(self):
        endereco = Endereco(city=u"São Paulo", state="SP", country="Brasil", district="Santa Cecilia", street="Rua Dr Albuquerque Lins",
                            number=1, complement="2 andar, fundos", zip_code="01230-000", address_type=1)
        endereco.to_dict().should.be.equal({
            "City": u"São Paulo",
            "State": "SP",
            "Country": "Brasil",
            "District": "Santa Cecilia",
            "Street": "Rua Dr Albuquerque Lins",
            "Number": 1,
            "Complement": "2 andar, fundos",
            "ZipCode": "01230-000",
            "AddressType": 1
        })


class TestInformacoesDeComprador(mox.MoxTestBase):
    def test_to_dict(self):
        informacoes = InformacoesDeComprador(key="Birthday", value="data-nascimeto")
        informacoes.to_dict().should.be.equal({"Key": "Birthday", "Value": "data-nascimeto"})


class TestFormaEnvio(mox.MoxTestBase):
    def test_to_dict(self):
        forma_envio = FormaEnvio(price=100, delivery_date="data-chegada", shipping_type=1)
        forma_envio.to_dict().should.be.equal({
            "Price": 100,
            "DeliveryDate": "data-chegada",
            "ShippingType": 1
        })

    def test_to_dict_com_endereco(self):
        endereco = Endereco(city=u"São Paulo", state="SP", country="Brasil", district="Santa Cecilia", street="Rua Dr Albuquerque Lins",
                            number=1, complement="2 andar, fundos", zip_code="01230-000", address_type=1)
        forma_envio = FormaEnvio(price=100, delivery_date="data-chegada", shipping_type=1, address=endereco)
        esperado = {
            "Price": 100,
            "DeliveryDate": "data-chegada",
            "ShippingType": 1,
            "Address": {
                "City": u"São Paulo",
                "State": "SP",
                "Country": "Brasil",
                "District": "Santa Cecilia",
                "Street": "Rua Dr Albuquerque Lins",
                "Number": 1,
                "Complement": "2 andar, fundos",
                "ZipCode": "01230-000",
                "AddressType": 1
            }
        }
        forma_envio.to_dict().should.be.equal(esperado)


class TestAtributoDeItem(mox.MoxTestBase):
    def test_to_dict(self):
        atributo = AtributoDeItem(key="Cor", value="Azul")
        atributo.to_dict().should.be.equal({"Key": "Cor", "Value": "Azul"})


class TestItem(mox.MoxTestBase):
    def test_to_dict(self):
        item = Item(reference="CODITEM01", description="TV 43", category="Eletronico", quantity=2, price=100)
        item.to_dict().should.be.equal({
            "Reference": "CODITEM01",
            "Description": "TV 43",
            "Category": "Eletronico",
            "Quantity": 2,
            "Price": 100,
        })

    def test_valida_tipo_de_atributos(self):
        Item.when.called_with(
            reference="CODITEM01", description="TV 43", category="Eletronico", quantity=2, price=100, attributes=["A"]
        ).should.throw(ValueError, u"O parâmetro attributes deve ser uma lista de EntidadeSerializavel")

    def test_to_dict_com_atributos(self):
        atributos = [AtributoDeItem(key="Cor", value="Azul"), AtributoDeItem(key="Peso", value="10kg")]
        item = Item(reference="CODITEM01", description="TV 43", category="Eletronico", quantity=2, price=100, attributes=atributos)
        esperado = {
            "Reference": "CODITEM01",
            "Description": "TV 43",
            "Category": "Eletronico",
            "Quantity": 2,
            "Price": 100,
            "Attributes": [{"Key": "Cor", "Value": "Azul"}, {"Key": "Peso", "Value": "10kg"}]
        }
        item.to_dict().should.be.equal(esperado)


class TestPedido(mox.MoxTestBase):
    def setUp(self):
        super(TestPedido, self).setUp()
        self.dados_pedido = {
            "fraud_id": "fraud id",
            "reference": "numero pedido",
            "currency": "BRL",
            "request_date": "request date",
            "price": 100,
            "discount_percent": 10,
            "discount_value": 0,
            "increase_percent": 0,
            "increase_value": 0,
            "is_gift": False,
            "payment_type": "",
        }
        self.esperado = {
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

    def test_to_dict_sem_outros_objetos(self):
        pedido = Pedido(**self.dados_pedido)
        pedido.to_dict().should.be.equal(self.esperado)

    def test_valida_tipo_de_comprador(self):
        self.dados_pedido["buyer"] = self.mox.CreateMockAnything()
        Pedido.when.called_with(**self.dados_pedido).should.throw(ValueError, u"O parâmetro buyer deve ser do tipo EntidadeSerializavel")

    def test_valida_tipo_de_items(self):
        self.dados_pedido["items"] = [self.mox.CreateMockAnything()]
        Pedido.when.called_with(**self.dados_pedido).should.throw(ValueError, u"O parâmetro items deve ser uma lista de EntidadeSerializavel")

    def test_valida_tipo_de_forma_de_envio(self):
        self.dados_pedido["shipping"] = self.mox.CreateMockAnything()
        Pedido.when.called_with(**self.dados_pedido).should.throw(ValueError, u"O parâmetro shipping deve ser do tipo EntidadeSerializavel")

    def test_to_dict_com_comprador(self):
        self.dados_pedido["buyer"] = Comprador(name="Nome", ip="IP", is_first_purchase=True, is_reliable=False, buyer_type=1, email="email")
        pedido = Pedido(**self.dados_pedido)
        self.esperado["Buyer"] = {"Name": "Nome", "Ip": "IP", "IsFirstPurchase": True, "IsReliable": False, "BuyerType": 1, "Email": "email"}
        pedido.to_dict().should.be.equal(self.esperado)

    def test_to_dict_com_forma_envio(self):
        self.dados_pedido["shipping"] = FormaEnvio(price=100, delivery_date="data-chegada", shipping_type=1)
        pedido = Pedido(**self.dados_pedido)
        self.esperado["Shipping"] = {"Price": 100, "DeliveryDate": "data-chegada", "ShippingType": 1}
        pedido.to_dict().should.be.equal(self.esperado)

    def test_to_dict_com_items(self):
        items = [
            Item(reference="CODITEM01", description="TV 43", category="Eletronico", quantity=2, price=100),
            Item(reference="CODITEM02", description="Tenis", category="Sapato", quantity=1, price=300)
        ]
        self.dados_pedido["items"] = items
        pedido = Pedido(**self.dados_pedido)
        self.esperado["Items"] = [
            {"Reference": "CODITEM01", "Description": "TV 43", "Category": "Eletronico", "Quantity": 2, "Price": 100},
            {"Reference": "CODITEM02", "Description": "Tenis", "Category": "Sapato", "Quantity": 1, "Price": 300}
        ]
        pedido.to_dict().should.be.equal(self.esperado)

    def test_completo(self):
        endereco = Endereco(city=u"São Paulo", state="SP", country="Brasil", district="Santa Cecilia", street="Rua Dr Albuquerque Lins",
                            number=1, complement="2 andar, fundos", zip_code="01230-000", address_type=1)
        telefones = [Telefone(area_code="11", number="1111-1111", phone_type=3)]
        documentos = [DocumentoDeComprador(key="CPF", value="000.000.000-00"), DocumentoDeComprador(key="RG", value="00.000.000-0")]
        informacoes = [InformacoesDeComprador(key="Birthday", value="1988-08-02"), InformacoesDeComprador(key="MotherName", value="Fulana de Souza")]
        self.dados_pedido["buyer"] = Comprador(name="Nome do comprador", ip="127.0.0.1", is_first_purchase=True, is_reliable=False, buyer_type=1, email="emailcomprador@email.com",
                                               address=endereco, phones=telefones, documents=documentos, additional_info=informacoes)
        self.dados_pedido["shipping"] = FormaEnvio(price=100, delivery_date="2013-11-07 00:00:00", shipping_type=1, address=endereco)
        atributos = [AtributoDeItem(key="Cor", value="Azul"), AtributoDeItem(key="Peso", value="7kg")]
        self.dados_pedido["items"] = [Item(reference="CODITEM01", description="TV 43", category="Eletronico", quantity=2, price=100, attributes=atributos)]
        pedido = Pedido(**self.dados_pedido)
        pedido.to_dict().should.be.equal(DADOS_DE_ENVIO_MODELO)

