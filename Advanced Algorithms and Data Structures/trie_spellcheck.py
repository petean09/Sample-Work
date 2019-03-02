class Trie:
    def __insert(node,item):
        if item == "":
            return None
        
        if node == None:
            node = Trie.TrieNode(item[0])
            restOfNode = item[1:]
            node.follows = Trie.__insert(None,item[1:])
            return node
        
        if item[0] == node.item:
            node.follows = Trie.__insert(node.follows,item[1:])
            return node
        
        else:
            node.nxt = Trie.__insert(node.nxt,item)
            return node

    def __contains(node,item):
        if item == "":
            return True
        
        if node == None:
            return False        
        
        if item[0] == node.item:
            return Trie.__contains(node.follows,item[1:])
        
        return Trie.__contains(node.nxt,item)
            

    
    class TrieNode:
        def __init__(self, item, follows = None, nxt = None):
            self.item = item
            self.nxt = nxt
            self.follows = follows
            
    def __init__(self):
        self.start = None
        
    def insert(self,item):
        item = item + '$'
        self.start = Trie.__insert(self.start,item)
        
    def __contains__(self,item):
        item = item + '$'
        return Trie.__contains(self.start,item)
    
def main():
    trie = Trie()
    
    file = open("wordsEn.txt", "r")
    for word in file:
        word = word.strip()
        trie.insert(word)
        
    print('Spell Checker')
    print()       
    
    file2 = open('declarationOfIndependence.txt', 'r')
    for line in file2:
        for word in line.split():
            word = word.lower().strip(",.-;:&")
            if word not in trie:
                print('"' + word + '"' + " is spelled wrong.")         
    
    
if __name__ == "__main__":
    main()
