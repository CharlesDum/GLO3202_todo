/* Scripts pour gérer les accordéons */
document.addEventListener("DOMContentLoaded", function () {
    const accordions = document.querySelectorAll(".accordion-item")
    const ACCORDION_STATE_KEY = "openAccordions"

    // Charger l'état des accordéons depuis le localStorage
    function loadAccordionState() {
        const savedState = localStorage.getItem(ACCORDION_STATE_KEY)
        return savedState ? JSON.parse(savedState) : []
    }

    // Sauvegarder l'état des accordéons dans le localStorage
    function saveAccordionState(openIndexes) {
        localStorage.setItem(ACCORDION_STATE_KEY, JSON.stringify(openIndexes))
    }

    // Mettre à jour l'affichage des accordéons en fonction de l'état sauvegardé
    function updateAccordionDisplay() {
        const openIndexes = loadAccordionState()

        accordions.forEach((accordion, index) => {
            const content = accordion.querySelector(".accordion-content")
            if (openIndexes.includes(index)) {
                content.style.display = "block"
                accordion.classList.add("open")
            } else {
                content.style.display = "none"
                accordion.classList.remove("open")
            }
        })
    }

    // Initialiser l'état des accordéons
    updateAccordionDisplay()

    // Ajouter des écouteurs d'événements pour gérer les clics sur les en-têtes
    accordions.forEach((accordion, index) => {
        const header = accordion.querySelector(".accordion-header")
        const content = accordion.querySelector(".accordion-content")

        header.addEventListener("click", function () {
            const openIndexes = loadAccordionState()
            const isActive = content.style.display === "block"

            if (isActive) {
                content.style.display = "none";
                accordion.classList.remove("open")
                const newIndexes = openIndexes.filter((i) => i !== index)
                saveAccordionState(newIndexes)
            } else {
                content.style.display = "block"
                accordion.classList.add("open")
                if (!openIndexes.includes(index)) {
                    openIndexes.push(index)
                }
                saveAccordionState(openIndexes)
            }
        })
    })
})

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

/* Script pour la gestion des boutons de validation des modifications
   pour les listes et leurs tâches */
document.addEventListener('DOMContentLoaded', () => {
    // Activer/désactiver le bouton Mettre à jour pour les tâches
    document.querySelectorAll('.task-form').forEach(form => {
        const descriptionInput = form.querySelector('input[name="description"]')
        const checkbox = form.querySelector('input[name="completed"]')
        const updateButton = form.querySelector('.update-button')

        const checkIfChanged = () => {
            const originalDescription = descriptionInput.getAttribute('data-original-value')
            const originalCompleted = checkbox.getAttribute('data-original-value')

            const descriptionChanged = descriptionInput.value.trim() !== originalDescription.trim()
            const completedChanged = checkbox.checked ? 'checked' !== originalCompleted : '' !== originalCompleted

            const hasChanges = descriptionChanged || completedChanged
            updateButton.disabled = !hasChanges
            updateButton.classList.toggle('hidden', !hasChanges)
        }

        descriptionInput.addEventListener('input', checkIfChanged)
        checkbox.addEventListener('change', checkIfChanged)

        checkIfChanged()
    })

    // Activer/désactiver le bouton Modifier le nom pour les listes
    document.querySelectorAll('.list-form').forEach(form => {
        const input = form.querySelector('input[name="name"]')
        const updateButton = form.querySelector('.update-button')

        const checkIfChanged = () => {
            const originalValue = input.getAttribute('data-original-value')

            const nameChanged = input.value.trim() !== originalValue.trim()

            updateButton.disabled = !nameChanged
            updateButton.classList.toggle('hidden', !nameChanged)
        }

        input.addEventListener('input', checkIfChanged)

        checkIfChanged()
    })
})