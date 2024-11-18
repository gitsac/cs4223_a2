from .cache import Cache

class MoesiCache(Cache):
    def __init__(self, cacheID, bus, cacheSize, blockSize, assoc, mainMemory):
        super().__init__(cacheID, bus, cacheSize, blockSize, assoc, mainMemory)

    def loadMemory(self, memAddr):
        #Set index and set tag returned in integer
        setIndex, setTag = super().translateAddr(memAddr)
        
        #This should return whether it was a hit AND whether any block was evicted in doing so.
        hit, eviction = self.sets[setIndex].loadMemoryWithMoesi(setTag)

        memCycles = 0
        #check if there was a hit, if yes, no need for bus transaction, else, call busRd
        if (not hit):
            memCycles = self.bus.moesiBusRd(memAddr, self.cacheID)

        if (eviction):
            self.bus.moesiFlush()

        return hit, eviction, memCycles
    
    def storeMemory(self, memAddr):
        setIndex, setTag = self.translateAddr(memAddr)
        
        #This should also return whether it was a hit in cache AND whether any block was evicted in doing so.
        hit, eviction, prevState = self.sets[setIndex].storeMemoryWithMoesi(setTag)

        #Must call for exclusive bus read regardless, due to the fact that a store changes values
        memCycles = 0
        if prevState != 'E' and prevState != 'M':
            memCycles = self.bus.moesiBusRdX(memAddr, self.cacheID, prevState)

        if (eviction):
            self.bus.moesiFlush()

        return hit, eviction, memCycles
    