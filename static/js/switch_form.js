let tipoSeleccionado = localStorage.getItem("tipoSeleccionado") || "xlsx"; // Recuperar del localStorage, o usar 'xlsx' por defecto


function mostrarFormulario(tipo) {
    tipoSeleccionado = tipo;

    // Guardamos la opción seleccionada en localStorage
    localStorage.setItem("tipoSeleccionado", tipo);

    // Mostrar el formulario correspondiente
    document.getElementById('form-xlsx').classList.toggle('d-none', tipo !== 'xlsx');
    document.getElementById('form-csv').classList.toggle('d-none', tipo !== 'csv');

    // Actualizar estilos de los botones
    document.getElementById('btn-xlsx').classList.toggle('active', tipo === 'xlsx');
    document.getElementById('btn-xlsx').classList.toggle('btn-primary', tipo === 'xlsx');
    document.getElementById('btn-xlsx').classList.toggle('btn-secondary', tipo !== 'xlsx');

    document.getElementById('btn-csv').classList.toggle('active', tipo === 'csv');
    document.getElementById('btn-csv').classList.toggle('btn-primary', tipo === 'csv');
    document.getElementById('btn-csv').classList.toggle('btn-secondary', tipo !== 'csv');
}



window.onload = function () {
    // Asegurarse de que la selección y el formulario estén en su estado correcto después de recargar la página
    mostrarFormulario(tipoSeleccionado);


};





// Función para hacer scroll hacia una sección específica
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Ejecutar cuando la ventana haya cargado completamente
window.addEventListener('load', function () {
    const imgElement = document.querySelector('#gráfico-deserción img');
    const btnDescargar = document.getElementById('btn-descargar');

    if (imgElement && imgElement.src) {
        scrollToSection('gráfico-deserción');
    } else if (btnDescargar) {
        scrollToSection('btn-descargar');
    }
});