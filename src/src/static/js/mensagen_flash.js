//Tirar mensagem flask após alguns segundos

const mensagensFlash  = document.querySelectorAll('.mensagem-flash')


  // Adiciona a classe CSS que inicia a animação de fade-out a cada mensagem
  mensagensFlash .forEach(mensagem => {
    mensagem.classList.add('mensagem-flash');
    // Remove a mensagem do DOM após a animação ser concluída
    mensagem.addEventListener('animationend', () => {
      mensagem.remove();
    });
  });

