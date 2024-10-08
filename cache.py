from .sets import memorySet
from .mainmem import mainMemory

class Cache:
    def __init__(self, cacheSize, blockSize, assoc, mainMemory: mainMemory):
        self.size = cacheSize
        self.blockSize = blockSize
        self.assoc = assoc
        self.numSets = int(self.size/(self.assoc * self.blockSize))
        self.sets = [memorySet(i) for i in range(self.numSets)]
        self.mainMem = mainMemory
        
    def loadMemory(self, memAddr):
        #If in cache, return + set recency
        
        #If not in cache, we add entry into cache + retrieve from main memory -> Might need to evict least recently used block -> writeback for that
        return
    
    def storeMemory(self, memAddr):
        return
    
    def writeBack(self):
        #Evict first

        #Write back the result of eviction into main memory
        self.mainMem.writeBack()
        
        
    
    
