$("#formas-pagamento-wrapper").on("click", "#finalizarCompra", function(event) {
    if (!$("#radio-koin").is(':checked')) {
        return true;
    }
    if (!$("#aceiteTermosKoin").is(':checked')) {
        alert("Você precisa aceitar os Termos de Serviço da Koin Pós-Pago.");
        event.preventDefault();
        return false;
    }
});