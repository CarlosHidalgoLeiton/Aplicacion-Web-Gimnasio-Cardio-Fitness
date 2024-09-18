(function($) {
    "use strict"

    $('#mdate').bootstrapMaterialDatePicker({
        weekStart: 0,
        time: false,
        lang: 'es',
    });
    $('#timepicker').bootstrapMaterialDatePicker({
        format: 'HH:mm',
        time: true,
        date: false,
        lang: 'es',
    });
    $('#date-format').bootstrapMaterialDatePicker({
        format: 'dddd DD MMMM YYYY - HH:mm',
        lang: 'es',
    });

    $('#min-date').bootstrapMaterialDatePicker({
        format: 'DD/MM/YYYY HH:mm',
        lang: 'es',
        minDate: new Date()
    });

})(jQuery);