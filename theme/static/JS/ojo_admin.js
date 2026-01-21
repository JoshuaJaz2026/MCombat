document.addEventListener("DOMContentLoaded", function() {
    // Buscamos el campo de contraseña
    let passwordInput = document.querySelector('input[type="password"]');
    
    if (passwordInput) {
        // 1. Preparamos el contenedor padre
        let parent = passwordInput.parentElement;
        parent.style.position = "relative";

        // 2. Creamos el ícono del ojo
        let eyeIcon = document.createElement('i');
        eyeIcon.className = "fas fa-eye"; // FontAwesome ya viene con Jazzmin
        
        // 3. Estilos para que quede flotando a la derecha
        eyeIcon.style.position = "absolute";
        eyeIcon.style.right = "15px";
        eyeIcon.style.top = "40px"; // Bajamos un poco para que no choque con la etiqueta
        eyeIcon.style.cursor = "pointer";
        eyeIcon.style.color = "#6c757d"; // Color gris suave
        eyeIcon.style.zIndex = "100";
        eyeIcon.setAttribute("title", "Ver contraseña");

        // 4. Función para cambiar entre texto y password
        eyeIcon.addEventListener('click', function() {
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                eyeIcon.className = "fas fa-eye-slash"; // Ojo tachado
            } else {
                passwordInput.type = "password";
                eyeIcon.className = "fas fa-eye"; // Ojo normal
            }
        });

        // 5. Agregamos el ícono al formulario
        parent.appendChild(eyeIcon);
    }
});