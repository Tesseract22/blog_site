
import json
import os
dirname = os.path.dirname(__file__)
ITEMS_PATH = os.path.join(dirname, "local/items.json")
RECIPES_PATH = os.path.join(dirname, "local/recipes.json")

with open(RECIPES_PATH, 'r') as f:
    r = json.load(f)

PATH = os.path.join(dirname, "local/items_.json")

new_r = []
for k, v in r.items():
    recipe = {}
    recipe['name'] = k
    recipe['ingredients'] = []
    recipe['products'] = []
    for item, amount in v[0].items():
        recipe['ingredients'].append([item, amount])
    for item, amount in v[1].items():
        recipe['products'].append([item, amount]) 
    new_r.append(recipe)
print(new_r)

with open(PATH, 'w') as f:
    json.dump(new_r, f)