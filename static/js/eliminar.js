
const eliminarPrueba = () => {
    Swal.fire({
        title: "Esta seguro que desear deshabilitar el cliente?",
        text: "Se deshabilitará el cliente",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Confirmar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "Usuario deshabilitado!",
                icon: "success",
                confirmButtonText: "Ok",
                confirmButtonColor: "#3085d6",
            });
        }
    });
}