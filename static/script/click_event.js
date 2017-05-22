var pageMenuButton = document.getElementById('page-menu-button');
var pageMenu = document.getElementById('header-content-wrapper');
var pageMenuShadow = document.getElementById('header-content-shadow');

var togglePageMenu = function(){
    pageMenu.classList.toggle('visible');
};

pageMenuButton.addEventListener('click', togglePageMenu);
pageMenuShadow.addEventListener('click', togglePageMenu);