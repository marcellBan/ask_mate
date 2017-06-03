var pageMenu = document.getElementById('page-menu');
var pageMenuOpenButton = document.getElementById('page-menu-open-button');
var pageMenuCloseButton = document.getElementById('page-menu-close-button');
var sideNavShadow = document.getElementById('side-nav-shadow');

function togglePageMenu() {
    pageMenu.classList.toggle('visible');
    sideNavShadow.classList.toggle('visible');
}

pageMenuOpenButton.addEventListener('click', togglePageMenu, false);
pageMenuCloseButton.addEventListener('click', togglePageMenu, false);