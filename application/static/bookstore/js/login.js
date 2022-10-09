const loginFormValidationAjax = function (login, password) {
    const obj = {'username': login, 'password': password}
    const body = JSON.stringify(obj)

    const request = new XMLHttpRequest();
    request.open('POST', `${window.location.href}`);
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.send(body);

    return request;
};

const loginInputs = document.querySelectorAll('.p-2'),
    buttonLogin = document.getElementById('login');


buttonLogin.addEventListener('click', function (event) {
    event.preventDefault();

    const loginInput = loginInputs[0].querySelector('.form-control');
    const PasswordInput = loginInputs[1].querySelector('.form-control');

    if (!loginInput.value || !PasswordInput.value) {
        if (!loginInput.value && !PasswordInput.value) {
            loginInput.placeholder = "Це поле є обов'язковим";
            loginInput.className = 'form-control is-invalid';
            PasswordInput.placeholder = "Це поле є обов'язковим";
            PasswordInput.className = 'form-control is-invalid';
        } else if (!PasswordInput.value) {
            PasswordInput.placeholder = "Це поле є обов'язковим";
            PasswordInput.className = 'form-control is-invalid';

            loginInput.placeholder = "";
            loginInput.className = 'form-control';
        } else {
            loginInput.placeholder = "Це поле є обов'язковим";
            loginInput.className = 'form-control is-invalid';

            PasswordInput.placeholder = "";
            PasswordInput.className = 'form-control';
        };
    } else {
        const request = loginFormValidationAjax(loginInput.value, PasswordInput.value);
        request.addEventListener("readystatechange", () => {
            if (request.readyState === 4 && request.status === 200) {
                const response = JSON.parse(request.response);
                if (response['isInvalid'] == 'true') {
                    if (response['textError'].includes('логіном')) {
                        loginInput.placeholder = response['textError'];
                        loginInput.className = 'form-control is-invalid';
                        loginInput.value = '';

                        PasswordInput.placeholder = '';
                        PasswordInput.className = 'form-control';
                    } else {
                        PasswordInput.placeholder = response['textError'];
                        PasswordInput.className = 'form-control is-invalid';
                        PasswordInput.value = '';

                        loginInput.placeholder = '';
                        loginInput.className = 'form-control';
                    };
                } else {
                    loginInput.className = 'form-control is-valid';
                    PasswordInput.className = 'form-control is-valid';
                    location.reload();
                };
            };
        });
    };
});