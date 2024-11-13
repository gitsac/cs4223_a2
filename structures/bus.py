from .fairLock import FCFSLock

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
        self.lock = FCFSLock()

        
    def attachCache(self, cache):
        self.attachedCache.append(cache)

    def mesiBusRd(self, memAddr, cacheNum):
        self.lock.acquire()
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
            
            self.lock.release()
            return 2 * cache.blockSize / 4 
        else: 
            self.lock.release()
            return 100

    
    def mesiBusRdX(self, memAddr, cacheNum, prevState):
        self.lock.acquire()
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
            self.lock.release()
            return 0

        elif prevState == 'I':
            block = None

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

                        currBlock.state = 'I'
                        self.invalidations += 1

            if block:
                self.lock.release()
                return 2 * cache.blockSize / 4 
            else:
                self.lock.release() 
                return 100

    def mesiFlush(self):
        self.lock.acquire()
        self.traffic += self.attachedCache[0].blockSize
        self.lock.release()

    def dragonBusRd(self, memAddr, cacheNum):
        self.lock.acquire()
        currCache = self.attachedCache[cacheNum]
        self.busRd += 1
        self.traffic += currCache.blockSize
        block = None
        setIndex, setTag = currCache.translateAddr(memAddr)

        #First, we check if any cache has this block, if yes, use the 2 * cache.blockSize/4 formula, else we will just spend 100 cycles to retrieve from main memory.
        for i, cache in enumerate(self.attachedCache):
            if (i == cacheNum):
                continue

            if (cache.blockInCache(memAddr)):
                for currBlock in cache.sets[setIndex].blocks:
                    if currBlock.blockId == setTag:
                        block = currBlock

                        if currBlock.state == 'M':
                            self.privateDataAccesses += 1
                            currBlock.state = 'Sm'
                            
                        elif currBlock.state == 'E':
                            self.privateDataAccesses += 1
                            currBlock.state = 'Sc'

                        elif currBlock.state == 'Sc' or currBlock.state == 'Sm':
                            self.sharedDataAccesses += 1

        #if we took from a fellow cache, we will set the state on current cache to Sc, else we will set it to E as it is the first to bring this block into cache. Return corresponding cycle.
        if (block):
            for i, cache in enumerate(self.attachedCache):
                if (i == cacheNum):
                    for currBlock in cache.sets[setIndex].blocks:
                        if currBlock.blockId == setTag:
                            currBlock.state = 'Sc'

            self.lock.release()
            return 2 * cache.blockSize / 4 
        else:
            self.lock.release()
            return 100


    def dragonBusUpd(self, memAddr, cacheNum):
        self.lock.acquire()
        currCache = self.attachedCache[cacheNum]
        self.busRd += 1
        self.traffic += currCache.blockSize
        block = None
        setIndex, setTag = currCache.translateAddr(memAddr)
        amtDataExchanged = 0
        
        #Iterate through all caches, and see if any of them have this block loaded. If yes, then we attempt to update them
        for i, cache in enumerate(self.attachedCache):
            if (i == cacheNum):
                continue

            if (cache.blockInCache(memAddr)):
                for currBlock in cache.sets[setIndex].blocks:
                    if currBlock.blockId == setTag:
                        block = currBlock
                        amtDataExchanged += (2 * cache.blockSize / 4)

                        self.sharedDataAccesses += 1
                        currBlock.state = 'Sc'

        #Since block != None, some other cache must be holding it, thus we cannot allow current cache to be M -> must be downgraded to Sm
        if (block):
            self.updates += 1
            for i, cache in enumerate(self.attachedCache):
                if (i == cacheNum):
                    for currBlock in cache.sets[setIndex].blocks:
                        if currBlock.blockId == setTag:
                            currBlock.state = 'Sm'
            
            #This represents data transfer from one of the other block to my current block
            amtDataExchanged += (2 * cache.blockSize / 4)
        else:
            #Else, fetched from memory
            amtDataExchanged += 100

        self.lock.release()
        return amtDataExchanged
    
    #Flush is used for transition from M -> Sm. We will simply use block size as the flushed data, no real need to send data around.
    def dragonFlush(self):
        self.lock.acquire()
        self.traffic += self.attachedCache[0].blockSize
        self.lock.release()
