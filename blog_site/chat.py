import openai
import json
from django.http import StreamingHttpResponse 
from django.shortcuts import render
import re
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


import requests

import json
import pprint
# pip install sseclient-py
import sseclient    
import logging
import sys
# openai.api_key = settings.API_KEY
@csrf_exempt
def Send(request):
    # print(request.body.decode('utf-8'), file=sys.stderr, flush=True)
    print(request)
    q = request.GET["q"]
    # print(request.GET, q, file=sys.stderr, flush=True)
    return StreamingHttpResponse(streaming_content=testIter(), content_type='text/event-stream')
# Send(5)

def testIter():
    for i in range(1000):
        yield f"data: {i}\n\n"

def performRequestWithStreaming(q):
    reqUrl = 'https://api.openai.com/v1/completions'
    reqHeaders = {
        'Accept': 'text/event-stream',
        'Authorization': 'Bearer ' + settings.API_KEY
    }
    reqBody = {
      "model": "text-davinci-003",
      "prompt": q,
      "max_tokens": 1000,
      "temperature": 0,
      "stream": True,
    }
    request = requests.post(reqUrl, stream=True, headers=reqHeaders, json=reqBody)
    client = sseclient.SSEClient(request)
    for event in client.events():
        if event.data != '[DONE]':
            txt = json.loads(event.data)['choices'][0]['text']
            yield txt

if __name__ == '__main__':
    for i in performRequestWithStreaming("Can you explain in datail the sino-japanese war"):
        print(i, flush=True, end="")