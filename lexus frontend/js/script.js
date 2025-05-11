document.addEventListener("DOMContentLoaded", function() {
    console.log("Página carregada!");
});
document.querySelector('form').addEventListener('submit', function(e) {
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmar-senha').value;
  
    if (senha !== confirmarSenha) {
      e.preventDefault();
      alert("As senhas não coincidem. Por favor, tente novamente.");
    }
  });
  