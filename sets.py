from .blocks import Blocks
from .mainmem import mainMemory

class memorySet:
    def __init__(self, setID, assoc, mainMemory: mainMemory) -> None:
        self.setID = setID
        self.assoc = assoc
        
        #Most recent - front, least recent - back
        self.blockRecency = []
        self.blocks = set()
        
    #return whether is hit, any evict
    def loadMemory(self, tagNum):
        #Check if tagNum in dictionary - if yes, just use blockRecency.indexOf to find index, remove it, then push it to index 0
        if tagNum in self.blocks:
            currIndex = self.blockRecency.index(tagNum)
    
            del self.blockRecency[currIndex]
            self.blockRecency.insert(0, tagNum)

            return True, False
        
        #If not in dictionary, if dictionary is full, evict the least recently used - blocksRecency[-1], remove this entry from dictionary, and write this entry back to main memory.
        else:
            if len(self.blocks) == self.assoc:
                tagNumToRemove = self.blockRecency[-1]
                del self.blockRecency[-1]
                del self.blocks[tagNumToRemove]

                #mainMemory.writeBack(dataToFlush)

                self.blockRecency.insert(0, tagNum)
                self.blocks.add(tagNum)

                return False, True
            else: 
                self.blockRecency.insert(0, tagNum)
                self.blocks.add(tagNum)
                return False, False



        #Then, access main memory to retrieve, and add to the front of blockRecency + add to dictionary
        
    def storeMemory(self, tagNum):
        #Check if tagNum in dictionary - if yes, bring it to front of blockRecency
        
        #If not in dictionary, if dictionary is full, evict lru + write back this evicted entry into memory
        
        #Then, access main memory to WRITE this block back, and add to the front of blockrecency + add to dictionary
        return
        
        
        
    
