# -*- coding: utf-8 -*-
from meio_pagamento.koin.pedido import Pedido, Comprador, DocumentoDeComprador, Telefone, Endereco, FormaEnvio, Item

from pagador.envio.requisicao import EnviarPedidoBase


def formata_data(data):
    return data.strftime("%Y-%m-%d %H:%M:%S")


class EnviarPedido(EnviarPedidoBase):
    def __init__(self, pedido, dados):
        super(EnviarPedido, self).__init__(pedido, dados)
        self._comprador_telefones = []
        self.dados = self.gerar_dados_de_envio()

    def gerar_dados_de_envio(self):
        pedido_envio = Pedido(
            fraud_id=self.dados["fraud_id"],
            reference=self.pedido.numero,
            currency="BRL",
            request_date=formata_data(self.pedido.data_criacao),
            price=self.pedido.valor_total,
            discount_value=self.pedido.valor_deconto,
            is_gift=False,
            payment_type=21,
            buyer=Comprador(
                name=self.pedido.cliente.nome,
                ip=self.dados["ip"],
                is_first_purchase=self.pedido.cliente.primeira_vez,
                is_reliable=self.pedido.cliente.eh_confiavel,
                buyer_type=self.tipo(),
                email=self.pedido.cliente.email,
                documents=[self.documento_de_comprador],
                additional_info=[self.informacao_adicional_de_comprador],
                phones=self.telefones,
                address=Endereco(
                    city=self.pedido.cliente.endereco.cidade,
                    state=self.pedido.cliente.endereco.estado,
                    country=self.pedido.cliente.endereco.pais_extenso,
                    district=self.pedido.cliente.endereco.bairro,
                    street=self.pedido.cliente.endereco.endereco,
                    number=self.pedido.cliente.endereco.numero,
                    complement=self.pedido.cliente.endereco.complemento,
                    zip_code=self.pedido.cliente.endereco.cep,
                    address_type=self.tipo()
                )
            ),
            shipping=FormaEnvio(
                price=self.pedido.valor_envio,
                delivery_date=formata_data(self.pedido.provavel_data_entrega),
                shipping_type=1,
                address=Endereco(
                    city=self.pedido.cliente.endereco_entrega.cidade,
                    state=self.pedido.cliente.endereco_entrega.estado,
                    country=self.pedido.cliente.endereco_entrega.pais_extenso,
                    district=self.pedido.cliente.endereco_entrega.bairro,
                    street=self.pedido.cliente.endereco_entrega.endereco,
                    number=self.pedido.cliente.endereco_entrega.numero,
                    complement=self.pedido.cliente.endereco_entrega.complemento,
                    zip_code=self.pedido.cliente.endereco_entrega.cep,
                    address_type=self.tipo(self.pedido.cliente.endereco_entrega.tipo)
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
            return DocumentoDeComprador(key="Birthday", value=formata_data(self.pedido.cliente.data_nascimento))
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
                quantity=item.quantidade,
                price=item.preco_venda
            )
            for item in self.pedido.itens
        ]
