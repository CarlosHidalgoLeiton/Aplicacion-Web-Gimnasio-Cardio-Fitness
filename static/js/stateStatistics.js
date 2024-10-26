
const disableStatistics = (event) => {

    const statisticsID = event.currentTarget.getAttribute('data-id');
    

    Swal.fire({
        title: "¿Esta seguro?",
        text: "Se deshabilitará la estadística.",
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
                    statisticsID: statisticsID,
                }),
                url: "/trainer/statisticsClient/disable",
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
                            text: "Las estadísticas ha sido deshabilitado correctamente.",
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


const ableStatistics = (event) => {

    const statisticsID = event.currentTarget.getAttribute('data-id');
    

    Swal.fire({
        title: "¿Esta seguro?",
        text: "Se habilitará la estadística.",
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
                    statisticsID: statisticsID,
                }),
                url: "/trainer/statisticsClient/able",
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
                            text: "Las estadísticas ha sido habilitado correctamente.",
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