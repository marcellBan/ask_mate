var numbersWrappers = document.getElementsByClassName('numbers-wrapper');
var numbersWrapperPadding = numbersWrappers[0].children[0].offsetTop - numbersWrappers[0].offsetTop;
var headerHeight = document.getElementById('page-header').offsetHeight;

function bottom(element){
    return element.offsetTop + element.offsetHeight;
}

function resetNumbersElements(){
    let numbersElements = document.getElementsByClassName('numbers');
    for(numbers of numbersElements){
        numbers.style.top = 0;
    }
}

function numbersScroll(){
    let yPos = window.scrollY;
    for(numbersWrapper of numbersWrappers){
        let numbers = numbersWrapper.children[0];
        if(
                numbers.offsetTop < numbersWrapper.offsetTop + numbersWrapperPadding ||
                numbersWrapper.offsetTop > yPos + headerHeight
        ){
            // Set top position of numbers to 0 if it goes into numbersWrapper padding area or
            // numbers wrapper covered by the page-header.
            // Currently inefficinet since it sets for every card even if they're off-screen.
            numbers.style.top = 0;
        }else if( // TODO: fix non-consistent stopping position.
                bottom(numbers) > bottom(numbersWrapper) - numbersWrapperPadding &&
                (numbersWrapper.offsetTop+numbersWrapper.offsetHeight) - (yPos+headerHeight) < numbers.offsetHeight + (numbersWrapperPadding*2)
        ){
            // Set top poisiton of numbers to highest value it can be without goin into numbersWrapper padding are if
            // it is in numbersWrapper padding area or the visible part of numbersWrapper is less than the
            // height of numbers and height for top and bottom padding.
            numbers.style.top = numbersWrapper - (numbersWrapperPadding*2) - numbers.offsetHeight + "px";
        }else{
            numbers.style.top = yPos + headerHeight - numbersWrapper.offsetTop + "px";
        }
    }
}

function setEventListener(){
    if(window.innerWidth >= 750){ // The threshold for numbers container being on the side, not top
        window.removeEventListener('scroll', numbersScroll);
        window.addEventListener('scroll', numbersScroll);
        numbersScroll()
    }else{
        window.removeEventListener('scroll', numbersScroll);
        resetNumbersElements();
    }
}

setEventListener();
window.addEventListener('resize', setEventListener);