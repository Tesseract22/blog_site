import os, sys
sys.path.insert(0, os.path.abspath("."))

from django.shortcuts import render
from django.http import HttpResponse
import json
import re
from calculator.Factorio import Factorio as FC



dirname = os.path.dirname(__file__)


f = FC.Factorio(FC.recipes, FC.alt, FC.items, FC.raw)


def main(request):
    ctx = {}
    ctx['items'] = FC.items
    ctx['raw'] = FC.raw
    ctx['alt'] = [r['name'] for r in FC.alt]
    ctx['game'] = 'factorio'
    ctx['img_type'] = '.webp'
    return render(request, "calculator/factorio.html", ctx)


def update(request):
    res = {}
    print("update")
    if request.method == "POST":    
        targets = request.POST['targets']
        priorities = request.POST["priorities"]
        alt = request.POST['alt']
        t = json.loads(targets)
        p = json.loads(priorities)
        a = json.loads(alt)
        print(t, p)
        raw_x = f.Solve(t, p, a)
        ans = f.RecipeArrToNameDict(raw_x)
        res['ans'] = ans
        items = f.ItemsInvolve(raw_x)
        res['items'] =  {(i.replace('-', ' ')).title() : f.ItemFlow(i, raw_x) for i in items}

        print(res)
        return HttpResponse(json.dumps(res), content_type="application/json")
    return HttpResponse(json.dumps({}), content_type="application/json")

def get_recipe(request):
    recipe_name = request.POST['recipe_name']
    return HttpResponse(json.dumps(f.GetRecipe(recipe_name)), content_type="application/json")



if __name__ == '__main__':
    pass