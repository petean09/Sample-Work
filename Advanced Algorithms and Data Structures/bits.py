'''
BloomFilter - Spellchecker
Author: Anna Peterson
CS360
'''


import math

class BloomFilter:
    def __init__(self, count, falsePosPercent=0):
        m = -1 * (count * math.log(falsePosPercent/100)) / ((math.log(2)) ** 2)
        k = (m/count)*math.log(2)
        
        self.bA = bytearray(int((m+7)//8))
        self.numHashes = int(k+0.5)
        
        #creates a dictionary of the 8 masks for easy look up
        self.masks = {}
        for i in range(8):
            self.masks[i] = 1 << i
        
    def add(self, word):
        for i in range(self.numHashes):
            hV = hash(word + str(i))
            bitIndex = hV % (len(self.bA) * 8)
            bAIndex = bitIndex >> 3
            exponent = bitIndex & 7
            mask = self.masks[exponent]
            self.bA[bAIndex] |= mask
            
            
    def __contains__(self,word):
        # same exact as add but uses '&' 
        for i in range(self.numHashes):
            hV = hash(word + str(i))
            bitIndex = hV % (len(self.bA) * 8)
            bAIndex = bitIndex >> 3
            exponent = bitIndex & 7
            mask = self.masks[exponent]
            value = self.bA[bAIndex] & mask
            if value == 0:
                return False
        return True
            
    
    def __str__(self):
        rv = str(self.numHashes) + " " + str(len(self.bA)) + "\n"
        for i in range(len(self.bA) -1, -1, -1):
            rv += bin(self.bA[i])
        return rv
        
def main():
    
    wordCount = 0
    file = open('wordsEn.txt', 'r')
    for line in file:
        wordCount +=1
    
    bf = BloomFilter(wordCount,.5)
    
    file = open('wordsEn.txt', 'r')
    for line in file:
        bf.add(line.strip())
        
    print('Spell Checker')
    print()       
    
    file2 = open('declarationOfIndependence.txt', 'r')
    for line in file2:
        for word in line.split():
            word = word.lower().strip(",.-;:&")
            if word not in bf:
                print('"' + word + '"' + " is spelled wrong.")            

main()