//var cadastroEdificacao = document.querySelector('.cadastroEdificacao');

//cadastroEdificacao.addEventListener('click', function() {
 //   alert('Cadastrar nova edificação clicado!');
//})

//Adiciona o formulário de Cadastro de Edificação e retira o botão de cadastrar nova.
const novaEdificacao = document.querySelector(".cadastroEdificacao");

function callback() {
    const addForm = document.querySelector(".container-form");
    addForm.removeAttribute("style");
  
    const sumirNovoCadastro = document.querySelector(".cadastroEdificacao");
    sumirNovoCadastro.setAttribute("style", "display: none;");
  }
  
// novaEdificacao.addEventListener("click", callback);