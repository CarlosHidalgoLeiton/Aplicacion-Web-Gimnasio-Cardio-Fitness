
const disableProduct = (event) => {

    const ProductId = event.currentTarget.getAttribute('data-id');
    const ProductName = event.currentTarget.getAttribute('data-name')

    Swal.fire({
        title: "¿Esta seguro?",
        text: "Se deshabilitará el producto: '" + ProductName + "'.",
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
                    ProductId: ProductId,
                }),
                url: "/admin/inventory/view/disable",
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
                            text: "El producto ha sido deshabilitado correctamente.",
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


const ableProduct = (event) => {

    const ProductId = event.currentTarget.getAttribute('data-id');
    const ProductName = event.currentTarget.getAttribute('data-name')
    

    Swal.fire({
        title: "¿Esta seguro?",
        text: "Se habilitará el producto '" + ProductName+ "'.",
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
                    ProductId: ProductId,
                }),
                url: "/admin/inventory/view/able",
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
                            text: "El producto ha sido habilitado correctamente.",
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