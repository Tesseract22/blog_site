import openai
import json
from django.http import HttpResponse
from django.shortcuts import render
openai.api_key = "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"




def Send(request):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Q: 土木工程 A:",
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    # r = json.loads(response)
    init = response['choices'][0]["text"]
    print(init)

    # return HttpResponse(json.dumps({"init":init}), content_type="application/json")
Send(5)

