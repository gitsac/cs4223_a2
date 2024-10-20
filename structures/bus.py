class Bus:
    def __init__(self):
        self.attachedCache = []
        self.traffic = 0
        self.busRd = 0
        self.busRdX = 0
        self.invalidations = 0
        self.updates = 0
        self.privateDataAccesses = 0
        self.sharedDataAccesses = 0
        
    def attachCache(self, cache):
        self.attachedCache.append(cache)

    def busReadShared(self, memAddr, cacheNum):
        self.busRd += 1
        for i, cache in self.attachedCache:
            if (i == cacheNum):
                continue
            cache.receiveBusShared(memAddr)

        return
    
    def busReadExclusive(self, memAddr, cacheNum):
        self.busRdX += 1
        for i, cache in self.attachedCache:
            if (i == cacheNum):
                continue
            cache.receiveBusSharedExclusive(memAddr)

        return