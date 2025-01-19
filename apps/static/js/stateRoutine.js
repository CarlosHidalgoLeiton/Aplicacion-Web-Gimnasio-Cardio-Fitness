
const disableRoutine = (event) => {

    const routineID = event.currentTarget.getAttribute('data-id');
    

    Swal.fire({
        title: "¿Esta seguro?",
        text: "Se deshabilitará la siguiente rutina .",
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
                    routineID: routineID,
                }),
                url: "/trainer/client/routineClient/disable",
                type: "POST",
                dataType: "json",
                contentType: "application/json",
                success: function (response) {
                    if (response.error) {
                        Swal.fire({
                            icon: "error",
                            title: "¡Uy ha ocurrido un Error!",
                            text: response.error,
                        }).then((result) => {
                            if (result.isConfirmed) {

                            }

                        });
                    } else {
                        Swal.fire({
                            icon: "success",
                            title: "¡Exito!",
                            text: "La rutina ha sido deshabilitado correctamente.",
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


const ableRoutine = (event) => {

    const routineID = event.currentTarget.getAttribute('data-id');
    

    Swal.fire({
        title: "¿Esta seguro?",
        text: "Se habilitará la siguiente rutina.",
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
                    routineID: routineID,
                }),
                url: "/trainer/client/routineClient/able",
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
                            text: "La rutina ha sido habilitado correctamente.",
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