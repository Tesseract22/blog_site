var positions = [];
var p_context;
function RenderInput(txt, first=0) {
    chatOutput.value += "GrowU: "  + txt + '\n';
    const arr  = [...txt.matchAll(/\d((\.\s)|、)(.*)：/g)];
    console.log(arr);

    if (first == 1) {
        ul = document.getElementById("list");
        arr.forEach(element => {
            positions.push(element[3]);
            p_context += element[3] + ', ';
            li = document.createElement("li");
            li.className = "list-group-item";
            $(li).html(`${element[3]}需要学习什么知识`);
            li.onclick = function() {Retrieve(`${element[3]}需要学习什么知识`, 2)};
            ul.appendChild(li);
        });
        li = document.createElement("li");
        li.className = "list-group-item";
        $(li).html(`我的性格适合什么职位`);
        p_context += "我的性格适合什么职位";
        li.onclick = function() { Retrieve(p_context, 0);}
        ul.prepend(li)
    }
    
    if (first == 2) {
        ul = document.getElementById("list");
        arr.forEach(element => {
            positions.push(element[3]);
            p_context += element[3] + ', ';
            li = document.createElement("li");
            li.className = "list-group-item";
            $(li).html(`${element[3]}要学习哪些内容`);
            li.onclick = function() {Retrieve(`${element[3]}要学习哪些内容，你能给我列个大纲吗, 不重不漏的给我总结成几大板块吗`, 0)};
            ul.appendChild(li);
        });
    }


}



function Search(el) {
    Retrieve(el.html)
}


function Retrieve(q, first=0) {
    chatOutput.value += "\n正在生成...\n";
    // var q = search.value;
    console.log()
    $.ajax({
        url : `/search/`, // the endpoint
        type : "POST", // http method
        data : {"q" : q}, // data sent with the post request
        dataType: 'json',
        headers:{"X-CSRFToken": django_csrf_token},
        success : function(json) {
            console.log(json); // log the returned json to the console
            chatOutput.value += "我：" + q + '\n'
            RenderInput(json["result"], first);

        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            chatOutput.value += "失败，请检查输入和网络连接"
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}


function Send() {
    var major = search.value;
    var q = `${major}专业可以有哪些职业发展方向`;
    search.disabled = true;
    Retrieve(q, 1)

}

function test(q="What is openai") {
    var source = new SSE(
        `/search?q=${q}`,
        {
          method: "GET",
        }
    );
    source.addEventListener("open", function(e) {
        console.log("open");
    });
    source.addEventListener("message", function(e) {
        // rep = JSON.parse(e.data);
        console.log(e)
        // chatOutput.value += rep['choices'][0]['txt'] + ',';
        // console.log(rep['choices'][0]['txt']);
    });
    source.addEventListener("error" , function(e) {
        console.log("error");
    })
    source.stream()

    // var source = new EventSource(`/search?q=${q}`)

    // source.onopen = function() {
    //     console.log("open");
    // }

    // source.onmessage = function(e) {
    //     console.log(e);
    // }
    // source.onerror = function(e) {
    //     console.log(e.data);
    // }
    
}

function Reset() {
    search.disabled = false;
    chatOutput.value = "Powered by ChatGPT";
    ul = document.getElementById("list");
    $(ul).html("");
    positions = [];
    p_context = "";
}
