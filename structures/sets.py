from .blocks import Block

class memorySet:
    def __init__(self, setID, assoc, blockSize) -> None:
        self.setID = setID
        self.assoc = assoc
        
        self.blockSize = blockSize
        #Most recent - front, least recent - back
        self.blockRecency = []
        self.blocks = set()
        
    #return whether is hit, any evict
    def loadMemory(self, tagNum):
        #Check if tagNum in dictionary - if yes, just use blockRecency.indexOf to find index, remove it, then push it to index 0

        tagNumInDict = any(elem.blockId == tagNum for elem in self.blocks)
        print(tagNumInDict)
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
                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)

                #Before returning that there was an eviction - we check if the evicted block is dirty. If yes, then we return that there was an eviction. Else, there is no need to tell them there is an eviction - no need to write back to main memory!
                if (blockToRemove.dirty == 1):
                    return False, True
                
                return False, False
            else: 
                toInsert = Block(self.blockSize, tagNum)
                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)
                return False, False

        #Then, access main memory to retrieve, and add to the front of blockRecency + add to dictionary
        
    def storeMemory(self, tagNum):
        #Check if tagNum in dictionary - if yes, bring it to front of blockRecency
        tagNumInDict = any(elem.blockId == tagNum for elem in self.blocks)
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

        #If not in dictionary, if dictionary is full, evict lru + write back this evicted entry into memory
        else:
            if len(self.blocks) == self.assoc:
                blockToRemove = self.blockRecency[-1]
                del self.blockRecency[-1]
                self.blocks.remove(blockToRemove)

                toInsert = Block(self.blockSize, tagNum)
                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)

                #Before returning that there was an eviction - we check if the evicted block is dirty. If yes, then we return that there was an eviction. Else, there is no need to tell them there is an eviction - no need to write back to main memory!
                if (blockToRemove.dirty == 1):
                    return False, True
                
                return False, False
            else: 
                toInsert = Block(self.blockSize, tagNum)
                toInsert.dirty = 1

                self.blockRecency.insert(0, toInsert)
                self.blocks.add(toInsert)
                return False, False          
        
        #Then, access main memory to WRITE this block back, and add to the front of blockrecency + add to dictionary        
        
        
    
