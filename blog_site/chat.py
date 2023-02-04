import openai
import json
from django.http import HttpResponse
from django.shortcuts import render
import re
openai.api_key = "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"




# def Send(request):
#     results = {}
#     q = request.POST["q"]
#     print("query: %s"%q)
#     q1 = "Q: %s专业可以有哪些职业发展方向? A:"%q
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=q1,
#         temperature=0,
#         max_tokens=1000,
#         top_p=1,
#         frequency_penalty=0.0,
#         presence_penalty=0.0,
        
#     )
#     # r = json.loads(response)
#     a1 = response['choices'][0]["text"]
#     results["a1"] = a1
#     positions = re.findall(r"[1-9]\.(.*)：", a1)
#     results["a2"] = []
#     for p in positions:
#         q2 = "Q: 需要学习哪些知识来胜任%s? A:"%p
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=q2,
#             temperature=0,
#             max_tokens=1000,
#             top_p=1,
#             frequency_penalty=0.0,
#             presence_penalty=0.0,
#             stop=["\n"]
#         )
#         a2 = response['choices'][0]["text"]
#         results["a2"].append(a2)

#     print(q1)
#     print(positions)
#     return HttpResponse(json.dumps(results), content_type="application/json")

def Send(request):
    q = request.POST["q"]
    print(q)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=q,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0, 
    )
    return HttpResponse(json.dumps({"result": response['choices'][0]["text"]}), content_type="application/json")
# Send(5)

