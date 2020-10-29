function addDate() {
    var s = document.createElement("section");
    s.appendChild(document.createTextNode(new Date().getFullYear()));
    s.setAttribute("id", "date");
    s.setAttribute("class", "date")
    document.getElementById("footer").appendChild(s);
}

function addRepositoryLink() {
    var a = document.createElement("a");
    a.setAttribute("class", "pagelink-button")
    a.setAttribute("href", "https://github.com/BazyliReps/web_kamien_milowy_1");
    a.setAttribute("id", "repoLink");
    a.appendChild(document.createTextNode("Link Do Repozytorium"));
    document.getElementById("footer").appendChild(a);
}

function initFooter() {
    addDate();
    addRepositoryLink();
}

initFooter();

