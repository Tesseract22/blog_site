
from audioop import mul
import re
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from calculator import RecipeMatrix
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
    def __init__(self, recipes:list, alt:list, items:list, raw:list, multiplier:int =10000) -> None:
        self.recipes = recipes
        self.items = items
        self.item_idx_dict = {items[i] : i for i in range(len(items))}
        self.raw = raw
        self.raw_prefix = "raw-"

        tmp_matrix = np.zeros((len(items), len(recipes) + len(alt)))
        self.recipe_names = []
        for col in range(len(recipes)):
            r = recipes[col]
            self.recipe_names.append(r['name'])
            for i in r['ingredients']:
                tmp_matrix[self.item_idx_dict[i[0]], col] = -i[1]
            for i in r['products']:
                tmp_matrix[self.item_idx_dict[i[0]], col] = i[1]
        self.alt_start = len(self.recipe_names)
        for col in range(len(alt)):
            r = alt[col]
            self.recipe_names.append(r['name'])
            for i in r['ingredients']:
                tmp_matrix[self.item_idx_dict[i[0]], self.alt_start + col] = -i[1]
            for i in r['products']:
                tmp_matrix[self.item_idx_dict[i[0]], self.alt_start + col] = i[1]
        self.alt_end = len(self.recipe_names)
        for r in self.raw:
            self.recipe_names.append(self.raw_prefix + r)
        self.multiplier = multiplier
        self.matrix = RecipeMatrix.RecipeMatrix(tmp_matrix, range(self.alt_start, self.alt_end), [self.item_idx_dict[r] for r in self.raw], self.multiplier)
        

    def RecipeArrToNameDict(self, arr) -> dict:
        '''
        Covert a recipe array to human-friendly dict
        
        arr: the index of array correspond to a recipe, and value at that idex determines the weight

        Returns a dict: {(recipe_name) : (weight)}
        
        '''
        return {self.recipe_names[i] : arr[i] for i in range(len(arr) - 1) if arr[i] != 0} # excluding tax

    def RecipesIdxToNameList(self, li:list) -> list:
        '''
        Covert a list of idxes to human-friendly names of recipes
        
        '''
        return [self.recipe_names[i] for i in li]
    
    def SimplePriority(self, priority:list) -> list:
        '''
        Convert names of items to recipe idxes, assuming that these idxes are in raw items
    
        '''
        return [ self.recipe_names.index(self.raw_prefix + p) for p in priority ]

    def ItemsIdxToNameList(self, li:list) -> list:
        '''
        ---NEED DOCUMENTATION---
        
        '''
        return [self.items[i] for i in li]


    def Solve(self, target:dict, priority:list, alt:list=[]) -> np.array:
        '''
        Solve human-readable target and priority and return huamn-readable answer array
        '''
        # turn the dict into numpy array
        target_arr = np.zeros(self.matrix.shape[0] - 1) #excluding tax
        for name, value in target.items():
            if value < 0:
                raise ValueError("Can not produce negative amount of %s"%name)
            target_arr[self.item_idx_dict[name]] = value
        priority_arr = self.SimplePriority(priority)
        alt_arr = np.sort([self.recipe_names.index(a) for a in alt])
        ans = self.matrix.Solve(target_arr, priority_arr, alt_arr)
        x = np.around(ans.x, decimals=5)
        return x / self.multiplier # excluding tax
    
    def ItemsInvolve(self, x:np.array):
        '''
        ---NEED DOCUMENTATION---
        
        '''
        item_idxes = self.matrix.ItemsInvolve(x)
        return self.ItemsIdxToNameList(item_idxes)


    def ItemFlow(self, item:str, x:np.array) -> dict:
        '''
        ---NEED DOCUMENTATION---
        
        '''
        raw_res = self.matrix.ItemFlow(self.item_idx_dict[item], x)
        res = {}
        res['output'] = {}
        for idx, amount in raw_res['output'].items():
            res['output'][self.recipe_names[idx]] = amount
        res['input'] = {}
        for idx, amount in raw_res['input'].items():
            res['input'][self.recipe_names[idx]] = amount
        return res





    def GetRecipe(self, recipe:str) -> dict:
        recipe_i = self.recipe_names.index(recipe)
        raw_res = self.matrix.GetRecipe(recipe_i)
        res = {}
        res['input'] = {}
        res['output'] = {}
        for k, v in raw_res.items():
            if v < 0:
                res['input'][self.items[k]] = -v
            elif v > 0:
                res['output'][self.items[k]] = v
        print(res)
        return res


if __name__ == '__main__':
    pass
