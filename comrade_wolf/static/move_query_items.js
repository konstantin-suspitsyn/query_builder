const selectWindow = document.getElementById("select-field")

let select = {};
let where = {};

let clickedElement;

let i = 0;

const selectOptions = "<select name=\"select_options\">\n" +
    "  <option selected=\"selected\" value=\"select\">Выбрать</option>\n" +
    "  <option value=\"count\">Количество</option>\n" +
    "  <option value=\"distinct count\">Кол-во уникальных</option>\n" +
    "</select>"

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

    elementInSelect = element.cloneNode(true)
    elementInSelect.classList.add("mr-1")
    elementInSelect.classList.add("control")
    elementInSelect.setAttribute("onclick","selectMe(event)");

    selectWindow.appendChild(elementInSelect)

});

addEventListener("click", (event) => {

    console.log(event.target.innerHTML);

    if (event.target === undefined || event.target === null) {
        return;
    }

    if (event.target.classList.contains("control")) {
        return;
    }

    let elementAggr = document.getElementById("aggregate-field");
    let elementDelete = document.getElementById("delete-field");

    elementAggr.disabled = true;
    elementDelete.disabled = true;

    if (clickedElement.classList.contains("selected-border")) {
        clickedElement.classList.remove("selected-border");
    }

    clickedElement = null;

});


function disableButtons() {
    let elementAggr = document.getElementById("aggregate-field");
    let elementDelete = document.getElementById("delete-field");

    elementAggr.removeAttribute('disabled');
    elementDelete.removeAttribute('disabled');
}

function selectMe(event) {

    disableButtons()

    clickedElement = event.target;

    console.log(clickedElement.innerHTML);

    clickedElement.classList.add("selected-border");
}

function deleteSelected() {
    clickedElement.remove();
    disableButtons()
}

function addDropdown() {
    clickedElement.innerHTML += selectOptions;
}