//{% load filters %}
$(function() {
    var pedidoPago = '{{ pedido.situacao_id }}' == '4';
    GetKoinFraudID(function(guid) {
        var $koinMensagem = $(".koin-mensagem");
        if (pedidoPago) {
            $koinMensagem.toggleClass("alert-message-warning alert-message-success");
            $("#successMessage").hide();
            $("#jaPago").show();
            $koinMensagem.find(".msg-warning").hide();
            $koinMensagem.find(".msg-success").show();
        }
        else {
            $.getJSON('{% url_loja "checkout_pagador" pedido.numero pagamento.id %}?fraud-id=' + guid + '&ip={% get_client_ip %}')
            .done(function(data) {
                if (jQuery.ui) {
                    $koinMensagem.find(".msg-warning").hide(600);
                }
                else {
                    $koinMensagem.find(".msg-warning").hide();
                }
                if (data.sucesso) {
                    $koinMensagem.toggleClass("alert-message-warning alert-message-success");
                    $koinMensagem.find(".msg-success").show();
                }
                else {
                    if (jQuery.ui) {
                        $koinMensagem.toggleClass("alert-message-warning alert-message-danger", 600, function() {
                            var $errorMessage = $("#errorMessage");
                            $errorMessage.text(data.status + ": " + data.content);
                            $koinMensagem.find(".msg-danger").show();
                        });
                    }
                    else {
                        $koinMensagem.toggleClass("alert-message-warning alert-message-danger");
                        var $errorMessage = $("#errorMessage");
                        $errorMessage.text(data.status + ": " + data.content);
                        $koinMensagem.find(".msg-danger").show();
                    }
                }
            });
        }
    });
});
