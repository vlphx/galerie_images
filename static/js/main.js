// BOUTON UP //

let boutonHaut = document.getElementById("buttonUp");

function scrollFunction() {
    if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
        boutonHaut.style.display = "block";
    } else {
        boutonHaut.style.display = "none";
    }
}

//t = current time
//b = start value
//c = change in value
//d = duration
Math.easeInOutQuad = function (t, b, c, d) {
    t /= d/2;
    if (t < 1) return c/2*t*t + b;
    t--;
    return -c/2 * (t*(t-2) - 1) + b;
};


function topFunction() {
    let start = document.documentElement.scrollTop,
        change = 0 - start,
        currentTime = 0,
        increment = 20,
        duration = 800;

    const animateScroll = function () {
        currentTime += increment;
        var val = Math.easeInOutQuad(currentTime, start, change, duration);
        document.documentElement.scrollTop = val;
        if (currentTime < duration) {
            setTimeout(animateScroll, increment);
        }
    };
    animateScroll();
    //document.body.scrollTop = 0;
    //document.documentElement.scrollTop = 0;
}


window.onscroll = function() {scrollFunction()};
boutonHaut.addEventListener("click",topFunction)