from django.shortcuts import render
import json
# Create your views here.
import os
from .Factorio import Factorio
from django.http import HttpResponse
dirname = os.path.dirname(__file__)
with open(dirname + "/Factorio/local/items.json", "r") as f:
    factorio_items = json.load(f)
with open(dirname + "/Factorio/local/raw.json", "r") as f:
    factorio_raw = json.load(f)

f = Factorio.Factorio(Factorio.recipes, Factorio.items, Factorio.raw)


def calculator_main(request):
    ctx = {}
    ctx['factorio_items'] = factorio_items
    ctx['factorio_raw'] = factorio_raw

    return render(request, "calculator/calculator_main.html", ctx)


def update(request):
    ctx = {}
    print("update")
    if request.method == "POST":    
        targets = request.POST['targets']
        priorities = request.POST["priorities"]
        t = json.loads(targets)
        p = json.loads(priorities)
        print(t, p)
        ans = f.SolveHuman(t, p)
        print(ans)
        return HttpResponse(json.dumps(ans), content_type="application/json")
    return HttpResponse(json.dumps({}), content_type="application/json")

