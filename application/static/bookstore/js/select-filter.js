// handler form-selector block
const filtersSticky = document.querySelector('.form-select'),
    url = window.location.href;

filtersSticky.onchange = (event) => {
    if (url.includes('sort') && url.includes('?')) {
        window.location.href = `${url.split('sort')[0]}sort_${filtersSticky.value}`;
    } else if (url.includes('sort')) {
        window.location.href = `${url.split('sort')[0]}sort_${filtersSticky.value}`;
    } else if (url.includes('?')) {
        window.location.href = `${url.split('?')[0]}sort_${filtersSticky.value}`
    } else {
        window.location.href = `${window.location.href}sort_${filtersSticky.value}`;
    };
};
// the end of handler block

// form-selector init block
if (window.location.href.includes('sort') && window.location.href.includes('?')) {
    filtersSticky.value = window.location.href.split('?')[0].split('sort')[1].slice(1, -1);
} else if (window.location.href.includes('sort')) {
    filtersSticky.value = window.location.href.split('sort')[1].slice(1, -1);
};
// the end of form-selector init block