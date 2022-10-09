const likeButtons = document.querySelectorAll('.pushLike');


likeButtons.forEach((item) => {
    item.addEventListener('click', (event) => {
        const amountLikes = document.querySelector(`.amountLikes${item.id}`);

        const request = new XMLHttpRequest();
        const url = window.location.href;

        if (window.location.href.includes('?')) {
            request.open('GET', `${url}&pushlike=${item.id}`);
        } else {
            request.open('GET', `${url}?pushlike=${item.id}`);
        };

        request.send();

        request.addEventListener('readystatechange', () => {
            if (request.readyState === 4 && request.status === 200) {
                const like = JSON.parse(request.response);

                if (like['likeResult'] == 'plusOne') {
                    amountLikes.innerText = +amountLikes.innerText + 1;
                } else if (like['likeResult'] == 'minusOne') {
                    amountLikes.innerText = +amountLikes.innerText - 1;
                } else {
                    const loginModal = new bootstrap.Modal('#LoginModal');
                    loginModal.show();
                };
            };
        });
    });
});
