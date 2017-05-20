var easterEggInput = document.getElementById('easter-egg-input');
var easterEggSubmit = document.getElementById('easter-egg-submit');
var easterEggAudio = document.getElementById('easter-egg-audio');

var easterEgg = function() {
    easterEggAudio.play();
};

easterEggSubmit.addEventListener('click', easterEgg);
easterEggInput.addEventListener('keyup', function(event) {
    if(event.which == 13) { // Pressing enter in input area
    easterEgg();
    }
});