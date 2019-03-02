'''
Dijakstra's Algorithm implemented with an Ordered Tree Set.
Author: Anna Peterson
CS360
'''

import random
import stack
from xml.dom import minidom
import sys
import turtle
import operator

class OrderedTreeSet:
    class BinarySearchTree:
        # This is a Node class that is internal to the BinarySearchTree class. 
        class Node:
            def __init__(self,val,left=None,right=None):
                self.val = val
                self.left = left
                self.right = right
                
            def getVal(self):
                return self.val
            
            def setVal(self,newval):
                self.val = newval
                
            def getLeft(self):
                return self.left
            
            def getRight(self):
                return self.right
            
            def setLeft(self,newleft):
                self.left = newleft
                
            def setRight(self,newright):
                self.right = newright        

            def __repr__(self):
                return "BinarySearchTree.Node(" + repr(self.val) + "," + repr(self.left) + "," + repr(self.right) + ")"  
            
            #def __iter__(self):
                #if self.left != None:
                    #for elem in self.left:
                        #yield elem
                        
                #yield self.val
                
                #if self.right != None:
                    #for elem in self.right:
                        #yield elem             
                
        # Below are the methods of the BinarySearchTree class. 
        def __init__(self, root=None):
            self.root = root
            
        def insert(self,val):
            self.root = OrderedTreeSet.BinarySearchTree.__insert(self.root,val)
            
        def __insert(root,val):
            if root == None:
                return OrderedTreeSet.BinarySearchTree.Node(val)
            
            if val < root.getVal():
                root.setLeft(OrderedTreeSet.BinarySearchTree.__insert(root.getLeft(),val))
            else:
                root.setRight(OrderedTreeSet.BinarySearchTree.__insert(root.getRight(),val))
                
            return root
        
        #write delete here (similar to insert)
        
        def delete(self,val):
            self.root = OrderedTreeSet.BinarySearchTree.__delete(self.root,val)

        def __delete(root,val):
            if root == None:
                return None
            
            if val < root.getVal():
                root.setLeft(OrderedTreeSet.BinarySearchTree.__delete(root.getLeft(),val))
                
            elif val > root.getVal():
                root.setRight(OrderedTreeSet.BinarySearchTree.__delete(root.getRight(),val))             
                
            else:
                if val == root.getVal():
                #Case1: no children
                    if root.getLeft() == None and root.getRight() == None:
                    #return an empty tree (i.e. None)
                        return None
                
                #Case2: one child (right)
                if root.getLeft() == None:
                    rightVal = root.getRight()
                    root = None
                    return rightVal
                 
                #Case2: one child (left)   
                if root.getRight() == None:
                    leftVal = root.getLeft()
                    root = None
                    return leftVal
                
                #Case4: 2 children
                if root.getRight() != None and root.getLeft() != None:
                    #find right most value of the left tree or the left most value of the right subtree
                    rightMostVal = OrderedTreeSet.BinarySearchTree.getMin(root,root.getLeft())
                    root.val = rightMostVal.getVal()
                    root.left = OrderedTreeSet.BinarySearchTree.__delete(root.getLeft(), rightMostVal.getVal())
                 
            return root
            
        def getSmallest(self,val):
            temp = val
            while temp.getRight() != None:
                temp = temp.getRight()
            return temp
        
        
        #recurisive iterator 
        #def __iter__(self):
            #if self.root != None:
                #return iter(self.root)
            #else:
                #return iter([])
            
        #write non-recurive iteration here
        def __iter__(self):
            if self.root != None:
                current = self.root
                s = stack.Stack()
                found = False
                while not found:
                    if current is not None:
                        s.push(current)
                        current = current.getLeft()
                    else:
                        if (s.size() > 0):
                            current = s.pop()
                            yield current.getVal()
                            current = current.getRight()
                        else:
                            found = True
            else:
                return iter([])
            

        def __str__(self):
            return "BinarySearchTree(" + repr(self.root) + ")"
            
    def __init__(self,contents=None):
        self.tree = OrderedTreeSet.BinarySearchTree()
        if contents != None:
            # randomize the list
            indices = list(range(len(contents)))
            random.shuffle(indices)
            
            for i in range(len(contents)):
                self.tree.insert(contents[indices[i]])
                
            self.numItems = len(contents)
        else:
            self.numItems = 0
            
    def __str__(self):
        pass
    
    def __iter__(self):
        return iter(self.tree)
    
    # Following are the mutator set methods 
    def add(self, item):
        self.tree.insert(item)
                
    def remove(self, item):
        if item in self.tree:
            self.tree.delete(item)
        else:
            raise Exception("Value not found")
        
    def discard(self, item):
        if item in self.tree:
            self.remove(item)
            
    def pop(self):
        pass
            
    def clear(self):
        rmlst = []
        for item in self.tree:
            rmlst.append(item)
        for i in rmlst:
            self.remove(i)
        
    def update(self, other):
        for item in other:
            if item not in self.tree:
                self.add(item) 
            
    def intersection_update(self, other):
        rmlst = []
        for item in self.tree:
            if item not in other.tree:
                rmlst.append(item)
        for i in rmlst:
            self.remove(i)
            
    def difference_update(self, other):
        for item in other.tree:
            self.discard(item)  
                
    def symmetric_difference_update(self, other):
        pass
                
    # Following are the accessor methods for the HashSet  
    def __len__(self):
        count = 0
        for i in self:
            count += 1
        return count
    
    def __contains__(self, item):
        root = self.tree.root
        found = True
        while found:
            if root.getVal() == item:
                return True
            
            if root.getVal() > item:
                root = root.getLeft()
                if root == None:
                    found = False
                
            if root.getVal() < item:
                root = root.getRight()
                if root == None:
                    found = False
                
        return found
        
    
    # One extra method for use with the HashMap class. This method is not needed in the 
    # HashSet implementation, but it is used by the HashMap implementation. 
    def __getitem__(self, item):
        pass      
        
    def not__contains__(self, item):
        return not(self.__contains__(item))
    
    def isdisjoint(self, other):
        pass
    
    
    def issubset(self, other):
        result = True
        for x in other.tree:
            if x in self.tree:
                result = True
            else:
                result = False
        return result
    
    def issuperset(self, other):
        result = True
        for x in self.tree:
            if x in other.tree:
                result = True
            else:
                result = False
        return result
    
    def union(self, other):
        pass
    
    def intersection(self, other):
        pass
    
    def difference(self, other):
        lst = []
        for item in self:
            lst.append(item)
        n_tree = OrderedTreeSet(lst)
        n_tree.difference_update(other)
        return n_tree        
    
    def symmetric_difference(self, other):
        pass
    
    def copy(self):
        copyList = []
        copy = OrderedTreeSet()
        for item in self:
            copyList.append(item)
        for i in copyList:
            copy.add(i)
        return copy        
    
    # Operator Definitions
    def __or__(self, other):
        pass
    
    def __and__(self,other):
        pass
    
    def __sub__(self,other):
        pass
    
    def __xor__(self,other):
        pass
    
    def __ior__(self,other):
        pass
    
    def __iand__(self,other):
        pass
    
    def __ixor(self,other):
        pass    
    
    def __le__(self,other):
        pass
    
    def __lt__(self,other):
        pass
    
    def __ge__(self,other):
        pass
    
    def __gt__(self,other):
        pass
    
    def __eq__(self,other):
        for item in self.tree:
            if item not in other.tree:
                return False        
        else:
            if len(self) != len(other):
                return False            
        return True      
    
    def __ne__ (self,other):
        return not(self.__eq__(other))       
                
    def __str__(self):
        return "OrderedTreeSet(" + self.tree.__str__() + ")"   
    
    def getSmallest(self):
        val = self.tree.root
        while val.getLeft() != None:
            val = val.getLeft()
        self.tree.delete(val.getVal())
        return val.getVal()    

class Vertex:
    def __init__(self,vertexId,x,y,label, edges=[]):
        self.vertexId = vertexId
        self.x = x
        self.y = y
        self.label = label
        # self.edges = edges
        
    def getVertexId(self, vertex):
        return self.vertexId
        
class Edge:
    def __init__(self,v1,v2,weight=0):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight
        
    def getVertices(self):
        return (self.v1,self.v2)    
    
    def __lt__(self, other):
        if type(self) != type(other):
            raise Exception("Unorderable types")
        return self.weight < other.weight 
    
class VertexCost():
    def __init__(self, vertexId, cost):
        self.vertexId = vertexId
        self.cost = cost
        
    def __lt__(self,other):
        if type(self) != type(other):
            raise Exception("Unorderable types: cannot compare")
        return self.cost < other.cost
    
    def __gt__(self,other):
        if type(self) != type(other):
            raise Exception("Unorderable types: cannot compare")
        return self.cost > other.cost        

 
def main():  
    xmldoc = minidom.parse("graph.xml")
    
    graph = xmldoc.getElementsByTagName("Graph")[0]
    vertices = graph.getElementsByTagName("Vertices")[0].getElementsByTagName("Vertex")
    edges = graph.getElementsByTagName("Edges")[0].getElementsByTagName("Edge")
    
    width = float(graph.attributes["width"].value)
    height = float(graph.attributes["height"].value)
    
    #t = turtle.Turtle()
    #screen = t.getscreen()
    #screen.setworldcoordinates(0,height,width,0)
    #t.speed(100)
    #t.ht()
    vertexDict = {}
    
    for vertex in vertices:
        vertexId = int(vertex.attributes["vertexId"].value)
        x = float(vertex.attributes["x"].value)
        y = float(vertex.attributes["y"].value)
        label = vertex.attributes["label"].value
        v = Vertex(vertexId, x, y, label)
        vertexDict[vertexId] = v
        #print("added", label)
        
    edgeList = []
    
    for edge in edges:
        anEdge = Edge(int(edge.attributes["head"].value), int(edge.attributes["tail"].value))
        if "weight" in edge.attributes:       
            anEdge.weight = float(edge.attributes["weight"].value) 
        edgeList.append(anEdge)



    #Dijakstra's Algorithm
    
    vertexList = []
    previous = []   
    
    for vertex in vertices:
        vertexList.insert(vertexId, float("inf"))
        previous.insert(vertexId, -1)    
    
    for vertex in vertexDict:
        if vertexDict[vertex].label == '0':
            sourceVertId = vertexDict[vertex]
            vertexList[vertex] = 0  
            previous[vertex] = 0            
            
    visited = set()
    visited.add(sourceVertId.vertexId)
    unvisited = OrderedTreeSet()
    unvisited.add(VertexCost(sourceVertId, 0))
        
    while len(unvisited) > 0:
        # find vertex with smallest cost and remove from the tree
        current = unvisited.getSmallest()
        currentId = current.vertexId.vertexId
        
        #check if in visited
        if current not in visited:
        # find adjacent vertices to current
            for edge in edgeList:
                vert1, vert2 = edge.getVertices()
                
                # if the vertex equals the current vertex, check edge weights and update values to be the smallest path(cost)
                if vert1 == currentId:
                    if vertexList[vert2] > (edge.weight + vertexList[currentId]):
                        # add vertex to the unvisited tree so it can be looked at later
                        unvisited.add(VertexCost(vertexDict[vert2], edge.weight + current.cost))
                        vertexList[vert2] = (edge.weight + current.cost)
                        previous[vert2] = vertexDict[currentId].label
                elif vert2 == currentId:
                    if vertexList[vert1] > (edge.weight + vertexList[currentId]):
                        # add vertex to the unvisited tree so it can be looked at later
                        unvisited.add(VertexCost(vertexDict[vert1], edge.weight + current.cost))
                        vertexList[vert1] = (edge.weight + current.cost)
                        previous[vert1] = vertexDict[currentId].label
                          
        visited.add(currentId)
    
    
    for i in range(30):
        for vertex in vertexDict:
            if str(i) == vertexDict[vertex].label:
                print('Vertex:')
                print('    label: ' + vertexDict[vertex].label)
                print('    cost: ' + str("{:.2f}".format(vertexList[vertex])))
                print('    previous: ' + str(previous[vertex]))

if __name__ == "__main__":
    main()


