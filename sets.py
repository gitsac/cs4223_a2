from .blocks import Blocks

class memorySet:
    def __init__(self, setID, setSize, blockSize) -> None:
        self.setID = setID
        self.size = setSize
        self.blockSize = blockSize
        
        #Most recent - front, least recent - back
        self.blockRecency = []
        self.blocks = {}
        
    def loadMemory(self, tagNum):
        #Check if tagNum in dictionary - if yes, just use blockRecency.indexOf to find index, remove it, then push it to index 0
        
        #If not in dictionary, if dictionary is full, evict the least recently used - blocksRecency[-1], remove this entry from dictionary, and write this entry back to main memory.
        
        #Then, access main memory to retrieve, and add to the front of blockRecency + add to dictionary
        return
        
    def storeMemory(self, tagNum):
        #Check if tagNum in dictionary - if yes, bring it to front of blockRecency
        
        #If not in dictionary, if dictionary is full, evict lru + write back this evicted entry into memory
        
        #Then, access main memory to WRITE this block back, and add to the front of blockrecency + add to dictionary
        return
        
        
        
    
