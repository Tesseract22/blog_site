import os, sys
sys.path.insert(0, os.path.abspath("."))

from django.shortcuts import render
from django.http import HttpResponse
import json

from calculator.Factorio import Factorio as FC



dirname = os.path.dirname(__file__)


f = FC.Factorio(FC.recipes, FC.items, FC.raw)


def calculator_main(request):
    ctx = {}
    ctx['factorio_items'] = FC.items
    ctx['factorio_raw'] = FC.raw

    return render(request, "calculator/calculator_main.html", ctx)


def update(request):
    res = {}
    print("update")
    if request.method == "POST":    
        targets = request.POST['targets']
        priorities = request.POST["priorities"]
        t = json.loads(targets)
        p = json.loads(priorities)
        print(t, p)
        raw_x = f.Solve(t, p)
        ans = f.RecipeArrToNameDict(raw_x)
        res['ans'] = ans
        items = f.ItemsInvolve(raw_x)
        res['items'] = [(i.replace('-', ' ')).title() for i in items]

        print(res)
        return HttpResponse(json.dumps(res), content_type="application/json")
    return HttpResponse(json.dumps({}), content_type="application/json")

if __name__ == '__main__':
    pass