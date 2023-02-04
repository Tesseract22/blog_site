import os, sys
sys.path.insert(0, os.path.abspath("."))

from django.shortcuts import render
from django.http import HttpResponse
import json

from . import Core



def main(request):
    ctx = {}
    ctx['items'] = FC.items
    ctx['raw'] = FC.raw
    ctx['alt'] = [r['name'] for r in FC.alt]
    ctx['game'] = 'factorio'
    ctx['img_type'] = '.webp'

    dirname = os.path.dirname(__file__)
    ITEMS_PATH = os.path.join(dirname, "local/items.json")
    RECIPES_PATH = os.path.join(dirname, "local/recipes.json")
    OLD_PATH = os.path.join(dirname, "local/item_list.json")
    ALT_PATH = os.path.join(dirname, 'local/alt.json')

    with open(RECIPES_PATH, 'r') as f:
        recipes = json.load(f)
    # print(recipes)
    with open(ITEMS_PATH, 'r') as f:
        items = json.load(f)
    with open(ALT_PATH, 'r') as f:
        alt = json.load(f)
    return render(request, "calculator/factorio.html", ctx)