document.addEventListener("DOMContentLoaded", function () {
    console.log("script.js cargado correctamente");

    // Selecciona todos los inputs numéricos en la página
    const inputsNumericos = document.querySelectorAll("input[type='number']");

    inputsNumericos.forEach(input => {
        input.addEventListener("keydown", function (event) {
            if (event.key.toLowerCase() === "e") {
                event.preventDefault();
                console.log(`Se bloqueó la tecla 'e' en el campo ${input.id}`);
            }
        });
    });
});