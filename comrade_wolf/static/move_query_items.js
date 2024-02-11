let select = {};
let where = {};

const SELECT = "select";
const WHERE = "where";

let clickedElement;
let whatToAdd = SELECT;

const selectOptions = "<select name=\"select_options\">\n" +
    "  <option selected=\"selected\" value=\"select\">Выбрать</option>\n" +
    "  <option value=\"count\">Количество</option>\n" +
    "  <option value=\"distinct count\">Кол-во уникальных</option>\n" +
    "</select>"

const calculationOptions = "<select name=\"select_options\">\n" +
    "  <option selected=\"selected\" value=\"select\">Выбрать</option>\n" +
    "  <option value=\"count\">Количество</option>\n" +
    "  <option value=\"sum\">Сумма</option>\n" +
    "  <option value=\"avg\">Средний</option>\n" +
    "  <option value=\"distinct count\">Кол-во уникальных</option>\n" +
    "</select>"

const whereOptions = "<select onchange=\"insertInput(event)\" name=\"select_options\">\n" +
    "  <option value=\"=\">Выбери</option>\n" +
    "  <option value=\"=\">Равно</option>\n" +
    "  <option value=\">\">Больше</option>\n" +
    "  <option value=\"<\">Меньше</option>\n" +
    "  <option value=\">=\">Больше или равно</option>\n" +
    "  <option value=\"<=\">Меньше или равно</option>\n" +
    "  <option value=\"between\">Между</option>\n" +
    "  <option value=\"like\">Содержит</option>\n" +
    "  <option value=\"not like\">Не содержит</option>\n" +
    "  <option value=\"in\">В списке</option>\n" +
    "  <option value=\"not in\">Не в списке</option>\n" +
    "</select>"

const lonelyInput = "<input type=\"text\" required minlength=\"4\" maxlength=\"8\" size=\"10\" />"
const betweenInput = "<input type=\"text\" required minlength=\"4\" maxlength=\"8\" size=\"10\" /> И  " +
    "<input type=\"text\" required minlength=\"4\" maxlength=\"8\" size=\"10\" />"

const selectOptionsMap = new Map([
  ["select", selectOptions],
  ["value", calculationOptions],
]);

const idSelectedOrAnd = "selected-or-and"

const andDiv = "<div class=\"and\" onclick=\"selectAndOr(event)\" id=\"" + idSelectedOrAnd + "\"></div>";
const orDiv = "<div class=\"or\" onclick=\"selectAndOr(event)\" id=\"" + idSelectedOrAnd + "\"></div>";

const whereBoxId = "where-field";
const selectBoxId = "select-field";




addEventListener("dblclick", (event) => {
    /**
     * Move button to selected field
     */

    let element = event.target;

    // We need only button
    if (element.type !== "button") {
        return;
    }

    // We need to work only on ready to select fields
    if (element.parentNode.id !== "all-fields") {
        return;
    }

    let elementInSelect = element.cloneNode(true);
    elementInSelect.classList.add("mr-1");
    elementInSelect.classList.add("control");
    elementInSelect.setAttribute("onclick","selectMe(event)");

    if (whatToAdd === SELECT) {
        // Все для select
        document.getElementById("select-field").appendChild(elementInSelect);
    }

    if (whatToAdd === WHERE) {

        elementInSelect.innerHTML += whereOptions;
        elementInSelect.innerHTML += "<span class='placeholder'></span>";
        elementInSelect.setAttribute("onclick","addWhereId(event)");

        // Все для select
        let isNoAndAndNoOr = true;

        let whereBlock = document.getElementById("where-field");
        let currentAndOrOr = document.getElementById("selected-or-and");

        if ((whereBlock.childElementCount === 0) && (currentAndOrOr === null)) {

            whereBlock.appendChild(elementInSelect);
            return;
        }

        if ((whereBlock.childElementCount > 0) && (currentAndOrOr === null)) {
            let alreadyInWhere = whereBlock.getElementsByTagName("button")[0].cloneNode(true);
            whereBlock.getElementsByTagName("button")[0].remove();
            addAnd();
            currentAndOrOr = document.getElementById("selected-or-and");
            currentAndOrOr.appendChild(alreadyInWhere);
            currentAndOrOr.appendChild(elementInSelect);
            return;
        }

        if (currentAndOrOr != null) {
            currentAndOrOr.appendChild(elementInSelect);
        }

    }

});

addEventListener("click", (event) => {

    if (event.target === undefined || event.target === null) {
        return;
    }

    if (event.target.classList.contains("control")) {
        return;
    }

    disableButtons()

    if (clickedElement.classList.contains("selected-border")) {
        clickedElement.classList.remove("selected-border");
    }

    clickedElement = null;

});


function disableButtons() {

    enableButton("aggregate-field", true);
    enableButton("delete-field", true);

}

function selectMe(event) {

    // This if for clicks between buttons in select
    enableButton("aggregate-field", true);

    enableButton("delete-field", false);

    clickedElement = event.target;

    const isFound = Array.from(selectOptionsMap.keys()).some(className => Array.from(clickedElement.classList).includes(className))

    if (isFound) {
        enableButton("aggregate-field", false);
    }
    clickedElement.classList.add("selected-border");
}

function deleteSelected() {
    clickedElement.remove();
    disableButtons();
}

function addDropdown() {

    let option = null;

    for (let [key, value] of selectOptionsMap) {
        if (clickedElement.classList.contains(key)) {
            option = value;
        }
    }

    if (option === null) {
        return;
    }

    if (clickedElement.getElementsByTagName("select")["length"] > 0) {
        return;
    }

    clickedElement.innerHTML += option;
}

function enableButton(elementId, disable) {
    /**
     * Enable or disable button
     */

    let element = document.getElementById(elementId);

    if (disable === false) {
        element.removeAttribute('disabled');
    } else {
        element.disabled = true;
    }
}


function changeAddition() {
    const toWhere = "to-where";
    let toWhereElement = document.getElementById(toWhere);
    const toSelect = "to-select";
    let toSelectElement = document.getElementById(toSelect);

    const btnLight = "btn-light";
    const btnOutlineDark = "btn-outline-dark";

    if (toWhereElement.hasAttribute("disabled")) {
        enableButton(toWhere, false);
        enableButton(toSelect, true);
        toWhereElement.classList.remove(btnLight);
        toWhereElement.classList.remove(btnLight);
        toWhereElement.classList.add(btnOutlineDark);
        toSelectElement.classList.remove(btnOutlineDark);
        toSelectElement.classList.add(btnLight);
        whatToAdd = SELECT;
    } else {
        enableButton(toWhere, true);
        enableButton(toSelect, false);
        toWhereElement.classList.remove(btnOutlineDark);
        toWhereElement.classList.add(btnLight);
        toSelectElement.classList.remove(btnLight);
        toSelectElement.classList.add(btnOutlineDark);
        whatToAdd = WHERE;
    }
}

function addAndOrOr(divToAdd) {

    enableButton("delete-or-and", false);

    let boxElement = document.getElementById(whereBoxId);

    if (boxElement.childElementCount === 0) {

        boxElement.innerHTML += divToAdd;
        return;
    }

    let innerOrOrAnd = document.getElementById(idSelectedOrAnd);

    if (innerOrOrAnd == null) {
        return;
    }

    innerOrOrAnd.removeAttribute("id");
    innerOrOrAnd.innerHTML += divToAdd;

}

function addOr() {
    addAndOrOr(orDiv);
}

function addAnd() {
    addAndOrOr(andDiv);
}

function deleteField() {
    let buttonToDelete = document.getElementById("selected-where-button");
    buttonToDelete.remove();
    enableButton("delete-field-where", true);
}

function deleteOrAnd() {
    let selectedAndOr = document.getElementById(idSelectedOrAnd);
    selectedAndOr.remove();
    enableButton("delete-or-and", true);
}

function removeIdFromAnyElement(idTagName) {
    /**
     * Removes id from any element
     */
    let alreadySelected = document.getElementById(idTagName.toString());

    if (alreadySelected !== null) {
        alreadySelected.removeAttribute("id");
    }

}

function selectAndOr(event) {


    // Selected div with and or for
    let selectedElement = event.target;

    if (!selectedElement.classList.contains("and") && !selectedElement.classList.contains("or")) {
        return;
    }

    removeIdFromAnyElement(idSelectedOrAnd);

    selectedElement.id = idSelectedOrAnd;

    enableButton("delete-or-and", false);

}

function insertInput(event) {
    let currentElement = event.target;
    let parentButton = currentElement.parentNode;
    let spanToInsert = parentButton.getElementsByClassName("placeholder")[0];
    spanToInsert.innerHTML = "";

    if (currentElement.value === "between") {
        spanToInsert.innerHTML += betweenInput;
    } else {
        spanToInsert.innerHTML += lonelyInput;
    }


}

function addWhereId(event) {
    let currentButton = event.target;

    enableButton("delete-field-where", false);
    addId(currentButton, "selected-where-button");

}

function addId(currentElement, idName) {

    let anyElement = document.getElementById(idName);
    if (anyElement !== null) {
        anyElement.removeAttribute("id");
    }
    currentElement.setAttribute("id", idName);

}
