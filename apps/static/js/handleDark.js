var ThemeModule = (function () {

    // Función para guardar el tema (oscuro o claro) en localStorage
    function setThemeVersion(version) {
        localStorage.setItem("theme-version", version);
    }

    // Función para obtener el tema (oscuro o claro) desde localStorage
    function getThemeVersion() {
        return localStorage.getItem("theme-version");
    }

    // Función para aplicar el tema a la página según el valor de localStorage
    function applyStoredTheme() {
        var themeVersion = getThemeVersion();  // Leer el tema desde localStorage
        if (themeVersion) {
            // Si existe un tema almacenado, aplicarlo al body
            jQuery("body").attr("data-theme-version", themeVersion);
            toggleIcons(themeVersion);  // Cambiar íconos según el tema
        } else {
            // Si no hay tema guardado, aplicar el claro por defecto
            jQuery("body").attr("data-theme-version", "light");
            toggleIcons("light");  // Cambiar íconos al modo claro
        }
    }

    // Función para alternar el tema al hacer clic en el botón de cambio de tema
    function toggleTheme() {
        if (jQuery(".dz-theme-mode").length > 0) {
            jQuery(".dz-theme-mode").on("click", function () {
                jQuery(this).toggleClass("active");

                // Si está activo, el tema es oscuro; si no, es claro
                if (jQuery(this).hasClass("active")) {
                    jQuery("body").attr("data-theme-version", "dark");
                    setThemeVersion("dark");  // Guardamos el tema oscuro en localStorage
                    toggleIcons("dark"); // Cambiar íconos al modo oscuro
                } else {
                    jQuery("body").attr("data-theme-version", "light");
                    setThemeVersion("light");  // Guardamos el tema claro en localStorage
                    toggleIcons("light"); // Cambiar íconos al modo claro
                }
            });
        }
    }

    // Función para cambiar los íconos de sol y luna según el tema
    function toggleIcons(theme) {
        var iconLight = jQuery("#icon-light");
        var iconDark = jQuery("#icon-dark");

        if (theme === "dark") {
            iconLight.show();  
            iconDark.hide();
        } else {
            iconLight.hide();  
            iconDark.show();   
        }
    }

    // Inicialización: aplicar el tema al cargar la página
    function init() {
        applyStoredTheme();  // Aplicar el tema guardado al cargar la página
        toggleTheme();       // Permitir alternar el tema al hacer clic
    }

    // Exponer las funciones necesarias desde el módulo
    return {
        init: init
    };

})();

// Inicializar el módulo al cargar la página
jQuery(document).ready(function () {
    ThemeModule.init();
});