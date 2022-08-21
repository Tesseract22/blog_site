
from scipy.optimize import linprog
import numpy as np






'''
Add a pseudo, cost-free recipe in the matrix for matrix 
matrix: the matrix that needed to be added
raw_idx: the designated idx of the raw_material in the matrix
Returns the new matrix with the pseudo recipe
'''
def AddRaw(matrix: np.array, raw_idx: int) -> np.array:
    new_col = np.zeros((matrix.shape[0], 1)) # row length
    new_col[raw_idx] = 1
    return np.append(matrix, new_col, axis=1)



'''
Find the location of resources that needed to be add as waste (result of a recipe that has more than one result).
matrix: 
Returns the idx in list
''' 
def FindWaste(matrix:np.array) -> list:
    res = []
    for col in range(matrix.shape[1]):
        potential_res = []
        c = 0
        for row in range(matrix.shape[0]):
            if matrix[row, col] > 0:
                c += 1
                potential_res.append(row)
        if c >= 2:
            res.extend(potential_res) 
    return list(set(res))

'''
Add the pseudo "taxes" item and recipe to the matrix. Tax are used to decrease the excess in output, which have the lowest priority by default.
matrix:
Returns the new matrix
'''
def AddTaxes(matrix:np.array):
    # Add a pseudo item in matrix. All recipes would consume 1 unit of tax.
    # It is not neccessary to add tax for pseudo raw input recipes, but here we do it anyway
    new_row = -np.ones((1, matrix.shape[1]))
    matrix = np.append(matrix, new_row, axis=0)

    # We here treat tax has raw input item. -1 represents the last row, which is the tax item we just added.
    matrix = AddRaw(matrix, -1)

    # In LP we would set the balance of tax to 0, meaning we would never have excess in taxes.
    # Later we woild put the pseudo input taxes recipe in object function with the lowest priority.
    return matrix




class RecipeMatrix:

    '''
    A wrapper for 2d-numpy-array
    self.matrix: the matrix where we perform all the operations. Notice that it should have different shape as the original matrix
    self.orginal_raw_idxes: store the indexes of raw input items in the row
    self.raw_idxes: store the indexes of pseudo raw input recipes in the col
    '''


    def __init__(self, matrix:np.array, alt_idx:tuple, raw_idxes:list, multiplier:int) -> None:
        '''
        Initialize the object, add pseduo recipe and locate alt recipes in the matrix
        self:
        matrix: the recipe matrix, or graph matrix
        raw_idxes: the idxes have the elment you want to appoint as raw material
        multiplier: an int that would multiply target and divide results. This clear edge behavior regarding tax
        '''
        self.matrix = np.copy(matrix)
        self.raw_idxes = []
        for i in raw_idxes:
            self.raw_idxes.append(self.matrix.shape[1])
            self.matrix = AddRaw(self.matrix, i)
        
        # Add taxes to all recipe
        self.matrix = AddTaxes(self.matrix)
        self.alt_idx = alt_idx
        self.shape = self.matrix.shape
        
        self.multiplier = multiplier

    
    def ObjFunc(self, priority:list, level_ratio=10) -> np.array:
        '''
        Constructs the object function with priority list. The item on the higher level would have 10x the "value" of the lower level.
        priority: only one item per level. ITEM IN LIST MUST ALSO BE IN self.raw_idxes
        level_ration: determines the difference between levels; default value = 10.
        Returns the object functon params.
        '''
        # scipy default set to minimize object function, so no need to inverse sign
        l = len(priority)
        res = np.zeros(self.matrix.shape[1])
        for i in range(l):
            p = priority[i]
            if p not in self.raw_idxes:
                raise KeyError("Item %i not in self.raw_idxes"%p)
            res[p] = pow(level_ratio, l - i)
        # Put a minimal value to raw recipe
        for r in self.raw_idxes:
            res[r] = max(res[r], 5)
        # tax
        res[-1] = 1
        return res

   
    def Inequalities(self, target:np.array, alt:list) -> np.array:
        '''
        Construc the left and right inequalities for LP.
        target: used to construct right hand inequalities
        alt: the alternate recipes availiable
        Returns two matrix, representing each ineq.
        '''
        # scipy default set to less or equal to, <=, but we want >=
        # so we need to multiply our result by -1
        
        # Everythng in the matrix except the last row
        alt_matrix = np.copy(self.matrix)
        j = 0
        print(alt, self.alt_idx)
        for col in self.alt_idx:
            if j < len(alt) and alt[j] == col:
                j += 1
            else:
                print("a")
                alt_matrix[:-1,col] = 0
        lhs_ineq = -alt_matrix[:-1, :]
        # Just the target
        rhs_ineq = -target * self.multiplier
        return lhs_ineq, rhs_ineq


    
    def Equalities(self) -> np.array:
        '''
        Construc the left and right equalities for LP. The only one we need here is tax equality.
        Returns two matrix, representing each eq.
        '''
        # TAXES!
        lhs_eq = [self.matrix[-1, :]]
        rhs_eq = [0]
        return lhs_eq, rhs_eq



    
    def Solve(self, target, priority, alt:list):
        '''
        Solving the problem with linear programming.
        target: the desire output in a np.array
        priority: the prioritiy used to construct the object function params
        Returns the amount needed for each recipe in an array.
        '''
        lhs_ineq, rhs_ineq = self.Inequalities(target, alt)
        lhs_eq, rhs_eq = self.Equalities()
        obj_func = self.ObjFunc(priority)
        # the bound of x_i, are by default 0 - inf
        opt = linprog(c=obj_func, A_ub=lhs_ineq, b_ub=rhs_ineq, A_eq=lhs_eq, b_eq= rhs_eq, method="highs")
        return opt

    def ItemsInvolve(self, x:np.array) -> list:
        '''
        Find the items involve in the given recipe weights
        x: the recipe weights array
        Returns a list of the correspoding idx of the items invloved.
        '''
        items = []
        for i in range(self.shape[0] - 1): # ignore tax
            for j in range(self.shape[1]):
                if x[j] != 0 and self.matrix[i][j] != 0:
                    items.append(i)
                    break
        return items
    
    def ItemFlow(self, item:int, x:np.array) -> dict:
        '''
        '''
        res = {}
        res['input'] = {}
        res['output'] = {}
        item_row = self.matrix[item]
        for i in range(len(item_row) - 1): #ignore tax
            t  = x[i] * item_row[i]
            if t < 0:
                res["output"][i] = -t
            elif t > 0:
                res['input'][i] = t
        return res
    def PrintAns(self, ans, recipe_name_list):
        '''
        ---debug---
        '''
        for i in range(len(ans)):
            if ans[i] == 0:
                continue
            if i < len(recipe_name_list):
                print(recipe_name_list[i], ans[i])
            elif i in self.waste_idxes:
                print(i, ans[i])
            elif i in self.raw_idxes:
                print(i, ans[i])

    def GetRecipe(self, recipe:int) -> dict:
        print(recipe)
        return {index : self.matrix[index, recipe] for index in np.where(self.matrix[:-1, recipe] != 0)[0]}
            
    







if __name__ == "__main__":

    '''
    This is a test scene toke from the game factrio
    item: heavy, light, gas, water, oil
    raw: water, oil
    recipe:
        40 heavy + 30 water = 30 light
        30 light + 30 water = 20 gas
        100 oil = 30 heavy + 30 light + 40 gas
        100 oil + 50 water = 10 heavy + 45 light + 55 gas
    Multiple recipe for one item
    '''

    A1 = np.array([
        [-40, 0, 30, 10],
        [30, -30, 30, 45],
        [0, 20, 40, 55],
        [-30, -30, 0, -50],
        [0, 0, -100, -100],
    ])
    # 300 gas
    b = np.array([0, 0, 300, 0, 0])
    p = [5 ,4] # oil > water

    rm = RecipeMatrix(A1, [3, 4])
    print(rm.matrix.shape)

    ans = rm.Solve(b, p)
    print(ans.x)
    print(rm.matrix @ ans.x)

    
