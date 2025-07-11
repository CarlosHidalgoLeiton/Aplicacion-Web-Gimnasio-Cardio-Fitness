$(document).ready(function () {
    // Verifica si DataTable ya está inicializado y, si es así, destrúyelo
    if ($.fn.DataTable.isDataTable('#example2')) {
        $('#example2').DataTable().destroy();
    }

    // Inicializa DataTable con configuración para ocultar botones y registros
    $('#example2').DataTable({
        paging: true,          // Desactiva la paginación
        info: true,            // Oculta el conteo de registros
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.11.2/i18n/es_es.json'
        }
    });

    $('.dataTables_length').addClass('bs-select');
});