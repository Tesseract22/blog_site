
from . import RecipeMatrix

import numpy as np
'''
---NEED DOCUMENTATION---
'''

'''
---NEED DOCUMENTATION---
'''
class Calculator:
    '''
    ---NEED DOCUMENTATION---
    '''
    def __init__(self, recipes:list, items:list, raw:list) -> None:
        self.recipes = recipes
        self.items = items
        self.item_idx_dict = {items[i] : i for i in range(len(items))}
        self.raw = raw
        
        tmp_matrix = np.zeros((len(items), len(recipes)))
        self.recipe_names = []
        for col in range(len(recipes)):
            r = recipes[col]
            self.recipe_names.append(r['name'])
            for i in r['ingredients']:
                tmp_matrix[self.item_idx_dict[i[0]], col] = -i[1]
            for i in r['products']:
                tmp_matrix[self.item_idx_dict[i[0]], col] = i[1]
        print("core ")
        for r in self.raw:
            print("raw")
            self.recipe_names.append("raw: " + r)
        self.matrix = RecipeMatrix.RecipeMatrix(tmp_matrix, [self.item_idx_dict[r] for r in self.raw])
    '''
    ---NEED DOCUMENTATION---
    
    '''
    def SimplePriority(self, priority:list) -> list:
        return [ self.recipe_names.index(p) for p in priority ]



    
    '''
    ---NEED DOCUMENTATION---
    
    '''
    def Solve(self, target:dict, priority:list) -> np.array:
        # turn the dict into numpy array
        target_arr = np.zeros(self.matrix.shape[0] - 1) #excluding tax
        for name, value in target.items():
            if value < 0:
                raise ValueError("Can not produce negative amount of %s"%name)
            target_arr[self.item_idx_dict[name]] = value
        priority_arr = self.SimplePriority(priority)
        p = [212, 213, 214, 215, 216, 217, 218, 219, 220, 222]
        ans = self.matrix.Solve(target_arr, priority_arr)
        x = np.around(ans.x, decimals=5)
        return x # excluding tax

    '''
    ---NEED DOCUMENTATION---
    
    '''
    def SolveHuman(self, target:dict, priority:list) -> dict:
        x = self.Solve(target, priority)
        return {self.recipe_names[i] : x[i] for i in range(len(x) - 1) if x[i] != 0} # excluding tax

    '''
    ---NEED DOCUMENTATION---
    
    '''
    def RecipesToItems(self, x:np.array) -> dict:
        pass

    '''
    ---NEED DOCUMENTATION---
    
    '''
    def SolveVisual(self, target:dict, priority:list) -> dict:
        x, _ = self.Solve(target, priority)
        return self.ListVisualize(x)



