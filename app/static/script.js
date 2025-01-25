/* Script pour gérer les accordéons de tâches */
document.addEventListener("DOMContentLoaded", function() {
    const accordions = document.querySelectorAll('.accordion-header')

    accordions.forEach(accordion => {
        accordion.addEventListener('click', function() {
            const content = this.nextElementSibling

            const isActive = content.style.display === 'block'
            
            if (!isActive) {
                content.style.display = 'block'
            } else {
                content.style.display = 'none'
            }
        })
    })
})

document.querySelectorAll('.accordion-header').forEach(header => {
    header.addEventListener('click', function() {
        const item = header.parentElement;
        item.classList.toggle('open');
    });
});

/* Script pour la validation des données des formulaires de connexion et d'inscription */
document.querySelector('form').addEventListener('submit', function(event) {
    const username = document.querySelector('input[name="username"]')
    const password = document.querySelector('input[name="password"]')

    if (username.value.length < 3 || username.value.length > 20) {
        alert("Le nom d'utilisateur doit comporter entre 3 et 20 caractères.")
        event.preventDefault()
    }

    if (password.value.length < 10) {
        alert("Le mot de passe doit contenir au moins 10 caractères.")
        event.preventDefault()
    }
})