// import { errorMessage } from "./toastrConfig";

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('invoiceType').addEventListener('change', function () {
        var value = this.value;
        console.log(value);

        document.querySelectorAll('.form-container').forEach(function (el) {
            el.style.display = 'none';
            document.getElementById('formCliente').style.display = 'block';
        });
        if (value) {
            document.getElementById(value + 'Form').style.display = 'block';
        }
    });
});




