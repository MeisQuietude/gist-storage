const linkPreviousPage = document.querySelector('a[data-nav="prev"]');
const linkNextPage = document.querySelector('a[data-nav="next"]');

linkNextPage.addEventListener('click', (el) => {
    const maxPage = +document.querySelector('a[data-nav="last"]').innerText;
    let curPage = getCurrentPage();
    curPage = curPage < maxPage ? curPage : maxPage - 1;
    window.location.href = `/discover/${++curPage}`
});
linkPreviousPage.addEventListener('click', (el) => {
    let curPage = getCurrentPage();
    window.location.href = `/discover/${--curPage || 1}`
});

const getCurrentPage = () => {
    const url = document.URL.split('/');
    return +url[url.length - 1] || 1;
};
