'''
Solving Sudoku using the HashSet class.
Author: Anna Peterson
CS330
Date: 19 Sept 2018
'''

class HashSet:
    class __Placeholder:
        def __init__(self):
            pass
            
        def __eq__(self,other):
            return False
            
    def __add(item,items):
        idx = hash(item) % len(items)
        loc = -1
        
        while items[idx] != None:
            if items[idx] == item:
                # item already in set
                return False
            
            if loc < 0 and type(items[idx]) == HashSet.__Placeholder:
                loc = idx
                
            idx = (idx + 1) % len(items)
            
        if loc < 0:
            loc = idx
            
        items[loc] = item  
        
        return True
    
    def __remove(item,items):
        idx = hash(item) % len(items)
        
        while items[idx] != None:
            if items[idx] == item:
                nextIdx = (idx + 1) % len(items)
                if items[nextIdx] == None:
                    items[idx] = None
                else:
                    items[idx] = HashSet.__Placeholder()
                return True
            
            idx = (idx + 1) % len(items)
            
        return False
        
    def __rehash(oldList, newList):
        for x in oldList:
            if x != None and type(x) != HashSet.__Placeholder:
                HashSet.__add(x,newList)
                
        return newList
    
    def __init__(self,contents=[]):
        self.items = [None] * 10
        self.numItems = 0
        
        for item in contents:
            self.add(item)
          
    def __str__(self):
        result = ""
        for item in self:
            result += str(item) 
        return "{" + result + "}"  
        
    def __iter__(self):
        for i in range(len(self.items)):
            if self.items[i] != None and type(self.items[i]) != HashSet.__Placeholder:
                yield self.items[i]    
            
    def add(self, item):
        if HashSet.__add(item,self.items):
            self.numItems += 1             
            load = self.numItems / len(self.items)
            if load >= 0.75:
                self.items = HashSet.__rehash(self.items,[None]*2*len(self.items))
    def remove(self, item):
        if HashSet.__remove(item,self.items):
            self.numItems -= 1
            load = max(self.numItems, 10) / len(self.items)
            if load <= 0.25:
                self.items = HashSet.__rehash(self.items,[None]*int(len(self.items)/2))
        else:
            raise KeyError("Item not in HashSet")
        
    
    def discard(self,item):
        if item in self:
            self.remove(item)

    def pop(self):
            pass
                
    def clear(self):
        rmlst = []
        for item in self:
            rmlst.append(item)
        for i in rmlst:
            self.remove(i)
            
    def update(self,other):
        for item in other:
            if item not in self:
                self.add(item)    
            
    def intersection_update(self, other):
        rmlst = []
        for item in self:
            if item not in other:
                rmlst.append(item)
        for i in rmlst:
            self.remove(i)
    
    def difference_update(self, other):
        for item in other:
            self.discard(item)
                
    # Following are the accessor methods for the HashSet  
    def __len__(self):
        count = 0
        for i in self:
            count += 1
        return count
    
    def __contains__(self, item):
        idx = hash(item) % len(self.items)
        while self.items[idx] != None:
            if self.items[idx] == item:
                return True
            
            idx = (idx + 1) % len(self.items)
            
        return False
    

            
    def __getitem__(self, item):
        pass      
        
    def not__contains__(self, item):
        pass
    
    def isdisjoint(self, other):
        pass
    
    
    def issubset(self, other):
        pass
            
    
    def issuperset(self, other):
        pass
    
    def union(self, other):
        pass
    
    def intersection(self, other):
        n_set = HashSet(self)
        n_set = intersection_update(other)
        return n_set
    
    def difference(self, other):
        n_set = HashSet(self)
        n_set = difference_update(other)
        return n_set
    
    def symmetric_difference(self, other):
        pass
    
    def copy(self):
        copyList = []
        copy = HashSet()
        for item in self:
            copyList.append(item)
        for i in copyList:
            copy.add(i)
        return copy
    
    def __eq__(self,other):
        for item in self:
            if item not in other:
                return False        
        else:
            if len(self) != len(other):
                return False            
        return True
            
    def __ne__ (self,other):
        return not(self.__eq__(other))    

#Code below creates Sudoku puzzle and makes solution
def reduceGroups(groups):
    changed = True
    while changed:
        changed = False
        for group in groups:
            if reduceGroup(group):
                changed = True
    return groups
                
def reduceGroup(group):
    changed = False
    
    #rule1
    for i in range(0,9):
        compareCell = group[i]
        dupCount = 0
        for cell in group:
            if cell == compareCell:
                dupCount += 1
        if dupCount == len(compareCell):
            for k in group:
                length = len(k)
                if k != compareCell:
                    k.difference_update(compareCell)
                if length > len(k):
                    changed = True
                    
    #rule2
    for i in range(0,9):
        compareCell = group[i]
        copy = compareCell.copy()
        for k in range(0,9):
            if i != k:
                copy.difference_update(group[k])
        if len(copy) == 1:
            compareLength = len(compareCell)
            compareCell.intersection_update(copy)
            if compareLength > len(compareCell):
                changed = True        
            
    return changed
            
            
def createPuzzle(file):
    puzzle = []
    for line in file:
        row = line.split()
        lst = []
        for cell in row:
            if cell == 'x':
                lst.append(HashSet([1,2,3,4,5,6,7,8,9]))
            else:
                lst.append(HashSet([int(cell)]))
        puzzle.append(lst)
    return puzzle
                
def createGroups(puzzle):
    # create rows in the groups
    groups = list(puzzle)
    
    #create columns in the groups
    for i in range(0,9):
        col = []
        for row in puzzle:
            col.append(row[i])
        groups.append(col)
        
    #create squares in the groups
    for i in range(0,9,3):
        for j in range(0,9,3):
            square = []
            for k in range(3):
                for m in range(3):
                    square.append(puzzle[i+k][j+m])
            groups.append(square) 
    return groups
    

def main():
    filename = input("Enter filename of the sudoku puzzle to be solve (sudoku1.txt, sudoku2.txt, sudoku3.txt): ")
    print()
    print("Solving Sudoku")
    file = open(filename, 'r')
    
    puzzle = createPuzzle(file)
    groups = createGroups(puzzle)
    solution = reduceGroups(groups)
    
    for i in range(0,9):
        lines = ''
        for k in range(0,9):
            lines += str(solution[i][k]).strip("{}") + " "
        print(lines)
    
if __name__ == "__main__":
    main()


    
