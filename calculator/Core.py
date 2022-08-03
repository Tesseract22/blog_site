
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
        self.recipe_names.extend(self.raw)
        
        self.matrix = RecipeMatrix.RecipeMatrix(tmp_matrix, [self.item_idx_dict[r] for r in self.raw])

    '''
    ---NEED DOCUMENTATION---
    
    '''
    def SimplePriority(self, priority:list) -> list:
        return [ self.recipe_names.index(p) for p in priority ]



    
    '''
    ---NEED DOCUMENTATION---
    
    '''
    def Solve(self, target:dict, priority:list) -> dict:
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
        return {self.recipe_names[i] : x[i] for i in range(len(x) - 1) if x[i] != 0} # excluding tax

    '''
    ---NEED DOCUMENTATION---
    
    '''
    def ListVisualize(self, x:np.array) -> dict:
        res = {}
        for i in range(len(x) - 1):
            if x[i] == 0:
                continue
            r = x[i] * self.matrix[:, i]
            for j in range(len(r) - 1):
                item_val = r[j]
                if item_val == 0:
                    continue
                item_name = self.items[j]
                if item_name not in res.keys():
                    res[item_name] = ({}, {},)
                if item_val > 0:
                    res[item_name][0][self.recipe_names[i]] = item_val
                else:
                    res[item_name][1][self.recipe_names[i]] = item_val
        return res

    '''
    ---NEED DOCUMENTATION---
    
    '''
    def SolveVisual(self, target:dict, priority:list) -> dict:
        x, _ = self.Solve(target, priority)
        return self.ListVisualize(x)



