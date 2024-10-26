$(document).ready( () => {
    const id = document.getElementById('sessionId').getAttribute('data-sessionId');
    const sessions = JSON.parse(localStorage.getItem('exerciseSessions'));

    const intId = parseInt(id);

    let session = sessions.find( (s) => {
        return s.Id == intId
    } )

    if (session != undefined){
        document.getElementById('name').value = session.Name;
        document.getElementById('indications').value = session.Indications;

        session.Exercises.forEach((excercise, count) => {
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
                <input type="text" class="form-control mb-2" id="exercises${count}"  name="Exercises[]" placeholder="Nombre del Ejercicio" required>

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
            container.appendChild(newExerciseDiv);
        });
    }

    console.log(session);
    
    


    // let exercisesCount = 1;

    // function addExerciseField(container, value = '', count) {
    //     const newExerciseDiv = document.createElement('div');
    //     newExerciseDiv.className = 'mb-4 exercise';
    //     newExerciseDiv.innerHTML = `
    //         <div class="d-flex justify-content-between align-items-center">
    //             <label for="exercises${count}" class="form-label">Ejercicio
    //                 <span class="text-danger">*</span>
    //             </label>
    //             ${count > 1 ? `<button type="button" class="btn btn-danger btn-circle btn-sm" onclick="removeExerciseField(this)">
    //                 <i class="fa fa-minus"></i>
    //             </button>` : ''}
    //         </div>
    //         <input type="text" class="form-control mb-2" id="exercises${count}" name="Exercises[]" placeholder="Nombre del Ejercicio" value="${value}" required>

    //         <div class="d-flex align-items-end mb-2">
    //             <div class="me-2">
    //                 <label for="reps${count}" class="form-label">Repeticiones
    //                     <span class="text-danger">*</span>
    //                 </label>
    //                 <input type="number" class="form-control" id="reps${count}" name="Repetitions[]" placeholder="Reps" required>
    //             </div>
    //             <div>
    //                 <label for="sets${count}" class="form-label">Series
    //                     <span class="text-danger">*</span>
    //                 </label>
    //                 <input type="number" class="form-control" id="sets${count}" name="Sets[]" placeholder="Sets" required>
    //             </div>
    //         </div>

    //         <label for="video${count}" class="form-label">Enlace de Video
    //             <span class="text-danger">*</span>
    //         </label>
    //         <input type="url" class="form-control mb-3" id="video${count}" name="VideoLinks[]" placeholder="Enlace del Video" required>
    //     `;
    //     container.appendChild(newExerciseDiv);
    // }
    
} )