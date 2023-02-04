import openai
import json
from django.http import HttpResponse
from django.shortcuts import render
openai.api_key = "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"




def Send(request):
    q = request.POST["q"]
    print("query: %s"%q)
    q1 = "Q: %s专业可以有哪些职业发展方向? A:"%q
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=q1,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        
    )
    # r = json.loads(response)
    a1 = response['choices'][0]["text"]
    q2 = q1 + a1 + "Q: 需要学习哪些知识来胜任这些职位? A:"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=q2,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    a2 = response['choices'][0]["text"]
    print(q1)
    print(q2)
    # print(a1, a2)
    return HttpResponse(json.dumps({"a1":a1, "a2":a2}), content_type="application/json")
# Send(5)

