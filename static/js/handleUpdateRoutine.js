$(document).ready(() => {

    const sessions = JSON.parse(localStorage.getItem('sessions')) || [];
    const sessionsContainer = document.getElementById('sessionsContainer');

    const load = () => {
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
                                    <a href="javascript:void(0);" class="text-black" onclick="viewSession(${index})">${session.Name}</a>
                                </h4>
                            </div>
                        </div>
                        <div class="col-xl-4 col-xxl-3 col-lg-2 col-sm-12 d-flex align-items-center">
                            <a href="/trainer/viewNewSession/${session.Id}/${clientId}" class="btn mb-3 play-button rounded me-3" onclick="viewSession(${index})">
                                <i class="las la-caret-right scale-2 me-3"></i>Visualizar
                            </a>
                            <button class="btn btn-danger btn-circle btn-sm" onclick="deleteSession(${index})" style="width: 25px; height: 25px; padding: 0;">
                                <i class="fa fa-minus" style="font-size: 14px;"></i>
                            </button>
                        </div>
                    `;
                    sessionsContainer.appendChild(sessionDiv);
            });
    };

    load();

});