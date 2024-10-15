from .sets import memorySet
from .mainmem import mainMemory
import math

class Cache:
    def __init__(self, bus, cacheSize, blockSize, assoc, mainMemory: mainMemory):
        self.size = cacheSize
        self.blockSize = blockSize
        self.assoc = assoc
        self.bus = bus
        self.numSets = int(self.size/(self.assoc * self.blockSize))
        self.sets = [memorySet(i, self.assoc) for i in range(self.numSets)]
        self.mainMem = mainMemory
        
    def translateAddr(self, memAddr: str):
        addrInt = int(memAddr, 16)
        addrBin = bin(addrInt)[2:]
        while (len(addrBin) < 32):
            addrBin = '0' + addrBin
        
        numBitsSetIndex = int(math.log(self.numSets, 2))
        numBitsOffset = int(math.log(self.blockSize, 2))
        setNumberBin = addrBin[-(numBitsSetIndex + numBitsOffset - 1):-numBitsOffset]
        setNumberInt = int(setNumberBin, 2)
        
        setTagBin = addrBin[0:-(numBitsSetIndex + numBitsOffset)]
        setTagInt = int(setTagBin, 2)
        return setNumberInt, setTagInt
        
    def loadMemory(self, memAddr: str):
        #Process memAddr to get set index + tag #
        
        #Set index and set tag returned in integer
        setIndex, setTag = self.translateAddr(memAddr)
        
        #This should return whether it was a hit AND whether any block was evicted in doing so.
        return self.sets[setIndex].loadMemory(setTag)
        
    
    def storeMemory(self, memAddr):
        setIndex, setTag = self.translateAddr(memAddr)
        
        #This should also return whether it was a hit in cache AND whether any block was evicted in doing so.
        return self.sets[setIndex].storeMemory(setTag)
    
    # #This function should be called by either load memory or store memory
    # def privateRead(self, memAddr):
    #     setIndex, setTag = self.translateAddr(memAddr)
        
    #     #Should call sets.transition here.
        
    #     #Thereafter, call busRd or busWr

    # #This function should be called by either load memory or store memory
    # def privateWrite(self, memAddr):
    #     setIndex, setTag = self.translateAddr(memAddr)
        
    #     #Should call sets.transition here