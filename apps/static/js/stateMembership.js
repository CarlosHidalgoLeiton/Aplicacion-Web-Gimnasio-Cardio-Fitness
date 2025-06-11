const disableMembership = (event) => {

    const membershipId = event.currentTarget.getAttribute('data-id');
    const membershipName = event.currentTarget.getAttribute('data-name');

    Swal.fire({
        title: "¿Esta seguro?",
        text: "Se deshabilitará la membresía '" + membershipName + "'.",
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
                    membershipId: membershipId,
                }),
                url: "/admin/membresias/deshabilitar",
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
                            text: "La membresía ha sido deshabilitada correctamente.",
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


const ableMembership = (event) => {

    const membershipId = event.currentTarget.getAttribute('data-id');
    const membershipName = event.currentTarget.getAttribute('data-name');

    Swal.fire({
        title: "¿Esta seguro?",
        text: "Se habilitará la membresía '" + membershipName + "'.",
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
                    membershipId: membershipId,
                }),
                url: "/admin/membresias/habilitar",
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
                            text: "La membresía ha sido habilitada correctamente.",
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