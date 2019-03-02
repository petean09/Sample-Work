'''
This module provides the AVLNode and AVLTree classes.
Author: Anna Peterson
CS360
'''
import random

class Stack:
    def __init__(self):
        self.items = []
        
    def size(self):
        return len(self.items)
        
    def pop(self):
        if self.isEmpty():
            raise RuntimeError("Attempt to pop an empty stack")
        
        topIdx = len(self.items)-1
        item = self.items[topIdx]
        del self.items[topIdx]
        return item
    
    def push(self,item):
        self.items.append(item)
        
    def top(self):
        if self.isEmpty():
            raise RuntimeError("Attempt to get top of empty stack")
        
        topIdx = len(self.items)-1
        return self.items[topIdx]
    
    def isEmpty(self):
        return len(self.items) == 0

    def clear(self):
        self.items = []

class AVLNode:
    def __init__(self, item, balance = 0, left = None, right= None):
        self.item = item
        self.left = None
        self.right = None
        self.balance = balance
      
    def __str__(self):
        '''  This performs an inorder traversal of the tree rooted at self, 
        using recursion.  Return the corresponding string.
        '''
        st = str(self.item) + ' ' + str(self.balance) + '\n'
        if self.left != None:
            st = str(self.left) +  st  # A recursive call: str(self.left)
        if self.right != None:
            st = st + str(self.right)  # Another recursive call
        return st
    
    def __repr__(self):
        return "AVLTree.AVLNode("+repr(self.item)+",balance="+repr(self.balance)+",left="+repr(self.left)+",right="+repr(self.right)+")"
    
    def __iter__(self):
        if self.left != None:
            for elem in self.left:
                yield elem
                
        yield self
        
        if self.right != None:
            for elem in self.right:
                yield elem      
    
    def depth(self):
        # return the depth of the node.
        if self.left == None or self.right == None:
            return 1
        return 1+max(self.left.depth(), self.right.depth())    
     
    def rotateLeft(self):
        '''  Perform a left rotation of the subtree rooted at the
         receiver.  Answer the root node of the new subtree.  
        '''
        child = self.right
        if (child == None):
            print( 'Error!  No right child in rotateLeft.' )
            return None  # redundant
        else:
            self.right = child.left
            child.left = self
            return child
  
    def rotateRight(self):
        '''  Perform a right rotation of the subtree rooted at the
         receiver.  Answer the root node of the new subtree.  
        '''
        child = self.left
        if (child == None):
            print( 'Error!  No left child in rotateRight.' )
            return None  # redundant
        else:
            self.left = child.right
            child.right = self
            return child
  
    def rotateRightThenLeft(self):
        '''Perform a double inside left rotation at the receiver.  We
         assume the receiver has a right child (the bad child), which has a left 
         child. We rotate right at the bad child then rotate left at the pivot 
         node, self. Answer the root node of the new subtree.  We call this 
         case 3, subcase 2.
        '''
        badChild = self.right
        self.right = badChild.rotateRight()
        self = self.rotateLeft()
        return self
        
       
    def rotateLeftThenRight(self):
        '''Perform a double inside right rotation at the receiver.  We
         assume the receiver has a left child (the bad child) which has a right 
         child. We rotate left at the bad child, then rotate right at 
         the pivot, self.  Answer the root node of the new subtree. We call this 
         case 3, subcase 2.
        '''
        badChild = self.left
        self.left = badChild.rotateLeft()
        self = self.rotateRight()
        return self
     
class AVLTree:
    def __init__(self,root=None, count=0):
        self.root = root
        self.count = 0
        
    def __str__(self):
        st = 'There are ' + str(self.count) + ' nodes in the AVL tree.\n'
        return  st + str(self.root)  # Using the string hook for AVL nodes
    
    #implement check function to check the balance of a node. raise exception
    def check(self):
        for node in self:
            if node.left != None and node.right != None:
                dLeft = node.left.depth()
                dRight = node.right.depth()                    
                if dRight - dLeft != node.balance:
                    print(self)
                    raise Exception("Tree balance incorrect")  
                
            else:
                if node.left != None or node.right != None:
                    if node.left == None:
                        dRight = node.right.depth()
                        dLeft = 0
                        if dRight - dLeft != node.balance:
                            print(self)
                            raise Exception("Tree balance incorrect")
                    if node.right == None:
                        dLeft = node.left.depth()
                        dRight = 0
                        if dRight - dLeft != node.balance:
                            print(self)
                            raise Exception("Tree balance incorrect")  
                     
    def __iter__(self):
        if self.root != None:
            return iter(self.root)
        else:
            return iter([])          
    
    def insert(self, newItem):
        '''  Add a new node with item newItem, if there is not a match in the 
          tree.  Perform any rotations necessary to maintain the AVL tree, 
          including any needed updates to the balances of the nodes.  Most of the 
          actual work is done by other methods.
        '''
        pivot, pathStack, parent, found = self.search(newItem)
        
        if found == True:
            raise Exception("Value already in AVLTree")
        
        # insert new item of its not already in the tree
        if parent == None:
            self.root = AVLNode(newItem,0)
            
        elif parent.item > newItem:
            parent.left = AVLNode(newItem,0)
            
        else:   
            parent.right = AVLNode(newItem,0)
            
        self.count += 1
           
        #case1 - no pivot
        if pivot == None:
            self.case1(pathStack, pivot, newItem)
            
        #case2
        elif (pivot.balance > 0 and pivot.item > newItem) or (pivot.balance < 0 and pivot.item < newItem):
            self.case2(pathStack, pivot, newItem)  
            
        #case3
        else:
            self.case3(pathStack, pivot, newItem) 
            
        #self.check()
               
  
    def adjustBalances(self, theStack, pivot, newItem):
        '''  We adjust the balances of all the nodes in theStack, up to and
           including the pivot node, if any.  Later rotations may cause
           some of the balances to change.
        '''
        done = False
        while not done:
            node = theStack.pop()
            if newItem < node.item:
                #decrease balance
                node.balance -= 1
            else:
                #increase balance
                node.balance += 1
                
            if theStack.isEmpty() or node == pivot:
                done = True
            
        
    def case1(self, theStack, pivot, newItem):
        '''  There is no pivot node.  Adjust the balances of all the nodes
           in theStack.
        '''
        self.adjustBalances(theStack, pivot, newItem)
              
    def case2(self, theStack, pivot, newItem):
        ''' The pivot node exists.  We have inserted a new node into the
           subtree of the pivot of smaller height.  Hence, we need to adjust 
           the balances of all the nodes in the stack up to and including 
           that of the pivot node.  No rotations are needed.
        '''
        self.adjustBalances(theStack, pivot, newItem)
              
    def case3(self, theStack, pivot, newItem):
        '''  The pivot node exists.  We have inserted a new node into the
           larger height subtree of the pivot node.  Hence rebalancing and 
           rotations are needed.
        '''
        self.adjustBalances(theStack, pivot, newItem)
        #(pivot.balance < 0 and pivot.item > newItem) or (pivot.balance > 0 and pivot.item < newItem)
        
        if theStack.isEmpty():
            parent = self.root
            
        else:
            parent = theStack.pop()
        
        #subcase A/B
        
        # left imbalance
        if pivot.balance < 0 and pivot.item > newItem:
            badChild = pivot.left
            # A 
            if badChild.item > newItem:
                if parent == self.root:
                    self.root = pivot.rotateRight()
                else:
                    parent.right = pivot.rotateRight()
                pivot.balance = 0
                badChild.balance = 0
            # B
            else:
                badGrandChild = badChild.right
                if parent == self.root:
                    self.root = pivot.rotateLeftThenRight()
                else:
                    parent.right = pivot.rotateLeftThenRight()
                
                #resetting balances
                badGrandChild.balance = 0
                if badGrandChild.item == newItem:
                    pivot.balance = 0
                    badChild.balance = 0
                elif newItem < badGrandChild.item:
                    badChild.balance = 0
                    pivot.balance = 1
                else:
                    badChild.balance = -1
                    pivot.balance = 0                
            
        # right imbalance
        elif pivot.balance > 0 and pivot.item < newItem:
            badChild = pivot.right
            # A
            if badChild.item < newItem:
                if parent == self.root:
                    self.root = pivot.rotateLeft()
                else:
                    parent.left = pivot.rotateLeft()
                pivot.balance = 0
                badChild.balance = 0  
            # B
            else:
                badGrandChild = badChild.left
                if parent == self.root:
                    self.root = pivot.rotateRightThenLeft()
                else:
                    parent.left = pivot.rotateRightThenLeft()
                
                #resetting balances
                badGrandChild.balance = 0
                if badGrandChild.item == newItem:
                    pivot.balance = 0
                    badChild.balance = 0
                elif newItem < badGrandChild.item:
                    badChild.balance = 1
                    pivot.balance = 0
                else:
                    badChild.balance = 0
                    pivot.balance = -1
                    
                     
    def search(self, newItem):
        '''  The AVL tree is not empty.  We search for newItem. This method will 
          return a tuple: (pivot, theStack, parent, found).  
          In this tuple, if there is a pivot node, we return a reference to it 
          (or None). We create a stack of nodes along the search path -- theStack. 
          We indicate whether or not we found an item which matches newItem.  We 
          also return a reference to the last node the search examined -- referred
          to here as the parent.  (Note that if we find an object, the parent is 
          reference to that matching node.)  If there is no match, parent is a 
          reference to the node used to add a child in insert().
        '''
        theStack = Stack()
        node = self.root
        pivot = None
        parent = None
        while node != None:
            # If the value is already in the tree
            if node.item == newItem:
                return (pivot, theStack, parent, True)
            
            # Finding and setting the pivot
            if node.balance != 0:
                pivot = node
                
            theStack.push(node)
            
            if node.item > newItem:
                parent = node
                node = node.left
                
            else:
                parent = node
                node = node.right 
                
        return (pivot, theStack, parent, False)
            
            
def main():
    print("Our names are ")
    print()
    a = AVLNode(20, -1)
    b = AVLNode( 30, -1)
    c = AVLNode(-100)
    d = AVLNode(290)
    '''
    print(a)
    print(b)
    '''
    t = AVLTree()
    t.root = b
    b.left = a
    a.left = c
    b.right = d
    t.count = 4
    print(t)
               
    a = AVLNode(50)
    b = AVLNode(30)
    c = AVLNode(40)
    a.left = b
    b.right = c
    print("Testing rotateLeftThenRight()")
    print(a.rotateLeftThenRight())
               
    (pivot, theStack, parent, found) = t.search(-70)
    print(pivot.item, parent.item, found)
    print()
    print("The items in the nodes of the stack are: ")
    while not theStack.isEmpty():
        current = theStack.pop()
        print(current.item)
    print()
 
    (pivot, theStack, parent, found) = t.search(25)
    print(pivot.item, parent.item, found)
    
    (pivot, theStack, parent, found) = t.search(-100)
    print(pivot.item, parent.item, found)
    
    n1 = AVLNode(50,0)
    n2 = AVLNode(75,0)
    n3 = AVLNode(62,0,n1,n2)
    
    tree = AVLTree(n3,3)
    print(tree)
    
    #t = AVLTree()
    
    #data = random.sample(range(1, 5000), 1000)
    
    #t.root = AVLNode(1001,0)
    #for num in data:
        #t.insert(num)
        
    #t.insert(num)
        
    #print(t)
    
    #n1 = AVLNode(25,0)
    #n2 = AVLNode(15,0)
    #n4 = AVLNode(40,1)
    #n5 = AVLNode(7,0)
    #n6 = AVLNode(18,0)
    #n7 = AVLNode(30,0)
    #n8 = AVLNode(50,0)
    #n9 = AVLNode(27,0)
    #n10 = AVLNode(33,0)
    #n11 = AVLNode(44,0)
    #n12 = AVLNode(65,0)
    
    #'''
    #print(a)
    #print(b)
    #'''
    #t = AVLTree()
    #t.root = n1
    #n1.left = n2
    #n2.left = n5
    #n1.right = n4
    #n2.right = n6
    #n4.left = n7
    #n4.right = n8
    #n7.left = n9
    #n7.right = n10
    #n8.left = n11
    #n8.right = n12
        
    
    #t.count = 6
    #print()
    #t.insert(35)
    
    #print(t)
    
    
if __name__ == '__main__': main()
'''  The output from main():
[evaluate avltree.py]
Our names are
There are 4 nodes in the AVL tree.
-100 0
20 -1
30 -1
290 0

Testing rotateLeftThenRight()
30 0
40 0
50 0

20 -100 False

The items in the nodes of the stack are: 
-100
20
30

20 20 False
20 -100 True
'''