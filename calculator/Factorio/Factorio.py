import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from calculator import Core
import os
import json

'''
---NEED DOCUMENTATION---
'''
fluid = ["crude-oil", "light-oil", "heavy-oil", "lubricant", "petroleum-gas", "sulfuric-acid", "water", "steam"]
ban = ['dummy-steel-axe', 'blueprint', 'deconstruction-planner', 'upgrade-planner', 'blueprint-book', 'copy-paste-tool', 'cut-paste-tool',
  'coin', 'tank-machine-gun', 'vehicle-machine-gun', 'tank-flamethrower', 'artillery-wagon-cannon', 'spidertron-rocket-launcher-1', 'spidertron-rocket-launcher-2',
   'spidertron-rocket-launcher-3', 'spidertron-rocket-launcher-4', 'tank-cannon', 'player-port', 'item-unknown', 'linked-chest', 'heat-interface', 'linked-belt',
    'infinity-chest', 'infinity-pipe', 'selection-tool', 'item-with-inventory', 'item-with-label', 'item-with-tags', 'simple-entity-with-force', 'simple-entity-with-owner', 'burner-generator', "space-science-pack"]
raw = [
   "crude-oil",
   "water",
   "wood",
   "coal",
   "stone",
   "iron-ore",
   "copper-ore",
   "uranium-ore",
   "raw-fish",
#    "used-up-uranium-fuel-cell",
   "steam"
]
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
'''
---NEED DOCUMENTATION---
'''

class Factorio(Core.Calculator):

    pass


if __name__ == '__main__':
    
    f = Factorio(recipes, alt, items, raw)
    target = {}
    target['iron-plate'] = 10
    priority = ["iron-ore", "copper-ore", "coal", "crude-oil", "wood",]
    x = f.Solve(target, priority, ['basic-oil-processing'])
    ans = f.RecipeArrToNameDict(x)
    # items = f.ItemsInvolve(x)
    # print(items)
    # new = []
    # new.extend(fluid)
    # for i in items:
    #     if i not in ban:
    #         new.append(i)
    f.GetRecipe("iron-plate")


