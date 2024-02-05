const selectWindow = document.getElementById("select-field")

let select = {};
let where = {};

let i = 0;

addEventListener("dblclick", (event) => {
    /**
     * Move button to selected field
     * @type {EventTarget}
     */
    const element = event.target

    // We need only button
    if (element.type !== "button") {
        return;
    }

    // We need to work only on ready to select fields
    if (element.parentNode.id !== "all-fields") {
        return;
    }

    console.log(element.outerHTML)

    selectWindow.innerHTML += "<div class='mr-1'>" + element.outerHTML + "</div>"

});

console.log(selectWindow)