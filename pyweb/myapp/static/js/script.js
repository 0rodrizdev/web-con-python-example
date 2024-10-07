// Espera a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function() {
    // Ocultar el preloader al finalizar la carga
    const preloader = document.getElementById('preloader');
    preloader.style.transition = 'opacity 0.5s ease'; // Transición para ocultar
    preloader.style.opacity = 0; // Hacer el preloader transparente

    setTimeout(() => {
        preloader.style.display = 'none'; // Ocultar completamente
    }, 500); // Esperar medio segundo para el efecto

    // Desplazamiento suave al hacer clic en los enlaces de la barra de navegación
    const navLinks = document.querySelectorAll('nav a');

    navLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevenir el comportamiento predeterminado del enlace
            const targetId = this.getAttribute('href').substring(1); // Obtener el ID del destino
            const targetElement = document.getElementById(targetId); // Obtener el elemento destino

            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Mostrar un mensaje de alerta al hacer clic en los divs de texto
    const textDivs = document.querySelectorAll('.text-div');

    textDivs.forEach(div => {
        div.addEventListener('click', function() {
            alert('¡Has hecho clic en un div de texto!');
        });
    });

    // Animación al cargar la imagen en el contenedor
    const imageContainer = document.querySelector('.image-container');
    imageContainer.style.opacity = 0; // Inicialmente oculto
    setTimeout(() => {
        imageContainer.style.transition = 'opacity 1s'; // Añadir transición
        imageContainer.style.opacity = 1; // Hacerlo visible
    }, 500); // Esperar medio segundo antes de mostrar
});
