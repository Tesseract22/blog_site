function RenderInput(txt) {
    chatOutput.value += "ChatGPT: "  + txt + '\n';
    const arr  = [...txt.matchAll(/\d\.\s(.*)：/g)];
    console.log(arr);
    arr.forEach(PositonOptions);
}

function PositonOptions(value) {
    ul = document.getElementById("list");
    li = document.createElement("li");
    li.className = "list-group-item";
    $(li).html(`${value[1]}需要学习什么知识`);
    li.onclick = function() {Retrieve(`${value[1]}需要学习什么知识`)};
    ul.appendChild(li);
}

function Search(el) {
    Retrieve(el.html)
}


function Retrieve(q, first=false) {
    chatOutput.value += "\n正在生成...\n";
    // var q = search.value;
    $.ajax({
        url : `/search/`, // the endpoint
        type : "POST", // http method
        data : {"q" : q}, // data sent with the post request
        dataType: 'json',
        headers:{"X-CSRFToken": django_csrf_token},
        success : function(json) {
            console.log(json); // log the returned json to the console
            RenderInput(json["result"]);
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}


function Send() {
    var major = search.value;
    var q = `${major}专业可以有哪些职业发展方向`;
    
    Retrieve(q, true)
}
