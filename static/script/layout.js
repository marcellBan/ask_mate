var pageMenu = document.getElementById('page-menu');
var pageMenuOpenButton = document.getElementById('page-menu-open-button');
var pageMenuCloseButton = document.getElementById('page-menu-close-button');

function closePageMenu() {
    pageMenu.classList.remove('visible');
}

function openPageMenu() {
    pageMenu.classList.add('visible');
}

pageMenuOpenButton.addEventListener('click', openPageMenu, false);
pageMenuCloseButton.addEventListener('click', closePageMenu, false);