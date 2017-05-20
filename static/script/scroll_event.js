var toTop = document.getElementById('to-top');

var scrollEvent = function() {
    if(window.scrollY > window.innerHeight * 1.65) {
    toTop.classList.add('visible');
    }else{
    toTop.classList.remove('visible');
    }
};

window.addEventListener('scroll', scrollEvent);