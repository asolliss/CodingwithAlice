function timeout() {
    alert("Timeout! Start again");
    clearInterval(timer);
    window.location.href = "#";
}
function update() {
    var time = document.getElementById("timer");
    var spl = time.innerHTML.split(" : ");
    var min = +spl[0];
    var sec = +spl[1];

    if (sec == 0) {
        if (min == 0) {
            timeout();
            return;
        }
        --min;
        sec = 59;
    }
    else {
        --sec;
    }

    min = (min < 10) ? "0" + min : min;
    sec = (sec < 10) ? "0" + sec : sec;
    time.innerHTML = min + " : " + sec;
}

function startTimer() {
    timer = window.setInterval(function () {
        update();
    }, 1000);
}
