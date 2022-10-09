const searchButton = document.querySelectorAll('.search-button-control'),
    searchInput = document.querySelectorAll('.input-search-product');

searchButton.forEach((button) => {
    button.addEventListener('click', (event) => {
        searchInput.forEach((input) => {
            if (input.value) {
                window.location.href = `${window.location.origin}/books_by_search/${input.value}`;
            };
        });
    });
});