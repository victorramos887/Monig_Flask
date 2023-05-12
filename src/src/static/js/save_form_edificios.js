$(document).ready(function(){
    $('#formulario-edificacoes').on("submit", function(event) {
        
        $(this).find(':input').prop('readonly', true);
        formulario_edificios = $('#formulario-edificacoes');
        $.ajax({
            data: $('#formulario-edificacoes').serialize(),
            type: 'POST',
            url: '/api/v1/cadastros/edificios',
            cache:false
        })
        .done(function(data) {
            var botao = document.querySelector("#btn_save_edificio")
            console.log('Clicado')
            $('#successAlert').text(data.nome_do_edificio).show()
            $('#errorAlert').hide();

            setTimeout(function(){
                $('#successAlert').hide();
            }, 5000)

            botao.style.display = 'none';
            botao.hidden = true;

        })
        .fail(function(jqXHR, textStatus, errorThrown, data){
            formulario_edificios.find(':input').prop('readonly', false)

            $('#errorAlert').show();
            $('#successAlaert').hide();

            setTimeout(function(){
                $('#errorAlert').hide();
            }, 5000)

        })

        event.preventDefault();

    })
})