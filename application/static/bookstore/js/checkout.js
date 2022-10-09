const choiceCity = document.querySelector('.choiceCity'),
    cityList = document.querySelector('.city-list');

function closeCityGroup() {
    cityList.innerHTML = '';
    const selectWarehouses = document.querySelector('.select-warehouses');

    selectWarehouses.innerHTML = `<option value="">Виберіть місто</option>`;
}

choiceCity.addEventListener('input', (event) => {
    const arrayCity = []

    const request = new XMLHttpRequest();
    request.open('GET', `${window.location.href}?getCities=True`);
    request.send();

    request.addEventListener('readystatechange', () => {
        if (request.readyState === 4 && request.status === 200) {
            const cities = JSON.parse(request.response);

            for (key in cities['cities']) {
                if (cities['cities'].hasOwnProperty(key)) {
                    arrayCity.push((cities['cities'][key]['Description']));
                };
            };

            const valueForSearch = choiceCity.value;
            const outputCityList = [];

            arrayCity.forEach((city) => {
                if (city.toLocaleLowerCase().includes(valueForSearch.toLocaleLowerCase())) {
                    outputCityList.push(city);
                };
            });

            let cityListHTML = `<ul class="list-group mb-3">
                              <li onclick="closeCityGroup()" 
                              class="city-list-item list-group-item d-flex justify-content-between lh-condensed">
                               Закрити пошук 
                               <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                               </svg>
                               </li>`;

            outputCityList.forEach((city) => {
                cityListHTML += `<li id="${city}"
                             class="city-list-item list-group-item d-flex justify-content-between lh-condensed">
                             <div>
                                 <h6 class="my-0">${city}</h6>
                             </div>
                         </li>`;
            });

            cityListHTML += `</ul>`;
            cityList.innerHTML = cityListHTML;

            const cityListItem = document.querySelectorAll('.city-list-item');
            cityListItem.forEach((city) => {
                city.addEventListener('click', (event) => {
                    choiceCity.value = city.id;
                    closeCityGroup();


                    const request = new XMLHttpRequest();
                    request.open('GET', `${window.location.href}?getWarehouse=${city.id}`);
                    request.send();

                    request.addEventListener('readystatechange', () => {
                        if (request.readyState === 4 && request.status === 200) {
                            const warehouses = JSON.parse(request.response);

                            const arrayWarehouse = [];
                            for (key in warehouses['warehouses']) {
                                if (warehouses['warehouses'].hasOwnProperty(key)) {
                                    arrayWarehouse.push((warehouses['warehouses'][key]['Description']));
                                };
                            };

                            const selectWarehouses = document.querySelector('.select-warehouses');
                            let outputHTML = '<option value="">Виберіть відділення</option>';

                            arrayWarehouse.forEach((warehouse) => {
                                outputHTML += `<option>${warehouse}</option>`;
                            });

                            selectWarehouses.innerHTML = outputHTML;
                        };
                    });
                });
            });
        };
    });
});

const confirmOrder = document.querySelector('.confirm-order');

confirmOrder.addEventListener('click', (event) => {
    event.preventDefault();

    const firstName = document.querySelector('.first-name').value,
        lastName = document.querySelector('.last-name').value,
        emailInput = document.querySelector('.email-input').value,
        phoneInput = document.querySelector('.phoneInput').value,
        cityInput = document.querySelector('.choiceCity').value,
        warehouseInput = document.querySelector('.select-warehouses'),

        cashPay = document.querySelector('.cashPay').checked,
        onlinePay = document.querySelector('.onlinePay').checked;


    if (!firstName || !lastName || !emailInput || !phoneInput || !cityInput || !warehouseInput.value) {
        alert('Не всі поля заповнені!');
    } else {
        if (cashPay) {
            const obj = {
                'createNewOrder': 'True',
                'firstName': firstName,
                'lastName': lastName,
                'emailInput': emailInput,
                'phoneInput': phoneInput,
                'cityInput': cityInput,
                'warehouseInput': warehouseInput.value,
                'payType': 'Оплата готівкою або картою при отриманні',
            };
            const body = JSON.stringify(obj)

            const request = new XMLHttpRequest();
            request.open('POST', window.location.href);
            request.setRequestHeader('X-CSRFToken', csrftoken);
            request.send(body);

            request.addEventListener('readystatechange', () => {
                if (request.readyState === 4 && request.status === 200) {
                    const response = JSON.parse(request.response);
                    if (response['createNewOrder'] == 'true') {
                        window.location.href = `${window.location.href}application_status/`;
                    } else {
                        alert('Щось пішло не так! Спробуйте ще раз');
                    };
                };
            });
        } else {

            const obj = {
                'saveSendData': 'True',
                'firstName': firstName,
                'lastName': lastName,
                'emailInput': emailInput,
                'phoneInput': phoneInput,
                'cityInput': cityInput,
                'warehouseInput': warehouseInput.value,
                'payType': 'Оплата карткою онлайн',
            };
            const body = JSON.stringify(obj)

            const request = new XMLHttpRequest();
            request.open('POST', `${window.location.href}save-data`);
            request.setRequestHeader('X-CSRFToken', csrftoken);
            request.send(body);

            request.addEventListener('readystatechange', () => {
                if (request.readyState === 4 && request.status === 200) {
                    const response = JSON.parse(request.response);
                    if (response['success'] == 'OK!') {
                        window.location.href = `${window.location.href}pay`;
                    };
                };
            });
        };
    };
});

