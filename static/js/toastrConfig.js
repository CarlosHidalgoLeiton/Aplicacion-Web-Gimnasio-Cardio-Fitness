toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-top-center",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut",
}


const errorMessage = (message) => {
    toastr.error("Error: "+ message);
}

const successMessage = (message) => {
    toastr.success("Hecho: "+ message);
}

const infoMessage = (message) => {
    toastr.info("Información: "+ message);
}

const warningMessage = (message) => {
    toastr.warning("Advertencia: "+ message);
}