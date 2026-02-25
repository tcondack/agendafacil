function toggleMenu() {
    const menu = document.getElementById('menu');
    if (menu.style.display === 'block') {
        menu.style.display = 'none';
    } else {
        menu.style.display = 'block';
    }
}       
document.addEventListener('click', function(event){
    const menu = document.getElementById('menu');
    const menuButton = document.querySelector('.menu-button');
    if (menu && menuButton && !menu.contains(event.target) && !menuButton.contains(event.target)){
        menu.style.display = 'none'
    }
})
function validarSenha() {
    let Senha = document.getElementById('Senha');
    let SenhaC = document.getElementById('SenhaC');
  
    if (Senha.value != SenhaC.value) {
        SenhaC.setCustomValidity("Senhas diferentes!");
        SenhaC.reportValidity();
        return false;
      } else {
        SenhaC.setCustomValidity("");
        return true;
      }    
  }


document.addEventListener("DOMContentLoaded", function () {
    // Máscaras automáticas
    const mascaras = {
        'id_CPF':      v => v.replace(/\D/g,'').replace(/(\d{3})(\d)/,'$1.$2').replace(/(\d{3})(\d)/,'$1.$2').replace(/(\d{3})(\d{1,2})$/,'$1-$2'),
        'id_telefone': v => v.replace(/\D/g,'').replace(/^(\d{2})(\d)/,'($1) $2').replace(/(\d{5})(\d)/,'$1-$2'),
        'id_cep':      v => v.replace(/\D/g,'').replace(/(\d{5})(\d)/,'$1-$2'),
    };

    Object.entries(mascaras).forEach(([id, fn]) => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('input', function () { this.value = fn(this.value); });
    });




    const cepInput = document.getElementById("id_cep");
    const form = document.querySelector("form");

    if (!cepInput || !form) return;

    // 🚫 NUNCA deixa ENTER enviar o form enquanto estiver no CEP
    cepInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            e.preventDefault();
            buscarCEP();
        }
    });

    // 🔎 Busca automaticamente quando completar 8 números
    cepInput.addEventListener("input", function () {

        let cep = cepInput.value.replace(/\D/g, '');

        if (cep.length === 8) {
            buscarCEP();
        }
    });

    // 🚫 Segurança extra — impede submit acidental
    form.addEventListener("submit", function (e) {

        const logradouro = document.getElementById("id_logradouro").value;

        // se digitou CEP mas não buscou ainda
        if (cepInput.value && !logradouro) {
            e.preventDefault();
            buscarCEP();
            alert("Aguarde o preenchimento do endereço antes de salvar.");
        }
    });

});


function buscarCEP() {

    const cep = document.getElementById("id_cep").value.replace(/\D/g, '');

    if (cep.length !== 8) return;

    fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(response => response.json())
        .then(data => {

            if (data.erro) {
                alert("CEP não encontrado");
                return;
            }

            document.getElementById("id_logradouro").value = data.logradouro;
            document.getElementById("id_bairro").value = data.bairro;
            document.getElementById("id_cidade").value = data.localidade;
            document.getElementById("id_estado").value = data.uf;

            document.getElementById("id_numero").focus();
        })
        .catch(() => alert("Erro ao buscar CEP"));
}
// Fecha alertas ao clicar neles
document.querySelectorAll('.alert').forEach(el => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', () => el.style.display = 'none');
    });
