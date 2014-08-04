# -*- coding: utf-8 -*-
import json
from pagador_koin import settings
from pagador_koin.extensao.pedido import Pedido, Comprador, DocumentoDeComprador, Telefone, Endereco, FormaEnvio, Item

from pagador.envio.requisicao import EnviarPedidoBase

MENSAGENS_RETORNO = {
    "0": u"Código de retorno inválido",
    "200": u"Compra aprovada pela Koin.",
    "301": u"Código de verificação de fraude não informado",
    "302": u"A análise / verificação de risco não autorizou o processamento desta operação",
    "304": u"A análise / verificação de risco não autorizou o processamento desta operação",
    "500": u"Houve um erro ao processar sua compra com Koin. Por favor, tente novamente.",
    "501": u"Não foi possível identificar esta loja. Por favor, tente novamente ou entre em contato com o responsável pela loja.",
    "502": u"Por favor, verifique o endereço de entrega informado. Ele deve ser igual ao utilizado em sua conta Koin.",
    "503": u"Por favor, verifique o E-mail informado. Ele precisa ser o mesmo utilizado em sua conta Koin.",
    "504": u"Por favor, verifique o telefone informado. Ele precisa ser o mesmo utilizado em sua conta Koin.",
    "505": u"Não foi possível processar o seu pedido devido a uma pendência em seu cadastro Koin. Entre em contato com a Koin para maiores informações.",
    "506": u"Não foi possível processar a sua compra devido a uma pendência em seu cadastro, por gentileza, contate o vendedor.",
    "507": u"Não foi possível localizar o seu endereço de entrega, verifique o CEP informado e tente novamente.",
    "508": u"Esta loja não está credenciada para processar pagamentos com Koin. Por favor, contate o vendedor.",
    "509": u"Ocorreu um erro em seu cadastro. Favor entrar em contato com a Koin.",
    "510": u"Não foi possível localizar o seu endereço de entrega. Verifique o CEP informado e tente novamente.",
    "511": u"Essa transação já foi enviada para o Koin anteriormente.",
    "601": u"O valor do seu pedido precisa ser maior do que zero. Verifique o carrinho de compras e tente novamente.",
    "602": u"Não encontramos nenhum produto no carrinho de compras. Por favor, tente novamente.",
    "603": u"O número do seu pedido não é valido. por gentileza, contate o vendedor e tente novamente.",
    "604": u"O código do produto está incorreto. Contate o vendedor e tente novamente.",
    "605": u"Por gentileza, informe o valor do produto.",
    "606": u"Por gentileza, informe a quantidade do produto.",
    "701": u"O seu pedido não poderá ser processado, pois o valor dele excede o seu limite de compras com Koin. Entre em contato com a Koin para maiores informações.",
    "702": u"O limite de vendas da loja foi atingido. Por gentileza, contate o vendedor.",
    "998": u"O pedido {} já foi utilizado no processamento de outra transação.",
    "999": u"Existe um erro nos dados informados. Verifique-os e tente novamente.",
}


def formata_data(data, hora=True):
    if hora:
        return data.strftime("%Y-%m-%d %H:%M:%S")
    return data.strftime("%Y-%m-%d")


def formata_decimal(valor):
    return '{0:.3g}'.format(valor)


class EnviarPedido(EnviarPedidoBase):
    def __init__(self, meio_pagamento, pedido, dados, usa_autenticacao=True, configuracao_pagamento=None):
        super(EnviarPedido, self).__init__(meio_pagamento, pedido, dados, usa_autenticacao=usa_autenticacao, configuracao_pagamento=configuracao_pagamento)
        self._comprador_telefones = []
        self.dados = self.gerar_dados_de_envio()
        self.url = settings.REQUEST_URL

    @property
    def chaves_credenciamento(self):
        return ["token", "senha"]

    def gerar_dados_de_envio(self):
        pedido_envio = Pedido(
            fraud_id=self.dados["fraud_id"],
            reference="{:03d}".format(self.pedido.numero),
            currency="BRL",
            request_date=formata_data(self.pedido.data_criacao),
            price=formata_decimal(self.pedido.valor_total),
            discount_value=formata_decimal(self.pedido.valor_desconto),
            is_gift=False,
            payment_type=21,
            buyer=Comprador(
                name=self.pedido.cliente.nome,
                ip=self.dados["ip"],
                is_first_purchase=self.pedido.cliente.eh_primeira_compra_na_loja,
                is_reliable=self.pedido.cliente.eh_confiavel,
                buyer_type=self.tipo(),
                email=self.pedido.cliente.email,
                documents=[self.documento_de_comprador],
                additional_info=[self.informacao_adicional_de_comprador],
                phones=self.telefones,
                address=Endereco(
                    city=self.pedido.cliente.endereco.cidade,
                    state=self.pedido.cliente.endereco.estado,
                    country=self.pedido.cliente.endereco.pais.nome,
                    district=self.pedido.cliente.endereco.bairro,
                    street=self.pedido.cliente.endereco.endereco,
                    number=self.pedido.cliente.endereco.numero,
                    complement=self.pedido.cliente.endereco.complemento,
                    zip_code=self.pedido.cliente.endereco.cep,
                    address_type=self.tipo()
                )
            ),
            shipping=FormaEnvio(
                price=formata_decimal(self.pedido.valor_envio),
                delivery_date=formata_data(self.pedido.provavel_data_entrega),
                shipping_type=1,
                address=Endereco(
                    city=self.pedido.endereco_entrega.cidade,
                    state=self.pedido.endereco_entrega.estado,
                    country=self.pedido.endereco_entrega.pais,
                    district=self.pedido.endereco_entrega.bairro,
                    street=self.pedido.endereco_entrega.endereco,
                    number=self.pedido.endereco_entrega.numero,
                    complement=self.pedido.endereco_entrega.complemento,
                    zip_code=self.pedido.endereco_entrega.cep,
                    address_type=self.tipo(self.pedido.endereco_entrega.tipo)
                )
            ),
            items=self.items,
        )
        return pedido_envio.to_dict()

    def tipo(self, tipo=None):
        if not tipo:
            tipo = self.pedido.cliente.endereco.tipo
        tipos = {'PF': 1, 'PJ': 2}
        return tipos[tipo]

    @property
    def documento_de_comprador(self):
        if self.pedido.cliente.endereco.tipo == "PF":
            return DocumentoDeComprador(key="CPF", value=self.pedido.cliente.endereco.cpf)
        else:
            return DocumentoDeComprador(key="CNPJ", value=self.pedido.cliente.endereco.cnpj)

    @property
    def informacao_adicional_de_comprador(self):
        if self.pedido.cliente.endereco.tipo == "PF":
            return DocumentoDeComprador(key="Birthday", value=formata_data(self.pedido.cliente.data_nascimento, hora=False))
        else:
            return DocumentoDeComprador(key="RazaoSocial", value=self.pedido.cliente.endereco.razao_social)

    @property
    def telefones(self):
        if self.pedido.cliente.telefone_principal:
            self._comprador_telefones.append(Telefone(area_code=self.pedido.cliente.telefone_principal[:1], number=self.pedido.cliente.telefone_principal[1:], phone_type=2))
        if self.pedido.cliente.telefone_comercial:
            self._comprador_telefones.append(Telefone(area_code=self.pedido.cliente.telefone_comercial[:1], number=self.pedido.cliente.telefone_comercial[1:], phone_type=3))
        if self.pedido.cliente.telefone_celular:
            self._comprador_telefones.append(Telefone(area_code=self.pedido.cliente.telefone_celular[:1], number=self.pedido.cliente.telefone_celular[1:], phone_type=4))
        return self._comprador_telefones

    @property
    def items(self):
        return [
            Item(
                reference=item.sku,
                description=item.nome,
                quantity=formata_decimal(item.quantidade),
                category="Desconhecida",
                price=formata_decimal(item.preco_venda)
            )
            for item in self.pedido.itens.all()
        ]

    def processar_resposta(self, resposta):
        if resposta.status_code != 200:
            return {"content": resposta.content, "status": resposta.status_code}
        content = json.loads(resposta.content)
        code = content.get("Code", 0)
        if code == 200:
            return {"content": content.get("Message", "Compra aprovada pela Koin."), "status": resposta.status_code}
        mensagem = content.get("Message", None)
        if not mensagem:
            mensagem = MENSAGENS_RETORNO[str(code)]
        return {"content": mensagem, "status": int(code)}
