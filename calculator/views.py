from django.shortcuts import render
import json
# Create your views here.
import os


dirname = os.path.dirname(__file__)
with open(dirname + "/Factorio/local/items.json", "r") as f:
    factorio_items = json.load(f)
with open(dirname + "/Factorio/local/raw.json", "r") as f:
    factorio_raw = json.load(f)


def calculator_main(request):
    f_li = []
    f_li.append("radar")
    f_li.append("file")
    ctx = {}
    ctx['factorio_items'] = factorio_items
    ctx['factorio_raw'] = factorio_raw
    if request.POST:    
        pass
    ctx['factorio_li'] = f_li
    return render(request, "calculator/calculator_main.html", ctx)

