
var count = 1

function Solve() {
    console.log("create")
    var targets = {}
    var priorities = GetPriorities()
    for (var i = 1; i <= count; ++i) {
        var item_name = document.getElementById("name_" + i).value
        var item_amount = document.getElementById("amount_" + i).value
        console.log(item_name, item_amount)
        if (item_name == '' || item_amount == '') {
            continue
        }
        if (!(item_name in targets)) {
            targets[item_name] = 0
        }
        targets[item_name] += parseInt(item_amount)
    }
    var res = {}
    $.ajax({
        url : "/calculator/update/", // the endpoint
        type : "POST", // http method
        data : {"priorities" : JSON.stringify(priorities), "targets" : JSON.stringify(targets)}, // data sent with the post request
        dataType: 'json',
        headers:{"X-CSRFToken": django_csrf_token},
        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            UpdateUI(json)
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    return res
};



function Add() {
    var new_row = document.getElementById("factorio_target_1").cloneNode(true)
    var new_col = document.createElement("div")
    new_col.setAttribute("class", "col-xs-2")
    but = document.createElement("button")
    but.setAttribute("type", "button")
    but.setAttribute("class", "btn btn-danger")
    but.setAttribute("onclick", "DeleteRow(this)")
    but.innerHTML = "X"

    new_col.appendChild(but)
    new_row.appendChild(new_col)


    var form = document.getElementById("items-form")
    form.appendChild(new_row)

    count += 1

    new_row.id = "factorio_target_" + count
    
    new_row.children[0].firstElementChild.name = "name_" + count
    new_row.children[0].firstElementChild.id = "name_" + count
    new_row.children[1].firstElementChild.name = "amount_" + count
    new_row.children[1].firstElementChild.id = "amount_" + count


}
function GetPriorities() {
    var li = document.getElementById("priorities")
    var children = li.children
    var inp = document.getElementById("priorities_input")
    var p = []
    for (var i = 0; i < children.length; ++i) {
        var el = children[i]
        if (el.id != '') {
            p.push(el.id)
        }
    }
    return p
}

function GetTargets() {
    var items_form = document.getElementById("items-form")
    var rows = items_form.children
    for (var i = 0; i < rows.length; i++) {
        var name = rows[i].children[0]
        var amount = rows[i].children[1]
    }

}

function DeleteRow(el) {
    count -= 1

    var row = el.parentNode.parentNode
    row.remove()

    var items_form = document.getElementById("items-form")
    var rows = items_form.children
    var j = 1
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i]
        console.log(row)
        if (row.className == "form-group row") {
            row.id = "factorio_target_" + j
            row.children[0].firstElementChild.name = "name_" + j
            row.children[0].firstElementChild.id = "name_" + j
            row.children[1].firstElementChild.name = "amount_" + j
            row.children[1].firstElementChild.id = "amount_" + j
            j++
        }
        console.log(i)
    }
}


function RenderItems(items) {
    var ul = document.getElementById("res_items_list")
    while (ul.firstChild) {
        ul.removeChild(ul.firstChild)
    }
    for (var i = 0; i < items.length; ++i) {
        var li = document.createElement("li")
        li.setAttribute("class", "list-group-item")
        if ((i + 1) % 2 == 0) {
            li.setAttribute("style", "background-color: #1f3853; color: white")
        } else {
            li.setAttribute("style", "background-color: #1978df; color: white")
        }
        li.innerHTML = items[i]
        ul.appendChild(li)
    }
}

function UpdateUI(res) {
    RenderItems(res['items'])
}

function Update() {
    var res = Solve()
}