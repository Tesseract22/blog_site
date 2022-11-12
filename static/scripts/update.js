// import * as helper from 'update-helper.js'
var default_machines = ["assembling-machine-3", "electric-mining-drill"]


var count = 1
function Solve(game) {
    var targets = GetTargets()
    var priorities = GetPriorities()
    var alt = GetAlt()
    // var url = `/calculator/${game}/update/`
    $.ajax({
        url : `/calculator/${game}/update/`, // the endpoint
        type : "POST", // http method
        data : {"priorities" : JSON.stringify(priorities), "targets" : JSON.stringify(targets), "alt" : JSON.stringify(alt)}, // data sent with the post request
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
};



function Add() {
    var new_row = document.getElementById("factorio_target").cloneNode(true)
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

    // new_row.id = "factorio_target_" + count
    
    new_row.children[0].firstElementChild.name = "name"
    new_row.children[1].firstElementChild.name = "amount"


}
function GetAlt() {
    var alt = []
    document.getElementsByName("alt-checkbox").forEach(function(el) {
        if (el.checked) {
            alt.push(el.getAttribute('value'))
        }
        // console.log(el.getAttribute('type'))
    })
    return alt
    
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
    var names = document.getElementsByName("name")
    var amounts = document.getElementsByName("amount")
    var l = names.length
    if (l != amounts.length) {
        alert("Unexpected Targets")
        return
    }
    var res = {}
    for (var i = 0; i < l; ++i) {
        var name = names[i].value
        var amount = amounts[i].value
        res[name] = parseFloat(amount)
    }
    // console.log(res)
    return res

}

function DeleteRow(el) {
    count -= 1

    var row = el.parentNode.parentNode
    row.remove()
}


function RenderItems(res) {
    var itemflow = res['items']
    var recipes = res['ans']
    var items = Object.keys(itemflow)

    // create the new tbody and its content
    var table = document.getElementById("res_items_list")
    table.removeChild(table.lastElementChild) // effectively remove <tbody>
    var tbody = document.createElement("tbody")
    table.appendChild(tbody)
    for (var i = 0; i < items.length; ++i) {
        var tr = document.createElement("tr")
        var td_item = document.createElement("td")
        tr.appendChild(td_item)
        // li.setAttribute("class", "list-group-item")
        var btn = document.createElement("button")
        btn.setAttribute("class", "btn btn-link collapsed")
        btn.setAttribute("data-toggle", "collapse")
        btn.setAttribute("data-target", "#res_item_" + i)
        btn.setAttribute("aria-expanded", "false")
        btn.setAttribute("aria-controls", "res_item_" + i)


        var icon = document.createElement("img")
        var icon_src = `${base_dir}img/${game}_item_icon/${items[i].replaceAll(' ', '-').toLowerCase()}${img_type}`
        // console.log(icon_src)
        icon.setAttribute("src", icon_src)
        icon.setAttribute("class", "item-icon left-icon")
        btn.appendChild(icon)

        var name = document.createElement("h5")
        name.setAttribute("style", "color: white")
        name.textContent = items[i]
        btn.appendChild(name)
        

        
        td_item.appendChild(btn)

        
        

        var coll = document.createElement("div")
        coll.setAttribute("id", "res_item_" + i)
        coll.setAttribute("class", "collapse")
        coll.innerText = "test"

        // helper.test()
        // RenderItemPut(coll, itemflow[items[i]])

        

        // if ((i + 1) % 2 == 0) {
        //     li.setAttribute("style", "background-color: var(--res-color-1); color: white")
        // } else {
        //     li.setAttribute("style", "background-color: var(--res-color-2); color: white")
        // }

        var flow_data = itemflow[items[i]]
        var total = document.createElement("td")
        total.innerText = (flow_data["total"]).toFixed(4)
        // total.setAttribute("data", (flow_data["total"]).toFixed(4))
        tr.appendChild(total)
        
        tr.appendChild(_RenderFactory(flow_data, recipes))

        
        var td_belt = document.createElement("td")
        var belt = Object.keys(belts)[0]

        var belt_icon = document.createElement("img")
        belt_icon.setAttribute("class", "item-icon left-icon")
        belt_icon.setAttribute("src", GetIcon(belt))
        td_belt.appendChild(belt_icon)
        
        var belt_amount = document.createElement("div")
        // console.log(machines[factory])
        belt_amount.setAttribute("style", "display: inline")
        belt_amount.innerText = (flow_data['total'] / (480 * belts[belt])).toFixed(4)
        td_belt.appendChild(belt_amount)

        tr.appendChild(td_belt)

        tbody.appendChild(tr)
        tbody.appendChild(coll)
    

    }
}

function _RenderBelt(flow_data) {
    var td_belt = document.createElement('td')
    var total = flow_data['total']
    // to do 
}

function _RenderFactory(flow_data, recipes) {

    var td_factory = document.createElement("td")
    var default_recipe = Object.keys(flow_data['input'])[0]
    var factories = _GetAllFactories(default_recipe)
    
    var factory = factories[0]
    for (const i of factories) {
        for (const d of default_machines) {
            if (d == i) {
                factory = d
            }
        }
    }
    var factory_icon = document.createElement("img")
    factory_icon.setAttribute("class", "item-icon")
    factory_icon.setAttribute("src", GetIcon(factory))

    if (factories.length == 1) {
        factory_icon.setAttribute("class", "item-icon left-icon")
        td_factory.appendChild(factory_icon)
    } else {
        var dropdown = document.createElement("div")
        dropdown.setAttribute("class", "dropdown")
        $(td_factory).html(
            `<div class="dropdown">
                <button class="btn" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="padding: 2px; background: #0000004d">
                   
                </button>
                <div class="dropdown-menu dropdown-menu-dark" aria-labelledby="dropdownMenuButton">
                </div>
            </div>`
        )
        td_factory.firstElementChild.firstElementChild.appendChild(factory_icon)
        for (var k in factories) {
            var a = document.createElement("a")
            a.setAttribute("class", "dropdown-item")
            var icon = document.createElement("img")
            icon.setAttribute("class", "item-icon")
            icon.setAttribute("src", GetIcon(factories[k]))
            icon.setAttribute('onclick', "UpdateFactory(this)")
            icon.setAttribute('factory', factories[k])
            a.appendChild(icon)

            td_factory.firstElementChild.firstElementChild.nextElementSibling.appendChild(a)
        }
        
    }

    var factory_amount = document.createElement("div")
    // console.log(machines[factory])
    factory_amount.setAttribute("style", "display: inline")
    factory_amount.innerText = (recipes[default_recipe] / machines[factory]["crafting_speed"]).toFixed(4)
    factory_amount.setAttribute('data', recipes[default_recipe])
    td_factory.appendChild(factory_amount)
    return td_factory
}

function _OnClickFactory(el) {
    var old_icon = el.parentNode.parentNode.previousElementSibling.firstElementChild
    old_icon.setAttribute('src', el.getAttribute('src'))
    old_icon.setAttribute('factory', el.getAttribute('factory'))
    

}

function UpdateFactory(el) {
    _OnClickFactory(el)
    var old_amount = el.parentNode.parentNode.parentNode.nextElementSibling
    old_amount.innerText =  (parseFloat(old_amount.getAttribute("data")) / (machines[el.getAttribute('factory')]["crafting_speed"])).toFixed(4)
}

function ChangeDefaultFactory(el) {
    var old_icon = el.parentNode.parentNode.previousElementSibling.firstElementChild
    var old_factory = old_icon.getAttribute("factory")
    default_machines = default_machines.filter(function(e) { return e != old_factory })
    _OnClickFactory(el)
    default_machines.push(old_icon.getAttribute('factory'))
    Update(game)
    
}

function _GetBestFactory(factories) {
    var max = 0
    var max_f = ""
    for (var f in factories) {
        for (var d in default_machines) {
            if (f == d) return f
        }
        if (machines[f]["crafting_speed"] > max) {
            max = machines[f]["crafting_speed"]
            max_f = f
        }
    }
    return max_
}




function _GetAllFactories(recipe) {
    
    return machine_group[recipe_group[recipe]]
}

function GetIcon(name) {
    return `${base_dir}img/${game}_item_icon/${name}.webp`
}

function RenderItemPut(el, put) {
    var input_ul = document.createElement("ul")
    input_ul.setAttribute("class", "list-group list-group-flush")
    el.appendChild(input_ul)

    var input_head = document.createElement("h6")
    $(input_head).html("<strong>Produced by: </strong>")
    input_ul.appendChild(input_head)

    var input_data = put['input']
    for (var k in input_data) {

        var li = document.createElement("li")
        li.setAttribute("class", "list-group-item")
        li.setAttribute("style", "color: white; background: #490000")
        
        $(li).html(`\
        <button type="button" class="btn btn-secondary"\
        name=${k}\
         data-toggle="tooltip" data-placement="right" data-html="true" title="Click to view more..." style="background: transparent" onclick="GetRecipe(this)">\
        ${k}: ${input_data[k]}\
        </button>`)

        input_ul.appendChild(li)
    }

    // -----------------------------------------
    var output_ul = document.createElement("ul")
    output_ul.setAttribute("class", "list-group list-group-flush")
    el.appendChild(output_ul)

    var output_head = document.createElement("h6")
    $(output_head).html("<strong>Consumed by: </strong>")
    output_ul.appendChild(output_head)

    var output_data = put['output']
    for (var k in output_data) {  
        var li = document.createElement("li")
        // var tooltip_btn = document.createElement("button")

        li.setAttribute("class", "list-group-item")
        li.setAttribute("style", "color: white; background: #00003e")

        $(li).html(`\
        <button type="button" class="btn btn-secondary"\
         name=${k}
         data-toggle="tooltip" data-placement="right" data-html="true" title="Click to view more..." style="background: transparent" onclick="GetRecipe(this)">\
        ${k}: ${output_data[k]}\
        </button>`)
        output_ul.appendChild(li)
    }
}


function UpdateUI(res) {
    RenderItems(res)
}

function Update(game) {
    console.log("update, game:" + game)
        Solve(game)
}

function GetRecipe(el) {
    var recipe_name = el.name
    $.ajax({
        url : `/calculator/${game}/get_recipe/`, // the endpoint
        type : "POST", // http method
        data : {'recipe_name': recipe_name}, // data sent with the post request
        dataType: 'json',
        headers:{"X-CSRFToken": django_csrf_token},
        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            RenderRecipeTooltip(el, json)

        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function RenderRecipeTooltip(el, json) {
    // el.setAttribute("data-original-title", "TEST")   
    var con = document.createElement("div")
    con.setAttribute("class", "container")
    con.setAttribute("style", "display: table;")
    
    var title = document.createElement("div")
    title.setAttribute("class", "row align-items-start")
    title.innerHTML = "<h6>Recipe Info: </h6>"
    con.appendChild(title)

    var input = document.createElement("div")
    input.setAttribute("class", "row align-items-start")

    var input_title = document.createElement("div")
    input_title.setAttribute("class", "col")
    input_title.innerHTML = "<h7>Input: </h7>"
    input.appendChild(input_title)
    con.appendChild(input)
    for (var item in json['input']) {
        var col = document.createElement("div")
        col.setAttribute("class", "col")
        col.textContent = item + ': ' + json['input'][item]
        input.appendChild(col)
    }

    var output = document.createElement("div")
    output.setAttribute("class", "row align-items-start")

    var output_title = document.createElement("div")
    output_title.setAttribute("class", "col")
    output_title.innerHTML = "<h7>Output: </h7>"
    output.appendChild(output_title)
    con.appendChild(output)
    for (var item in json['output']) {
        var col = document.createElement("div")
        col.setAttribute("class", "col")
        col.textContent = item + ': ' + json['output'][item]
        output.appendChild(col)
    }
    
    $(el).tooltip("dispose").attr("title", con.outerHTML).tooltip()
    $(el).attr("onclick", "")
    $(':focus').blur()
    $(el).focus() // basically reload the tooltip

}

function ShowPriorities(el) {
    $("#priorities").toggle(500)

}














