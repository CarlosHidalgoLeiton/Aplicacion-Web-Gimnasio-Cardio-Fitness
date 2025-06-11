
const disableClient = (event) => {

    const clientId = event.currentTarget.getAttribute('data-id');
    

    Swal.fire({
        title: "¿Esta seguro?",
        text: "Se deshabilitará el cliente con la cédula '" + clientId + "'.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Si, deshabilitar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                data: JSON.stringify({
                    clientId: clientId,
                }),
                url: "/admin/clientes/deshabilitar",
                type: "POST",
                dataType: "json",
                contentType: "application/json",
                success: function (response) {
                    if (response.error) {
                        Swal.fire({
                            icon: "error",
                            title: "¡Uy ha Ocurrido un Error!",
                            text: response.error,
                        }).then((result) => {
                            if (result.isConfirmed) {

                            }

                        });
                    } else {
                        Swal.fire({
                            icon: "success",
                            title: "¡Exito!",
                            text: "El cliente ha sido deshabilitado correctamente.",
                            confirmButtonColor: 'green',
                        }).then((result) => {
                            if (result.isConfirmed) {
                            }
                            location.reload()
                        });
                    }
                },
                error: function (xhr, status, error) {
                    console.log("Error: ", error);
                    console.log("Mensaje de error: ", xhr.responseJSON.error);
                },
            });
        }
    });
}


const ableClient = (event) => {

    const clientId = event.currentTarget.getAttribute('data-id');
    

    Swal.fire({
        title: "¿Esta seguro?",
        text: "Se habilitará el cliente con la cédula '" + clientId + "'.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Si, habilitar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                data: JSON.stringify({
                    clientId: clientId,
                }),
                url: "/admin/clientes/habilitar",
                type: "POST",
                dataType: "json",
                contentType: "application/json",
                success: function (response) {
                    if (response.error) {
                        Swal.fire({
                            icon: "error",
                            title: "¡Uy ha Ocurrido un Error!",
                            text: response.error,
                        }).then((result) => {
                            if (result.isConfirmed) {

                            }

                        });
                    } else {
                        Swal.fire({
                            icon: "success",
                            title: "¡Exito!",
                            text: "El cliente ha sido habilitado correctamente.",
                            confirmButtonColor: 'green',
                        }).then((result) => {
                            if (result.isConfirmed) {
                            }
                            location.reload()
                        });
                    }
                },
                error: function (xhr, status, error) {
                    console.log("Error: ", error);
                    console.log("Mensaje de error: ", xhr.responseJSON.error);
                },
            });
        }
    });
}