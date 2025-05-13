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
  
  // Dropdown Produzir já existente
const btn = document.getElementById('produzir-btn');
const dropdown = document.getElementById('produzir-dropdown');

btn.addEventListener('click', (e) => {
  e.preventDefault();
  dropdown.style.display = dropdown.style.display === 'flex' ? 'none' : 'flex';
});

document.addEventListener('click', function (e) {
  if (!btn.contains(e.target) && !dropdown.contains(e.target)) {
    dropdown.style.display = 'none';
  }
});

// Dropdown Perfil
const perfilBtn = document.getElementById('perfil-btn');
const perfilDropdown = document.getElementById('perfil-dropdown');

perfilBtn.addEventListener('click', (e) => {
  e.preventDefault();
  perfilDropdown.style.display = perfilDropdown.style.display === 'flex' ? 'none' : 'flex';
});

document.addEventListener('click', function (e) {
  if (!perfilBtn.contains(e.target) && !perfilDropdown.contains(e.target)) {
    perfilDropdown.style.display = 'none';
  }
});
