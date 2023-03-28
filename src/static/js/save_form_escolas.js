$(document).ready(function(){
    $('#formulario-escolas').on('submit', function(event){
        $(this).find(':input').prop('readonly', true);
        var formulario_escolas = $('form');

        $.ajax({
            data: $('#formulario-escolas').serialize(),
            type: 'POST',
            url: '/api/v1/cadastros/escolas',
            cache:false
        })
        .done(function(data) {
            var botao = document.querySelector('.botao');
            let form_edificios = document.querySelector('.cadastros-edificios')

            $('#successAlert').text(data.nome).show()
            $('#errorAlert').hide();

            setTimeout(function(){
                $('#successAlert').hide();
            }, 5000)

            //apagando botão "PRÓXIMO >"
            botao.style.display = 'none';
            botao.hidden = true;

            //adiciona novo formulário (edifícios)
            form_edificios.insertAdjacentHTML('beforeend', data.edificios)
            // carregar script para o formulário de cadastro de edificios
            // $.getScript("./save_form_edificios.js?" + Math.random(), function() {
            //console.log("Script save_form_edificios.js executado.");
            // });
            console.log("TESTANDO CONSOLE");
        })
        .fail(function(jqXHR, textStatus, errorThrown, data){
            formulario_escolas.find(':input').prop('readonly', false)

            $('#errorAlert').show();
            $('#successAlaert').hide();

            setTimeout(function(){
                $('#errorAlert').hide();
            }, 5000)

        })
        event.preventDefault();
    })
})

