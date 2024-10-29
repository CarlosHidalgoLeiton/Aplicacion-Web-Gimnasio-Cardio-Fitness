const clientId = parseInt(document.getElementById('data').getAttribute('data-client'));
const routineId = parseInt(document.getElementById('data').getAttribute('data-routine'));

const sessionsContainer = document.getElementById('sessionsContainer');

// Función para renderizar las sesiones
const renderSessions = (sessions) => {
    sessionsContainer.innerHTML = '';
    sessions.forEach((session, index) => {
        const sessionDiv = document.createElement('div');
        sessionDiv.className = 'd-flex border-bottom flex-wrap pt-3 list-row align-items-center mb-2 px-3';
        sessionDiv.innerHTML = `
            <div class="col-xl-8 col-xxl-9 col-lg-10 col-sm-12 d-flex align-items-center">
                <div class="list-icon bgl-primary me-3 mb-3">
                    <p class="fs-24 text-primary mb-0 mt-2">${index + 1}</p>
                    <span class="fs-14 text-primary">Sec</span>
                </div>
                <div class="info mb-3">
                    <h4 class="fs-20 ">
                        <a href="javascript:void(0);" class="text-black" onclick="viewSession(event,${index})">${session.Name}</a>
                    </h4>
                </div>
            </div>
            <div class="col-xl-4 col-xxl-3 col-lg-2 col-sm-12 d-flex align-items-center">
                <a href="/trainer/viewUpdateSession/${session.Session_ID}/${clientId}?routineId=${routineId}" class="btn mb-3 play-button rounded me-3" onclick="loadIndications(event)">
                    <i class="las la-caret-right scale-2 me-3"></i>Visualizar
                </a>
                <button class="btn btn-danger btn-circle btn-sm" onclick='deleteSession(event, ${index})' style="width: 25px; height: 25px; padding: 0;">
                    <i class="fa fa-minus" style="font-size: 14px;"></i>
                </button>
            </div>
        `;
        sessionsContainer.appendChild(sessionDiv);
    });
}

// Función para eliminar sesión
const deleteSession = (event, index) => {
    event.preventDefault();
    sessions = JSON.parse(localStorage.getItem('sessions'));
    sessionsToDelete = JSON.parse(localStorage.getItem('sessionsToDelete')) || [];

    const session = sessions[index];

    if (!session.hasOwnProperty('insert')) {
        const idsessionDelete = session.Session_ID;

        if (!sessionsToDelete.includes(idsessionDelete)) {
            sessionsToDelete.push(idsessionDelete);
        }

        localStorage.setItem('sessionsToDelete', JSON.stringify(sessionsToDelete));
    }

    sessions.splice(index, 1);

    localStorage.setItem('sessions', JSON.stringify(sessions));

    renderSessions(sessions);
};

// Cargar y mantener las indicaciones
$(document).ready(() => {
    const routineId = $("#data").data("routine");

    let sessions = JSON.parse(localStorage.getItem('sessions'));

    if (sessions == null) {
        $.ajax({
            url: `/trainer/getSession/${routineId}`,
            type: "GET",
            dataType: "json",
            contentType: "application/json",
            success: function (response) {
                if (response.error) {
                    Swal.fire({
                        icon: "error",
                        title: "¡Uy ha Ocurrido un Error!",
                        text: response.error,
                    });
                } else {
                    const responseUpdated = response.map((e) => {
                        const exercises = JSON.parse(e.Exercises);
                        return {
                            ...e,
                            Exercises: exercises
                        };
                    });

                    sessions = responseUpdated;
                    renderSessions(sessions, sessionsContainer, clientId);
                    localStorage.setItem('sessions', JSON.stringify(sessions));
                }
            },
            error: function (xhr, status, error) {
                console.log("Error: ", error);
                console.log("Mensaje de error: ", xhr.responseJSON.error);
            },
        });
    } else {
        renderSessions(sessions, sessionsContainer, clientId);
    }

    // Almacenar las indicaciones en localStorage cuando se cambian
    document.getElementById('Indications').addEventListener('input', (event) => {
        localStorage.setItem('routineIndications', event.target.value);
    });

    // Cargar las indicaciones guardadas o el valor original
    const storedIndications = localStorage.getItem('routineIndications');
    const indications = document.getElementById('data').getAttribute('data-indications');
    document.getElementById('Indications').value = storedIndications || indications || "";

    // Remover indicaciones de localStorage al enviar el formulario
    document.querySelector('form').onsubmit = function () {
        const sessionsToSend = JSON.parse(localStorage.getItem('sessions'));
        const deleteToSend = JSON.parse(localStorage.getItem('sessionsToDelete'));

        const sessionsInput = document.createElement('input');
        sessionsInput.type = 'hidden';
        sessionsInput.name = 'sessions';
        sessionsInput.value = JSON.stringify(sessionsToSend);
        this.appendChild(sessionsInput);

        const deleteInput = document.createElement('input');
        deleteInput.type = 'hidden';
        deleteInput.name = 'delete';
        deleteInput.value = JSON.stringify(deleteToSend);
        this.appendChild(deleteInput);

        // Limpiar las indicaciones del localStorage después de enviar
        localStorage.removeItem('routineIndications');
    };


    // Función para limpiar localStorage al cancelar
    const clearLocalStorage = () => {
        localStorage.removeItem('sessions');
        localStorage.removeItem('sessionsToDelete');
        localStorage.removeItem('routineIndications');
    };

});
