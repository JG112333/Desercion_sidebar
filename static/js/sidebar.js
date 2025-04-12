document.getElementById("sidebarToggle").addEventListener("click", function() {
    var sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("active");
  });

  // Detectar cambio de tamaño de ventana
window.addEventListener("resize", function () {
    var sidebar = document.getElementById("sidebar");
    if (window.innerWidth > 768) {
      // Si está en modo escritorio, asegurate que el sidebar esté visible
      sidebar.classList.add("active");
    }
  });