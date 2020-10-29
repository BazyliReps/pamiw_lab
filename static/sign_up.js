function checkLogin(e) {
    let username = this.value;
    let link = "/check_login/" + username;
    let re = "^[a-z]{3,12}$";
    let s = document.getElementById("login");

    var responseText = "";
    if (username.match(re)) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = "json"
        xhr.open("GET", link, true);
        xhr.onload = function (e) {
        if (this.readyState == 4) {
            if (this.status == 200) {
                isAvailable = this.response[username] == 'available'
                if (!isAvailable) {
                    responseText = "Użytkownik zajęty!";
                    console.log('zajety!')
                    s.setCustomValidity(responseText);
                    s.reportValidity();
                }
            } else {
                console.error(xhr.statusText);
            }
        }
        };
        xhr.send();
    } else {
        responseText = "Login powinien składać się z od 3 do 12 małych liter bez polskich znaków.";
    }
    console.log(responseText);
    s.setCustomValidity(responseText);
    s.reportValidity();
}

function checkFirstname(e) {
    var firstname = this.value;
    var re = "^[A-Z{PL}][a-z{pl}]+$";
    var f = document.getElementById("firstname");
    var errorResponse = "";
    if (!firstname.match(re)) {
        errorResponse = "Imię powinno zaczynać się od wielkiej litery a następnie wyłącznie z małych liter.";
    }
    f.setCustomValidity(errorResponse);
    f.reportValidity();
}

function checkLastname(e) {
    var lastname = this.value;
    var re = "^[A-Z{PL}][a-z{pl}]+$";
    var s = document.getElementById("lastname");
    var errorResponse = "";
    if (!lastname.match(re)) {
        errorResponse = "Nazwisko powinno zaczynać się od wielkiej litery a następnie wyłącznie z małych liter.";
    }
    s.setCustomValidity(errorResponse);
    s.reportValidity();
}

function checkPassword(e) {
    var passwd = this.value;
    var re = "^.{8,}$";
    var s = document.getElementById("password");
    var errorResponse = "";
    if (!passwd.match(re)) {
        errorResponse = "Hasło musi składać się z co najmniej 8 znaków.";
    }
    s.setCustomValidity(errorResponse);
    s.reportValidity();
}

function checkConfirmPassword(e) {
    var passwd = document.getElementById("password").value
    console.log("passwd: " + passwd)
    var confPasswd = this.value;
    var s = document.getElementById("confirmPassword");
    var errorResponse = "";
    if (passwd != confPasswd) {
        errorResponse = "Niepoprawnie powtórzone hasło!"
    }
    s.setCustomValidity(errorResponse);
    s.reportValidity();
}

function attach_events() {
    var username = document.getElementById("login");
    username.addEventListener("input", checkLogin);

    var firstname = document.getElementById("firstname");
    firstname.addEventListener("input", checkFirstname);

    var lastname = document.getElementById("lastname");
    lastname.addEventListener("input", checkLastname);

    var passwd = document.getElementById("password");
    passwd.addEventListener("input", checkPassword)

    var confPasswd = document.getElementById("confirmPassword");
    confPasswd.addEventListener("input", checkConfirmPassword);
}

attach_events()