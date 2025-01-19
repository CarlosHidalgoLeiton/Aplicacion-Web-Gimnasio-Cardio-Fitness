document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('invoiceType').addEventListener('change', function () {
        var value = this.value;
        var tableBody = document.querySelector('#reportTable tbody');
        tableBody.innerHTML = '';

        if (!value) {
            alert('Por favor, seleccione un tipo de reporte válido.');
            return;
        }

        fetch('/admin/billsReports', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ invoiceType: value })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la solicitud: ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                Object.keys(data).forEach(group => {
                    var groupReports = data[group];
                    var totalMonto = 0;

                    groupReports.forEach(report => {
                        totalMonto += parseFloat(report.Monto); 
                    });

                    if (value === 'daily' && group instanceof Date) {
                        group = group.toLocaleDateString();  
                    }

                    var groupLabel = '';

                    if (value === 'mensual') {
                        groupLabel = 'Reporte del mes de ' + group; 
                    } else if (value === 'semanal') {

                        var year = group.slice(0, 4); 
                        var week = group.slice(4); 
                        groupLabel = `Reporte de la semana ${week} del ${year}`; 
                    } else if (value === 'diaria') {
                        groupLabel = 'Reporte del día ' + group; 
                    }

                    var row = document.createElement('tr');

                    
                    row.innerHTML = `
                        <td>${groupLabel}</td>
                        <td>${totalMonto.toFixed(2)}</td>
                        <td>
                            <a href="/admin/generate_report_bill?month=${group}&invoice_type=${value}" 
                               class="btn btn-danger shadow btn-xs sharp" 
                               target="_blank">
                                <i class="fa fa-download"></i>
                            </a>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error al obtener los reportes:', error);
                alert('Ocurrió un error al generar el reporte.');
            });
    });
});
