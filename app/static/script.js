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