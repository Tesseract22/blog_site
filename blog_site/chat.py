import openai
import json
from django.http import HttpResponse
from django.shortcuts import render
openai.api_key = "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"




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
