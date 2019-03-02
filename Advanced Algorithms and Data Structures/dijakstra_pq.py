'''
Dijakstra's Algorithm implemented with a Priority Queue.
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
    class PriorityQueue:
        def __init__(self, degree = 2, contents = []):
            self.degree = degree
            self.data = list(contents) # making contents a list ensures that when making two empty priorityQueues they point to different lists, so when one is changed the other does not change. 
            self.size = len(contents)
            
            parentIndex = (self.size-2) // self.degree
            for i in range(parentIndex,-1,-1):
                self.__siftDownFromTo(i, self.size-1)
            
        def __repr__(self):
            return "PriorityQueue(" + str(self.degree) + "," + str(self.data) + ")"
        
        def __str__(self):
            return repr(self)
        
        def __bestChildOf(self, parentIndex, toIndex):
            
            firstChildIndex = parentIndex * self.degree + 1
            endIndex = min(parentIndex * self.degree + self.degree, toIndex)
            
            if firstChildIndex > endIndex:
                return None
            
            # guess and check pattern
            bestChildIndex = firstChildIndex
            
            for k in range(firstChildIndex, endIndex+1):
                if self.data[k] < self.data[bestChildIndex]:
                    bestChildIndex = k
                    
            return bestChildIndex
            
            
        def __siftDownFromTo(self, fromIndex, toIndex):
            parentIndex = fromIndex
            done = False
            
            while not done:
                childIndex = self.__bestChildOf(parentIndex, toIndex)
                
                if childIndex == None:
                    done = True
                    
                elif self.data[parentIndex] > self.data[childIndex]:
                    self.data[parentIndex], self.data[childIndex] = \
                        self.data[childIndex], self.data[parentIndex]
                    
                    parentIndex = childIndex
                    
                else:
                    done = True
                    
        def __siftUp(self,idx):
            childIdx = idx
            
            done = False
            while not done:
                parentIdx = (childIdx-1) // self.degree
                if childIdx == 0:
                    done = True
                elif self.data[parentIdx] > self.data[childIdx]:
                    self.data[parentIdx], self.data[childIdx] = self.data[childIdx], self.data[parentIdx]
                    childIdx = parentIdx
                else:
                    done = True
                
                    
        def isEmpty(self): 
            if self.size == 0:
                return True
            return False    
        
        def dequeque(self):
            firstNode = self.data[0]
            lastNode = self.data[self.size - 1]
            self.data[0] = lastNode
            
            self.data.pop()
            
            self.size -=1        
            self.__siftDownFromTo(0,self.size-1)
            return firstNode
            
        def enqueue(self, item):
            # add to right most avaliable on bottom level
            if self.size <= len(self.data): # number of items in list <= length of list
                self.data.append(item)
                self.size += 1
                
                # sift up
                self.__siftUp(self.size-1)
            
            
    def __init__(self,contents=None):
        self.tree = OrderedTreeSet.PriorityQueue()
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
    def __init__(self,vertexId,x,y,label): # edges=[]
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
    unvisited = OrderedTreeSet.PriorityQueue(2)
    unvisited.enqueue(VertexCost(sourceVertId, 0))
        
    while unvisited.size > 0:
        # find vertex with smallest cost and remove from the tree
        current = unvisited.dequeque()
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
                        unvisited.enqueue(VertexCost(vertexDict[vert2], edge.weight + current.cost))
                        vertexList[vert2] = (edge.weight + current.cost)
                        previous[vert2] = vertexDict[currentId].label
                elif vert2 == currentId:
                    if vertexList[vert1] > (edge.weight + vertexList[currentId]):
                        # add vertex to the unvisited tree so it can be looked at later
                        unvisited.enqueue(VertexCost(vertexDict[vert1], edge.weight + current.cost))
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




