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

    def mesiBusRd(self, memAddr, cacheNum):
        currCache = self.attachedCache[cacheNum]
        self.busRd += 1
        self.traffic += currCache.blockSize
        block = None
        setIndex, setTag = currCache.translateAddr(memAddr)

        for i, cache in enumerate(self.attachedCache):
            if (i == cacheNum):
                continue

            if (cache.blockInCache(memAddr)):
                for currBlock in cache.sets[setIndex].blocks:
                    if currBlock.blockId == setTag:
                        block = currBlock

                        if currBlock.state == 'M':
                            self.privateDataAccesses += 1
                        elif currBlock.state == 'E':
                            self.privateDataAccesses += 1
                        elif currBlock.state == 'S':
                            self.sharedDataAccesses += 1

                    currBlock.state = 'S'

        if block: 
            for i, cache in enumerate(self.attachedCache):
                if (i == cacheNum):
                    for currBlock in cache.sets[setIndex].blocks:
                        if currBlock.blockId == setTag:
                            currBlock.state = 'S'
            
            return 2 * cache.blockSize / 4 
        else: 
            return 100

    
    def mesiBusRdX(self, memAddr, cacheNum, prevState):
        currCache = self.attachedCache[cacheNum]
        self.busRd += 1
        self.traffic += currCache.blockSize
        setIndex, setTag = currCache.translateAddr(memAddr)

        #Invalidate all caches with the same data from S to I
        if prevState == 'S':
            for i, cache in enumerate(self.attachedCache):
                if (i == cacheNum):
                    continue
                    
                if (cache.blockInCache(memAddr)):
                    self.invalidations += 1
                    self.sharedDataAccesses += 1

                    for currBlock in cache.sets[setIndex].blocks:
                        if currBlock.blockId == setTag:
                            currBlock.state = 'I'
            return 0

        elif prevState == 'I':
            block = None

            for i, cache in enumerate(self.attachedCache):
                if (i == cacheNum):
                    continue

                if (cache.blockInCache(memAddr)):
                    for currBlock in cache.sets[setIndex].blocks:
                        p
                        if currBlock.blockId == setTag:
                            block = currBlock

                            if currBlock.state == 'M':
                                self.privateDataAccesses += 1
                            elif currBlock.state == 'E':
                                self.privateDataAccesses += 1
                            elif currBlock.state == 'S':
                                self.sharedDataAccesses += 1

                        currBlock.state = 'I'
                        self.invalidations += 1

            if block:
                return 2 * cache.blockSize / 4 
            else: 
                return 100

    def mesiFlush(self):
        self.traffic += self.attachedCache[0].blockSize