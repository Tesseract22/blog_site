import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from calculator import Core
import os
import json


dirname = os.path.dirname(__file__)
ITEMS_PATH = os.path.join(dirname, "local/items.json")
RECIPES_PATH = os.path.join(dirname, "local/recipes.json")
alt = []
raw = [
   "limestone",
   "iron-ore",
   "copper-ore",
   "caterium-ore",
   "coal",
   "raw-quartz",
   "sulfur",
   "bauxite",
   "uranium",
   "water",
   "crude-oil",
   "nitrogen-gas"
]
miss = ["alien-carapace", 'alien-organs']
with open(RECIPES_PATH, 'r') as f:
    recipes = json.load(f)
# print(recipes)
with open(ITEMS_PATH, 'r') as f:
    items = json.load(f)
items.extend(miss)
# -------------------------------------------------------------------
class Satisfactory(Core.Calculator):
    pass



if __name__ == "__main__":
    # print(recipes)
    s = Satisfactory(recipes, items, raw)
    # print(items)
    target = {}
    target['Motor'] = 5
    target['Encased Industrial Beam'] = 5
    p = ['Copper Ore', 'Iron Ore', 'Caterium Ore', 'Crude Oil']
    
    ans = s.Solve(target, p)
    print(ans)
    pass