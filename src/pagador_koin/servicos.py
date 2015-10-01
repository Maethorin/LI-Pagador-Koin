# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import time
from datetime import datetime
from li_common.comunicacao import requisicao
from pagador import servicos, configuracoes


REQUEST_URL = 'http://api.koin.com.br/V1/TransactionService.svc/Request'
if configuracoes.DEBUG:
    REQUEST_URL = 'http://api.qa.koin.in/V1/TransactionService.svc/Request'


MENSAGENS_RETORNO = {
    '0': u'Código de retorno inválido',
    '200': u'Compra aprovada pela Koin.',
    '301': u'Código de verificação de fraude não informado',
    '302': u'A análise / verificação de risco não autorizou o processamento desta operação',
    '304': u'A análise / verificação de risco não autorizou o processamento desta operação',
    '312': u'O pagamento do pedido foi enviado e encontra-se em análise. Você será informado por e-mail sobre o resultado.',
    '314': u'O pagamento do pedido foi enviado e encontra-se em análise. Você será informado por e-mail sobre o resultado.',
    '500': u'Houve um erro ao processar sua compra com Koin. Por favor, tente novamente.',
    '501': u'Não foi possível identificar esta loja. Por favor, tente novamente ou entre em contato com o responsável pela loja.',
    '502': u'Por favor, verifique o endereço de entrega informado. Ele deve ser igual ao utilizado em sua conta Koin.',
    '503': u'Por favor, verifique o E-mail informado. Ele precisa ser o mesmo utilizado em sua conta Koin.',
    '504': u'Por favor, verifique o telefone informado. Ele precisa ser o mesmo utilizado em sua conta Koin.',
    '505': u'Não foi possível processar o seu pedido devido a uma pendência em seu cadastro Koin. Entre em contato com a Koin para maiores informações.',
    '506': u'Não foi possível processar a sua compra devido a uma pendência em seu cadastro, por gentileza, contate o vendedor.',
    '507': u'Não foi possível localizar o seu endereço de entrega, verifique o CEP informado e tente novamente.',
    '508': u'Esta loja não está credenciada para processar pagamentos com Koin. Por favor, contate o vendedor.',
    '509': u'Ocorreu um erro em seu cadastro. Favor entrar em contato com a Koin.',
    '510': u'Não foi possível localizar o seu endereço de entrega. Verifique o CEP informado e tente novamente.',
    '511': u'Essa transação já foi enviada para o Koin anteriormente.',
    '601': u'O valor do seu pedido precisa ser maior do que zero. Verifique o carrinho de compras e tente novamente.',
    '602': u'Não encontramos nenhum produto no carrinho de compras. Por favor, tente novamente.',
    '603': u'O número do seu pedido não é valido. por gentileza, contate o vendedor e tente novamente.',
    '604': u'O código do produto está incorreto. Contate o vendedor e tente novamente.',
    '605': u'Por gentileza, informe o valor do produto.',
    '606': u'Por gentileza, informe a quantidade do produto.',
    '701': u'O seu pedido não poderá ser processado, pois o valor dele excede o seu limite de compras com Koin. Entre em contato com a Koin para maiores informações.',
    '702': u'O limite de vendas da loja foi atingido. Por gentileza, contate o vendedor.',
    '998': u'O pedido já foi enviado está em processo de análise. Você será informado por e-mail.',
    '999': u'Existe um erro nos dados informados. Verifique-os e tente novamente.',
}


class Credenciador(servicos.Credenciador):
    def __init__(self, tipo=None, configuracao=None):
        super(Credenciador, self).__init__(tipo=self.TipoAutenticacao.cabecalho_http, configuracao=configuracao)
        self.secret_key = str(getattr(self.configuracao, 'senha', ''))
        self.consumer_key = str(getattr(self.configuracao, 'token', ''))
        self._timestamp = None

    @property
    def timestamp(self):
        if not self._timestamp:
            self._timestamp = int(time.mktime(datetime.utcnow().timetuple()))
        return self._timestamp

    @property
    def corpo_hmac(self):
        return '{}{}'.format(REQUEST_URL, self.timestamp)

    @property
    def hash(self):
        digest = hmac.new(self.secret_key, self.corpo_hmac, hashlib.sha512).digest()
        return base64.b64encode(digest)

    def obter_credenciais(self):
        return '{},{},{}'.format(self.consumer_key, self.hash, self.timestamp)


class EntregaPagamento(servicos.EntregaPagamento):
    def __init__(self, loja_id, plano_indice=1, dados=None):
        super(EntregaPagamento, self).__init__(loja_id, plano_indice, dados=dados)
        self.tem_malote = True
        self.faz_http = True
        self.conexao = self.obter_conexao()
        self.resposta = None
        self.url = REQUEST_URL

    def define_credenciais(self):
        self.conexao.credenciador = Credenciador(configuracao=self.configuracao)

    def envia_pagamento(self, tentativa=1):
        self.dados_enviados = self.malote.to_dict()
        try:
            self.resposta = self.conexao.post(self.url, self.dados_enviados)
        except requisicao.RespostaJsonInvalida, ex:
            raise self.EnvioNaoRealizado(u'Ocorreu um erro no envio dos dados para a Koin.', self.loja_id, self.pedido.numero, dados_envio=self.malote.to_dict(), erros=[ex.message])

    def processa_dados_pagamento(self):
        self.resultado = self._processa_resposta()

    def define_mensagem(self, mensagem):
        self.dados_pagamento = {
            'conteudo_json': {
                'mensagem_retorno': mensagem,
            }
        }
        return mensagem

    def _processa_resposta(self):
        if not self.resposta:
            return {'mensagem': self.define_mensagem(u'Ocorreu um erro no envio dos dados para a Koin.'), 'status_code': 400}
        status_code = self.resposta.status_code
        if self.resposta.timeout:
            return {'mensagem': self.define_mensagem(u'O servidor da Koin não respondeu em tempo útil.'), 'status_code': status_code}
        if self.resposta.nao_autenticado:
            return {'mensagem': self.define_mensagem(u'Autenticação da loja com a Koin Falhou. Contate o SAC da loja.'), 'status_code': status_code}
        if self.resposta.sucesso:
            if isinstance(self.resposta.conteudo, dict):
                mensagem, code = self._trata_conteudo_dict(status_code)
            else:
                try:
                    self.resposta.conteudo = json.loads(self.resposta.conteudo)
                    mensagem, code = self._trata_conteudo_dict(status_code)
                except ValueError:
                    return {'mensagem': self.define_mensagem(u'A Koin não enviou uma resposta válida.'), 'status': 500}
            return {'mensagem': self.define_mensagem(mensagem), 'status': int(code)}
        self.situacao_pedido = servicos.SituacaoPedido.SITUACAO_PEDIDO_CANCELADO
        return {'mensagem': self.define_mensagem(u'Sua compra não foi aprovada. Por favor, escolha outra forma de pagamento'), 'status_code': status_code}

    def _trata_conteudo_dict(self, status_code):
        code = self.resposta.conteudo.get('Code', 0)
        mensagem = self.resposta.conteudo.get('Message', None)
        if code == 200:
            self.situacao_pedido = servicos.SituacaoPedido.SITUACAO_PEDIDO_PAGO
            return mensagem or 'Compra aprovada pela Koin.', status_code
        if code in [312, 314, 998]:
            self.situacao_pedido = servicos.SituacaoPedido.SITUACAO_PAGTO_EM_ANALISE
            return mensagem or u'O pagamento do pedido foi enviado e encontra-se em análise. Você será informado por e-mail sobre o resultado.', status_code
        self.situacao_pedido = servicos.SituacaoPedido.SITUACAO_PEDIDO_CANCELADO
        if not mensagem:
            mensagem = MENSAGENS_RETORNO[str(code)]
        return mensagem, code
