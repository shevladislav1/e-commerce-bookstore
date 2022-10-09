const buttonsBuy = document.querySelectorAll('.add-to-cart');

buttonsBuy.forEach((button) => {
	button.addEventListener('click', (event) => {
		const request = new XMLHttpRequest();
		const currentURL = window.location.href;

		if (currentURL.includes('?')) {
			request.open('GET', `${currentURL}&add-to-cart=${button.value}`);
		} else {
			request.open('GET', `${currentURL}?add-to-cart=${button.value}`);
		};

		request.send();

		request.addEventListener('readystatechange', () => {
			if (request.readyState === 4 && request.status === 200) {
				const bookList = JSON.parse(request.response);

				const outputHTML = getOutputHTML(bookList);

				const cartWrapper = document.getElementById('cartWrapper');
				cartWrapper.innerHTML = outputHTML;
				const myModalCart = new bootstrap.Modal('#CartModal');
				myModalCart.show();

				const deleteFromCartButtons = document.querySelectorAll('.deleteFromCart');
				deleteFromCartButtons.forEach((item) => {
					item.addEventListener('click', (event) => {
						const cardBook = document.getElementById(`divCard${item.id}`);
						cardBook.remove();

						const request = new XMLHttpRequest();
						const currentURL = window.location.href;

						if (currentURL.includes('?')) {
							request.open('GET', `${currentURL}&deleteFromCart=${item.id}`);
						} else {
							request.open('GET', `${currentURL}?deleteFromCart=${item.id}`);
						};

						request.send();
					});
				});

				const inputQuantityInteger = document.querySelectorAll('.inputQuantityInteger');
				inputQuantityInteger.forEach((item) => {
					item.addEventListener('input', () => {

						if (!item.value) {
							// do nothing
						} else {
							changeQuantityByInput(item.name, item.value);
						};
					});
				});
			};
		});
	});
});


function plusOne(book_pk) {
	const quantityOfProduct = document.getElementById(`quantityOfProduct${book_pk}`);
	quantityOfProduct.value = +quantityOfProduct.value + 1;
	changeQuantity(book_pk, 'plus');
};

function minusOne(book_pk) {
	const quantityOfProduct = document.getElementById(`quantityOfProduct${book_pk}`);

	if (quantityOfProduct.value == 1) {
		// do nothing
	} else {
		quantityOfProduct.value = +quantityOfProduct.value - 1;
		changeQuantity(book_pk, 'minus');
	};
};

function changeQuantity(book_pk, unit) {
	const request = new XMLHttpRequest();
	const currentURL = window.location.href;

	request.open('GET', currentURL);

	if (currentURL.includes('?')) {
		request.open('GET', `${currentURL}&changeQuantity=${unit}:${book_pk}`);
	} else {
		request.open('GET', `${window.location.href}?changeQuantity=${unit}:${book_pk}`);
	};

	request.send();
};

function changeQuantityByInput(book_pk, quantity) {
	const request = new XMLHttpRequest();
	const currentURL = window.location.href;

	if (currentURL.includes('?')) {
		request.open('GET', `${currentURL}&changeQuantityByInput=${book_pk}:${quantity}`);
	} else {
		request.open('GET', `${currentURL}?changeQuantity=${quantity}:${book_pk}`);
	};

	request.send();
};


const deleteFromCartButtons = document.querySelectorAll('.deleteFromCart');
deleteFromCartButtons.forEach((item) => {
	item.addEventListener('click', (event) => {
		const cardBook = document.getElementById(`divCard${item.id}`);
		cardBook.remove();

		const request = new XMLHttpRequest();
		const currentURL = window.location.href;

		if (currentURL.includes('?')) {
			request.open('GET', `${currentURL}&deleteFromCart=${item.id}`);
		} else {
			request.open('GET', `${currentURL}?deleteFromCart=${item.id}`);
		};

		request.send();
	});
});

const inputQuantityInteger = document.querySelectorAll('.inputQuantityInteger');
inputQuantityInteger.forEach((item) => {
	item.addEventListener('input', () => {

		if (!item.value) {
			// do nothing
		} else {
			changeQuantityByInput(item.name, item.value);
		};
	});
});

const addToCartOnDetailPage = document.querySelector('.addToCartOnDetailPage');

addToCartOnDetailPage.addEventListener('click', (event) => {
	const request = new XMLHttpRequest();
	const currentURL = window.location.href;

	if (currentURL.includes('?')) {
		request.open('GET', `${currentURL}&add-to-cart=${addToCartOnDetailPage.id}`);
	} else {
		request.open('GET', `${currentURL}?add-to-cart=${addToCartOnDetailPage.id}`);
	};

	request.send();

	request.addEventListener('readystatechange', () => {
		if (request.readyState === 4 && request.status === 200) {
			const bookList = JSON.parse(request.response);

			const outputHTML = getOutputHTML(bookList);

			const cartWrapper = document.getElementById('cartWrapper');
			cartWrapper.innerHTML = outputHTML;
			const myModalCart = new bootstrap.Modal('#CartModal');
			myModalCart.show();

			const deleteFromCartButtons = document.querySelectorAll('.deleteFromCart');
			deleteFromCartButtons.forEach((item) => {
				item.addEventListener('click', (event) => {
					const cardBook = document.getElementById(`divCard${item.id}`);
					cardBook.remove();

					const request = new XMLHttpRequest();
					const currentURL = window.location.href;

					if (currentURL.includes('?')) {
						request.open('GET', `${currentURL}&deleteFromCart=${item.id}`);
					} else {
						request.open('GET', `${currentURL}?deleteFromCart=${item.id}`);
					};

					request.send();
				});
			});
		};
	});
});


function getOutputHTML(bookList) {
	outputHTML = `
<div class="modal fade" id="CartModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
        <div class="modal-content">
            <div class="modal-header">

                <h5 class="modal-title" id="exampleModalLabel">Корзина</h5>

                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">

                <section class="h-100" style="background-color: #eee;">
                    <div class="container h-100 py-5">
                        <div class="row d-flex justify-content-center align-items-center h-100">
                            <div class="col-10">`;


	for (let bookPK in bookList['book_list']) {
		const current_book = bookList['book_list'][bookPK];

		outputHTML += `<div class="card rounded-3 mb-4" id="divCard${bookPK}">
                                    <div class="card-body p-4">
                                        <div class="row d-flex justify-content-between align-items-center">
                                            <div class="col-md-2 col-lg-2 col-xl-2">
                                                <img
                                                        src="${current_book['image']}"
                                                        class="img-fluid rounded-3" alt="Cotton T-shirt">
                                            </div>
                                            <div class="col-md-3 col-lg-3 col-xl-3">
                                                <p class="lead fw-normal mb-2">${current_book['title']}</p>
                                            </div>
                                            <div class="col-md-3 col-lg-3 col-xl-2 d-flex">
                                                <button id="buttonMinus${bookPK}" onclick="minusOne(${bookPK})" class="btn btn-link px-2">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                         fill="currentColor" class="bi bi-dash-lg" viewBox="0 0 16 16">
                                                        <path fill-rule="evenodd"
                                                              d="M2 8a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11A.5.5 0 0 1 2 8Z"/>
                                                    </svg>
                                            
                                                </button>

                                                <input id="quantityOfProduct${bookPK}" min="0" name="${bookPK}" value="${current_book['quantity']}" type="number"
                                                       class="inputQuantityInteger form-control form-control-sm"/>

                                                <button id="buttonPlus${bookPK}" onclick="plusOne(${bookPK})" class="btn btn-link px-2">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                         fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                                                        <path fill-rule="evenodd"
                                                              d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/>
                                                    </svg>
                                                </button>
                                            </div>
                                            <div class="col-md-3 col-lg-2 col-xl-2 offset-lg-1">
                                                <h5 class="mb-0 text-center" style="margin-top: 35px">${current_book['price']} грн</h5>
                                            </div>
                                            <div class="col-md-1 col-lg-1 col-xl-1 text-end">
                                                <div class="deleteFromCart" id="${bookPK}">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25"
                                                         fill="currentColor" 
                                                         class="bi bi-trash" viewBox="0 0 16 16">
                                                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                                                        <path fill-rule="evenodd"
                                                              d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                                                    </svg>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>`;

	};

	outputHTML += `<div class="card">
                                    <div class="card-body">
                                        <button type="button" class="btn btn-warning btn-block btn-lg">
                                        <a style="text-decoration: none; color: white"
                                        href="${window.location.origin}/checkout">Оформити
                                            замовлення</a>
                                        
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </div>
</div>`;

	return outputHTML;
};