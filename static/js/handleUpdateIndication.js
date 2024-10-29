const loadIndications = (event) => {
    event.preventDefault();

    let indications = document.getElementById('Indications').value;

    localStorage.setItem('updateIndications', indications);

    window.location.href = event.currentTarget.href;
}

$(document).ready( () => {

    const indications = localStorage.getItem('updateIndications') || '';

    document.getElementById('Indications').value = indications;

    console.log(localStorage.getItem('exerciseSessions'));

} )