const removeExerciseField = (button) => {
    const exerciseDiv = button.closest('.exercise');
    exerciseDiv.remove();
}

$(document).ready(() => {

    let count = 1;

    const id = document.getElementById('sessionId').getAttribute('data-sessionId');
    const clientId = document.getElementById('clientId').getAttribute('data-clientId');
    const sessions = JSON.parse(localStorage.getItem('exerciseSessions'));
    const exercisesContainer = document.getElementById('exercisesContainer');

    const loadData = () => {

        const intId = parseInt(id);

        let session = sessions.find((s) => {
            return s.Id == intId
        })

        if (session != undefined) {
            document.getElementById('name').value = session.Name;
            document.getElementById('indications').value = session.Indications;

            session.Exercises.forEach((excercise) => {
                const newExerciseDiv = document.createElement('div');
                newExerciseDiv.className = 'mb-4 exercise';
                newExerciseDiv.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <label for="exercises${count}" class="form-label">Ejercicio
                        <span class="text-danger">*</span>
                    </label>
                    ${count > 1 ? `<button type="button" class="btn btn-danger btn-circle btn-sm" onclick="removeExerciseField(this)">
                        <i class="fa fa-minus"></i>
                    </button>` : ''}
                </div>
                <input type="text" class="form-control mb-2" id="exercises${count}" value="${excercise.nombre}"  name="Exercises[]" placeholder="Nombre del Ejercicio" required>
                <div class="invalid-feedback">
                    Por favor ingresar el nombre del ejercicio
                </div>
                <div class="d-flex align-items-end mb-2">
                    <div class="me-2">
                        <label for="reps${count}" class="form-label">Repeticiones
                            <span class="text-danger">*</span>
                        </label>
                        <input type="number" class="form-control" id="reps${count}" value="${excercise.repeticiones}" name="Repetitions[]" placeholder="Reps" required>
                        <div class="invalid-feedback">
                            Por favor ingresar las repeticiones
                        </div>
                        </div>
                    <div>
                        <label for="sets${count}" class="form-label">Series
                            <span class="text-danger">*</span>
                        </label>
                        <input type="number" class="form-control" id="sets${count}" value="${excercise.series}" name="Sets[]" placeholder="Sets" required>
                        <div class="invalid-feedback">
                            Por favor ingresar las series
                        </div>
                    </div>
                </div>

                <label for="video${count}" class="form-label">Enlace de Video
                </label>
                <input type="url" class="form-control mb-3" id="video${count}" value="${excercise.Link}" name="VideoLinks[]" placeholder="Enlace del Video">
            `;
                exercisesContainer.appendChild(newExerciseDiv);

                count++;
            });
        }

    }

    document.getElementById('addEjercicioBtn').addEventListener('click', function () {
        count++;
        addExerciseField(count);
    });

    document.getElementById('exerciseForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const form = event.target;
        if (!form.checkValidity()) {
            form.classList.add('was-validated'); // Añade estilos de validación de Bootstrap
            return; // Si algún campo no es válido, no se guarda la sesión
        }

        const name = document.getElementById('name').value;
        const indications = document.getElementById('indications').value;

        // Crear un array de objetos para los ejercicios
        const exercises = Array.from(document.querySelectorAll('.exercise')).map((exerciseDiv, index) => {
            const exerciseName = exerciseDiv.querySelector(`input[name="Exercises[]"]`).value;
            const reps = exerciseDiv.querySelector(`input[name="Repetitions[]"]`).value;
            const sets = exerciseDiv.querySelector(`input[name="Sets[]"]`).value;
            const videoLink = exerciseDiv.querySelector(`input[name="VideoLinks[]"]`).value;

            return {
                nombre: exerciseName,
                repeticiones: reps,
                series: sets,
                Link: videoLink
            };
        });

        const updatedSession = {
            Id: parseInt(id),
            Name: name,
            Indications: indications,
            Exercises: exercises
        };

        updatedSessions = sessions.map((s) => {
            if (parseInt(s.Id) === parseInt(id)) {
                return updatedSession; // Reemplaza con la nueva sesión
            }
            return s; // Devuelve la sesión original
        });

        // Guardar el nuevo arreglo en local storage
        localStorage.setItem('exerciseSessions', JSON.stringify(updatedSessions));

        // Limpiar el formulario después de guardar
        document.getElementById('exerciseForm').reset();
        exercisesCount = 1; // Reiniciar el contador de ejercicios
        exercisesContainer.innerHTML = ''; // Limpiar el contenedor de ejercicios

        // Redirigir a la página de rutinas del cliente después de guardar
        window.location.href = `/trainer/client/routineClient/${clientId}`;
    });

    function addExerciseField(count) {
        const newExerciseDiv = document.createElement('div');
        newExerciseDiv.className = 'mb-4 exercise';
        newExerciseDiv.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <label for="exercises${count}" class="form-label">Ejercicio
                    <span class="text-danger">*</span>
                </label>
                ${count > 1 ? `<button type="button" class="btn btn-danger btn-circle btn-sm" onclick="removeExerciseField(this)">
                    <i class="fa fa-minus"></i>
                </button>` : ''}
            </div>
            <input type="text" class="form-control mb-2" id="exercises${count}" name="Exercises[]" placeholder="Nombre del Ejercicio" required>

            <div class="d-flex align-items-end mb-2">
                <div class="me-2">
                    <label for="reps${count}" class="form-label">Repeticiones
                        <span class="text-danger">*</span>
                    </label>
                    <input type="number" class="form-control" id="reps${count}" name="Repetitions[]" placeholder="Reps" required>
                </div>
                <div>
                    <label for="sets${count}" class="form-label">Series
                        <span class="text-danger">*</span>
                    </label>
                    <input type="number" class="form-control" id="sets${count}" name="Sets[]" placeholder="Sets" required>
                </div>
            </div>

            <label for="video${count}" class="form-label">Enlace de Video
                <span class="text-danger">*</span>
            </label>
            <input type="url" class="form-control mb-3" id="video${count}" name="VideoLinks[]" placeholder="Enlace del Video" required>
        `;

        exercisesContainer.appendChild(newExerciseDiv);
    }



    loadData();
});