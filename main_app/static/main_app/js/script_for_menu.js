

function goToLevel(level) {

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            window.location = this.responseText;
        }
    };

    xmlHttp.open("GET", 'lvl/' + level + '/', false);
    xmlHttp.send();
}