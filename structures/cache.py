from .sets import memorySet
from .mainmem import mainMemory
from .bus import Bus
import math

class Cache:
    def __init__(self, cacheID, bus: Bus, cacheSize, blockSize, assoc, mainMemory: mainMemory):
        self.cacheID = cacheID
        self.size = cacheSize
        self.blockSize = blockSize
        self.assoc = assoc
        self.bus = bus
        self.numSets = int(self.size/(self.assoc * self.blockSize))
        self.sets = [memorySet(i, self.assoc, blockSize) for i in range(self.numSets)]
        self.mainMem = mainMemory
        
    def translateAddr(self, memAddr: str):
        addrInt = int(memAddr, 16)
        addrBin = bin(addrInt)[2:].zfill(32)  # More concise way to zero-pad
        
        numBitsSetIndex = int(math.log(self.numSets, 2))
        numBitsOffset = int(math.log(self.blockSize, 2))
        
        # Correct slice for set index
        setNumberBin = addrBin[-(numBitsSetIndex + numBitsOffset):-numBitsOffset]
        setNumberInt = int(setNumberBin, 2)
        
        # Correct slice for tag
        setTagBin = addrBin[0:-(numBitsSetIndex + numBitsOffset)]
        setTagInt = int(setTagBin, 2)
        
        return setNumberInt, setTagInt
    
    #Check if block exists in cache
    def blockInCache(self, memAddr):
        setIndex, setTag = self.translateAddr(memAddr)
        return self.sets[setIndex].blockInSet(setTag)
        
    def loadMemory(self, memAddr: str):
        #Process memAddr to get set index + tag #
        
        #Set index and set tag returned in integer
        setIndex, setTag = self.translateAddr(memAddr)
        
        #This should return whether it was a hit AND whether any block was evicted in doing so.
        hit, eviction = self.sets[setIndex].loadMemory(setTag)

        #check if there was a hit, if yes, no need for bus transaction, else, call busRd
        if (not hit):
            self.bus.busReadShared(memAddr, self.cacheID)
        return hit, eviction
        
    
    def storeMemory(self, memAddr):
        setIndex, setTag = self.translateAddr(memAddr)
        
        #This should also return whether it was a hit in cache AND whether any block was evicted in doing so.
        hit, eviction = self.sets[setIndex].storeMemory(setTag)

        #Must call for exclusive bus read regardless, due to the fact that a store changes values
        self.bus.busReadExclusive(memAddr, self.cacheID)
        return hit, eviction
    
    # #This function should be called by either load memory or store memory
    # def privateRead(self, memAddr):
    #     setIndex, setTag = self.translateAddr(memAddr)
        
    #     #Should call sets.transition here.
        
    #     #Thereafter, call busRd or busWr

    # #This function should be called by either load memory or store memory
    # def privateWrite(self, memAddr):
    #     setIndex, setTag = self.translateAddr(memAddr)
        
    #     #Should call sets.transition here