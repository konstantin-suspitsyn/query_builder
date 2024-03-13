// Map to set correct input using frontend type
let frontInputTypes = new Map();
frontInputTypes.set("date", "date");
frontInputTypes.set("number", "text");
frontInputTypes.set("datetime", "datetime-local");
frontInputTypes.set("boolean", "text");
frontInputTypes.set("text", "text");

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

const lonelyInput = "<input type=\"%TYPE%\" required minlength=\"4\" maxlength=\"8\" size=\"10\" />"
const betweenInput = "<input type=\"%TYPE%\" required minlength=\"4\" maxlength=\"8\" size=\"10\" /> И  " +
    "<input type=\"%TYPE%\" required minlength=\"4\" maxlength=\"8\" size=\"10\" />"

const selectOptionsMap = new Map([
  ["select", selectOptions],
  ["value", calculationOptions],
]);

const idSelectedOrAnd = "selected-or-and"

const andDiv = "<div class=\"and\" onclick=\"selectAndOr(event)\" id=\"" + idSelectedOrAnd + "\"></div>";
const orDiv = "<div class=\"or\" onclick=\"selectAndOr(event)\" id=\"" + idSelectedOrAnd + "\"></div>";

const whereBoxId = "where-field";
const selectBoxId = "select-field";


function addElementToWhere(elementInSelect) {

    elementInSelect = elementInSelect.cloneNode(true);

    elementInSelect.removeAttribute("onclick");

    elementInSelect.setAttribute("onclick","addWhereId(event)");

    let whereBlock = document.getElementById("where-field");
    let currentAndOrOr = document.getElementById("selected-or-and");

    if ((whereBlock.childElementCount === 0) && (currentAndOrOr === null)) {

        whereBlock.appendChild(elementInSelect);
        return;
    }

    if ((whereBlock.childElementCount > 0) && (currentAndOrOr === null)) {

        insertWrapper(whereBlock, andDiv);
        currentAndOrOr = document.getElementById("selected-or-and");

    }

    if (currentAndOrOr != null) {
        currentAndOrOr.appendChild(elementInSelect);
    }
}

function includeIntoWhere(event) {
    let elementInSelect = event.target;
    addElementToWhere(elementInSelect);
}

function includeIntoQuery(event) {
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

        if (elementInSelect.classList.contains("calculation")) {
            window.alert("Поле является вычисляемым. Его нельзя использовать во where");
            return;
        }
        if (!elementInSelect.classList.contains("where")) {
            elementInSelect.innerHTML += whereOptions;
            elementInSelect.innerHTML += "<span class='placeholder'></span>";
        }

        // Все для where

        addElementToWhere(elementInSelect);

    }

}

addEventListener("click", (event) => {

    if (event.target === undefined || event.target === null) {
        return;
    }

    if (event.target.classList.contains("control")) {
        return;
    }

    disableAggregateAndDelete()

    if (clickedElement === undefined || clickedElement === null) {
        return;
    }

    if (clickedElement.classList.contains("selected-border")) {
        clickedElement.classList.remove("selected-border");
    }

    clickedElement = null;

});


function disableAggregateAndDelete() {

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
    disableAggregateAndDelete();
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

function insertWrapper(boxElement, divToAdd) {
    let alreadyInWhere = boxElement.getElementsByTagName("button")[0].cloneNode(true);
    boxElement.getElementsByTagName("button")[0].remove();

    boxElement.innerHTML += divToAdd;

    let currentAndOrOr = document.getElementById("selected-or-and");
    currentAndOrOr.appendChild(alreadyInWhere);

}

function addAndOrOr(divToAdd) {

    enableButton("delete-or-and", false);

    let boxElement = document.getElementById(whereBoxId);

    let andOrCount = boxElement.getElementsByClassName("or").length + boxElement.getElementsByClassName("and").length

    if ((boxElement.childElementCount === 0) || (andOrCount === 0)) {

            if (boxElement.childElementCount > 0) {
                insertWrapper(boxElement, divToAdd);
                return;
            }
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
    enableButton("delete-field-where", true);
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

    let inputType = new Map();

    for (let [key, value] of frontInputTypes) {
        if (parentButton.classList.contains(key)) {
            inputType.set("%TYPE%", value);
        }
    }

    spanToInsert.innerHTML = "";

    if (currentElement.value === "between") {
        spanToInsert.innerHTML += betweenInput.replace("%TYPE%", inputType.get("%TYPE%")).replace("%TYPE%", inputType.get("%TYPE%"));
    } else {
        if (currentElement.value === "in") {
            spanToInsert.innerHTML += lonelyInput.replace("%TYPE%", "text");
        }
        else {
            spanToInsert.innerHTML += lonelyInput.replace("%TYPE%", inputType.get("%TYPE%"));
        }
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

function isWhereOk(where) {
    /**
     * Checks if where is fine
     * All inputs exist
     * All inputs are filled in
     */

    if (where.size === 0) {
        return true;
    }

    for (let value of where.values()) {

        if (value instanceof Array) {

            for (let i = 0; i < value.length; i++) {
                let answer = isWhereOk(value[i]);
                if (answer === false) {
                    return false;
                }
            }
        }

        if (value instanceof Map) {
            if (value.has("condition")) {
                let condition = value.get("condition");
                if (condition.length === 0) {
                    return false;
                }
                for (let i = 0; i < condition.length; i++) {
                    if (condition[i] === "") {
                        return false;
                    }
                }
            }

        }
    }

    return true;
}

function sendPostWithFields(select) {
    const json = JSON.stringify(mapToObject(select), replacer);

    let request = new XMLHttpRequest();

    request.onload = () => {
          if (request.readyState === 4 && request.status === 200) {
              let overlayElement = document.getElementById("overlay");
              overlayElement.classList.remove("no-show");
              overlayElement.classList.add("show");
              let sqlText = document.getElementById("sql-text");
              sqlText.innerHTML = request.responseText;
            console.log(request.responseText);
          } else {
            console.log(`Error: ${request.status}`);
          }
        };

    request.open('POST', window.location.href);
    request.setRequestHeader("Content-Type", "application/json");
    request.send(json);



}

function reqListener() {
  console.log(this.responseText);
}

function generateFieldsAndWhere() {

    let select = generateSelect();
    select.set("where", generateWhereCondition())

    if (select.get("select").length === 0) {
        window.alert("Ничего не выбрано в select");
        return;
    }

    if (isWhereOk(select.get("where")) === false) {
        window.alert("Поле where заполнено некорректным образом");
        return;
    }

    sendPostWithFields(select);

}

function replacer(name, val) {
    //console.log('replacer name=' + name + ' value ' + val);
    if (val instanceof Map){
        // Convert Map to Object
        return mapToObject(val);
    } else {
        return val; // return as is
    }
}

function myJsonStringify(obj){
    let rtn;
    if (obj instanceof Map) {
        rtn = JSON.stringify(mapToObject(obj), replacer, 4);
    } else {
        rtn = JSON.stringify(obj, replacer, 4);
    }
    return rtn;
}

function mapToObject(aMap) {
    let obj = Object.create(null);
    for (let [k,v] of aMap) {
        // We don’t escape the key '__proto__' which can cause problems on older engines
        if (v instanceof Map) {
            obj[k.toString()] = mapToObject(v); // handle Maps that have Maps as values
        } else {
            obj[k.toString()] = v;              // calling toString handles case where map key is not a string JSON requires key to be a string
        }
    }
    return obj;
}


function buttonPrint(element) {
    /**
     * Generates condition for button
     * @type {Map<any, any>}
     */

    let where = new Map();
    let whereConditions = new Map();

    if (element.classList.contains("where")) {
        whereConditions.set("operator", "predefined");
        where.set(element.value, whereConditions);
        return where;
    }

    let dropdown = element.getElementsByTagName("select")[0];
    let inputValues = []

    let inputs = element.getElementsByTagName("input");

    for (let i = 0; i < inputs.length; i++) {
        inputValues.push(inputs[i].value);
    }

    whereConditions.set("operator", dropdown.value);
    whereConditions.set("condition", inputValues);

    where.set(element.value, whereConditions);

    return where;
}

function generateStringOfOrOrAnd(element, classListElement) {
    /**
     * Generates map for every and and or inside where box
     * @type {Map<any, any>}
     */

    let where = new Map();

    let allInners = [];

    let children = element.children;

    for (let i=0; i < children.length; i++) {

        if (children[i].tagName === "BUTTON") {
            allInners.push(buttonPrint(children[i]))
        }

        if (children[i].tagName === "DIV") {
            allInners.push(generateStringOfOrOrAnd(children[i], children[i].classList[0]));
        }
    }

    where.set(classListElement, allInners);

    return where;
}

function generateWhereCondition() {
    /**
     * Generates map from where field
     * @type {Map<any, any>}
     */

    let where = new Map();

    let element = document.getElementById("where-field").children[0];

    if (element === undefined) {
        return where;
    }

    if (element.tagName === "BUTTON") {
        where = buttonPrint(element);
    }

    if (element.tagName === "DIV") {
       where = generateStringOfOrOrAnd(element, element.classList[0]);
    }

    return where;

}

function generateSelect() {
    let selectedFields = new Map();
    selectedFields.set("select", []);
    selectedFields.set("calculation", []);

    let selectBox = document.getElementById("select-field").children;

    for (let i=0; i < selectBox.length; i++) {

        if (selectBox[i].classList.contains("calculation")) {
            selectedFields.get("calculation").push(selectCalculatedButton(selectBox[i], true));
        }

        if (selectBox[i].classList.contains("value") || selectBox[i].classList.contains("select")) {

            if (selectBox[i].getElementsByTagName("select").length === 0) {
                selectedFields.get("select").push(selectBox[i].value);
            } else {
                selectedFields.get("calculation").push(selectCalculatedButton(selectBox[i], false));
            }
        }

    }
    return selectedFields;

}

function selectCalculatedButton(selectButton, isPreCalculated) {

    let buttonInfo = new Map();

    let calcType = "PREDEFINED";

    if (isPreCalculated === false) {
        let select = selectButton.getElementsByTagName("select")[0];
        calcType = select.value;
    }

    buttonInfo.set(selectButton.value, calcType);
    return buttonInfo;
}

function closeOverlay() {
    let overlayElement = document.getElementById("overlay");
    overlayElement.classList.remove("show");
    overlayElement.classList.add("no-show");
}