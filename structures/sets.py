from .blocks import Block
from copy import deepcopy

class memorySet:
    def __init__(self, setID, assoc, blockSize) -> None:
        self.setID = setID
        self.assoc = assoc
        
        self.blockSize = blockSize
        #Most recent - front, least recent - back
        self.blockRecency = []
        self.blocks = set()

    def blockInSet(self, tagNum):
        return any(elem.blockId == tagNum and elem.state != 'I' for elem in self.blocks)

    #return whether is hit, any evict
    def loadMemoryWithMesi(self, tagNum):
        #Check if tagNum in dictionary - if yes, just use blockRecency.indexOf to find index, remove it, then push it to index 0

        #Check if block is in dictionary and block is not invalid
        tagNumInDict = self.blockInSet(tagNum)
        if (tagNumInDict):
            block = Block(self.blockSize, tagNum)
            for elem in self.blocks:
                if elem.blockId == tagNum:
                    block = elem
                    break

            currIndex = self.blockRecency.index(block)
            del self.blockRecency[currIndex]
            self.blockRecency.insert(0, block)
            return True, False

        #If not in dictionary, if dictionary is full, evict the least recently used - blocksRecency[-1], remove this entry from dictionary, and write this entry back to main memory.
        else:
            if len(self.blocks) == self.assoc:
                blockToRemove = self.blockRecency[-1]
                del self.blockRecency[-1]
                self.blocks.remove(blockToRemove)

                toInsert = Block(self.blockSize, tagNum)
                toInsert.state = 'E'
                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)

                #Before returning that there was an eviction - we check if the evicted block is dirty. If yes, then we return that there was an eviction. Else, there is no need to tell them there is an eviction - no need to write back to main memory!
                #Instead of dirty bit, check if data is in modified or exclusive state
                if (blockToRemove.state == 'M'):
                    return False, True

                return False, False
            else: 
                toInsert = Block(self.blockSize, tagNum)
                toInsert.state = 'E'
                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)
                
                return False, False

        #Then, access main memory to retrieve, and add to the front of blockRecency + add to dictionary       
        
    def storeMemoryWithMesi(self, tagNum):
        #Check if tagNum in dictionary - if yes, bring it to front of blockRecency
        tagNumInDict = self.blockInSet(tagNum)

        if (tagNumInDict):
            block = Block(self.blockSize, tagNum)
            for elem in self.blocks:
                if elem.blockId == tagNum:
                    block = elem
                    break
                
            prevState = block.state
            block.state = 'M'

            currIndex = self.blockRecency.index(block)
            del self.blockRecency[currIndex]
            self.blockRecency.insert(0, block)
            return True, False, prevState

        #If not in dictionary, if dictionary is full, evict lru + write back this evicted entry into memory
        else:
            if len(self.blocks) == self.assoc:
                blockToRemove = self.blockRecency[-1]
                del self.blockRecency[-1]
                self.blocks.remove(blockToRemove)

                toInsert = Block(self.blockSize, tagNum)
                toInsert.state = 'M'
                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)

                #Before returning that there was an eviction - we check if the evicted block is dirty. If yes, then we return that there was an eviction. Else, there is no need to tell them there is an eviction - no need to write back to main memory!
                if (blockToRemove.state == 'M'):
                    return False, True, 'I'
                
                return False, False, 'I'
            else: 
                toInsert = Block(self.blockSize, tagNum)
                toInsert.state = 'M'

                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)
   
                return False, False, 'I'
        
        #Then, access main memory to WRITE this block back, and add to the front of blockrecency + add to dictionary 

        #return whether is hit, any evict
    def loadMemoryWithMoesi(self, tagNum):
        #Check if tagNum in dictionary - if yes, just use blockRecency.indexOf to find index, remove it, then push it to index 0

        #Check if block is in dictionary and block is not invalid
        tagNumInDict = self.blockInSet(tagNum)
        if (tagNumInDict):
            block = Block(self.blockSize, tagNum)
            for elem in self.blocks:
                if elem.blockId == tagNum:
                    block = elem
                    break

            currIndex = self.blockRecency.index(block)
            del self.blockRecency[currIndex]
            self.blockRecency.insert(0, block)
            return True, False

        #If not in dictionary, if dictionary is full, evict the least recently used - blocksRecency[-1], remove this entry from dictionary, and write this entry back to main memory.
        else:
            if len(self.blocks) == self.assoc:
                blockToRemove = self.blockRecency[-1]
                del self.blockRecency[-1]
                self.blocks.remove(blockToRemove)

                toInsert = Block(self.blockSize, tagNum)
                toInsert.state = 'E'
                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)

                #Before returning that there was an eviction - we check if the evicted block is dirty. If yes, then we return that there was an eviction. Else, there is no need to tell them there is an eviction - no need to write back to main memory!
                #Instead of dirty bit, check if data is in modified or exclusive state
                if (blockToRemove.state == 'M'):
                    return False, True

                return False, False
            else: 
                toInsert = Block(self.blockSize, tagNum)
                toInsert.state = 'E'
                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)
                
                return False, False

        #Then, access main memory to retrieve, and add to the front of blockRecency + add to dictionary       
        
    def storeMemoryWithMoesi(self, tagNum):
        #Check if tagNum in dictionary - if yes, bring it to front of blockRecency
        tagNumInDict = self.blockInSet(tagNum)

        if (tagNumInDict):
            block = Block(self.blockSize, tagNum)
            for elem in self.blocks:
                if elem.blockId == tagNum:
                    block = elem
                    break
                
            prevState = block.state
            block.state = 'M'

            currIndex = self.blockRecency.index(block)
            del self.blockRecency[currIndex]
            self.blockRecency.insert(0, block)
            return True, False, prevState

        #If not in dictionary, if dictionary is full, evict lru + write back this evicted entry into memory
        else:
            if len(self.blocks) == self.assoc:
                blockToRemove = self.blockRecency[-1]
                del self.blockRecency[-1]
                self.blocks.remove(blockToRemove)

                toInsert = Block(self.blockSize, tagNum)
                toInsert.state = 'M'
                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)

                #Before returning that there was an eviction - we check if the evicted block is dirty. If yes, then we return that there was an eviction. Else, there is no need to tell them there is an eviction - no need to write back to main memory!
                if (blockToRemove.state == 'M'):
                    return False, True, 'I'
                
                return False, False, 'I'
            else: 
                toInsert = Block(self.blockSize, tagNum)
                toInsert.state = 'M'

                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)
   
                return False, False, 'I'
        
        #Then, access main memory to WRITE this block back, and add to the front of blockrecency + add to dictionary 
    
    def loadMemoryWithDragon(self, tagNum):
        #Check if tagNum in dictionary - if yes, just use blockRecency.indexOf to find index, remove it, then push it to index 0

        #Check if block is in dictionary and block is not invalid
        tagNumInDict = self.blockInSet(tagNum)
        if (tagNumInDict):
            block = Block(self.blockSize, tagNum)
            for elem in self.blocks:
                if elem.blockId == tagNum:
                    block = elem
                    break

            currIndex = self.blockRecency.index(block)
            del self.blockRecency[currIndex]
            self.blockRecency.insert(0, block)
            return True, False

        #If not in dictionary, if dictionary is full, evict the least recently used - blocksRecency[-1], remove this entry from dictionary, and write this entry back to main memory.
        else:
            if len(self.blocks) == self.assoc:
                blockToRemove = self.blockRecency[-1]
                del self.blockRecency[-1]
                self.blocks.remove(blockToRemove)

                toInsert = Block(self.blockSize, tagNum)
                toInsert.state = 'E'
                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)

                #Before returning that there was an eviction - we check if the evicted block is dirty. If yes, then we return that there was an eviction. Else, there is no need to tell them there is an eviction - no need to write back to main memory!
                #Instead of dirty bit, check if data is in modified or exclusive state
                if (blockToRemove.state == 'M' or blockToRemove.state == 'Sm'):
                    return False, True

                return False, False
            else:
                #We can instantiate the block with state of 'E' first, then we correct it later in the bus.py if needed when we call busRd.
                toInsert = Block(self.blockSize, tagNum)
                toInsert.state = 'E'
                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)
                
                return False, False
    
    def storeMemoryWithDragon(self, tagNum):
        #Check if tagNum in dictionary - if yes, bring it to front of blockRecency
        tagNumInDict = self.blockInSet(tagNum)

        if (tagNumInDict):
            block = Block(self.blockSize, tagNum)
            for elem in self.blocks:
                if elem.blockId == tagNum:
                    block = elem
                    break
                
            block.state = 'M'

            currIndex = self.blockRecency.index(block)
            del self.blockRecency[currIndex]
            self.blockRecency.insert(0, block)
            return True, False

        #If not in dictionary, if dictionary is full, evict lru + write back this evicted entry into memory
        else:
            if len(self.blocks) == self.assoc:
                blockToRemove = self.blockRecency[-1]
                del self.blockRecency[-1]
                self.blocks.remove(blockToRemove)

                toInsert = Block(self.blockSize, tagNum)
                toInsert.state = 'M'
                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)

                #Before returning that there was an eviction - we check if the evicted block is dirty. If yes, then we return that there was an eviction. Else, there is no need to tell them there is an eviction - no need to write back to main memory!
                if (blockToRemove.state == 'M' or blockToRemove.state == 'Sm'):
                    return False, True
                
                return False, False
            else: 
                toInsert = Block(self.blockSize, tagNum)
                toInsert.state = 'M'

                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)
   
                return False, False
