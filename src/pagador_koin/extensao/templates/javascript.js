//{% load filters %}
$(function() {
    var $koinMensagem = $(".koin-mensagem");
    var pedidoPago = '{{ pedido.situacao_id }}' == '4';
    var pedidoPodePagar = '{{ pedido.situacao_id }}' == '9' || '{{ pedido.situacao_id }}' == '2';
    if (pedidoPago) {
        $koinMensagem.toggleClass("alert-message-warning alert-message-success");
        $("#successMessage").hide();
        $("#jaPago").show();
        $koinMensagem.find(".msg-warning").hide();
        $koinMensagem.find(".msg-success").show();
    }
    else if (pedidoPodePagar) {
        GetKoinFraudID(function (guid) {
            $.getJSON('{% url_loja "checkout_pagador" pedido.numero pagamento.id %}?fraud_id=' + guid + '&ip={% get_client_ip %}')
                .done(function (data) {
                    $koinMensagem.find(".msg-warning").hide();
                    if (data.sucesso) {
                        $koinMensagem.toggleClass("alert-message-warning alert-message-success");
                        $koinMensagem.find(".msg-success").show();
                    }
                    else {
                        $koinMensagem.toggleClass("alert-message-warning alert-message-danger");
                        var $errorMessage = $("#errorMessage");
                        $errorMessage.text(data.status + ": " + data.content.string);
                        $koinMensagem.find(".msg-danger").show();
                    }
                });
        });
    }
    else {
        $(".situacao-pedido").text('{{ pedido.situacao }}');
        $("#aguarde").hide();
        $("#jaProcessado").show();
    }
});
