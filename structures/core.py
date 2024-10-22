from .cache import Cache
from .mainmem import mainMemory

class Core:
    def __init__(self, coreID, bus, cacheSize, blockSize, assoc, mainMemory: mainMemory):
        self.coreID = coreID
        self.size = cacheSize
        self.blockSize = blockSize
        self.assoc = assoc
        self.mainMem = mainMemory
        self.executionCycle = 0
        self.computeCycles = 0
        self.bus = bus
        self.loadCount = 0
        self.storeCount = 0
        self.idleCycles = 0
        self.dataCacheHit = 0
        self.dataCacheMiss = 0

        #creating a cache for each core first
        self.cache = [Cache(self.coreID, self.bus, self.size, self.blockSize, self.assoc, mainMemory) for _ in range(1)]

        #need to attach to bus

    def run(self, inputFile):
        #start reading from input file
        with open(inputFile, 'r') as file:
            for i, line in enumerate(file):
                
                # #For testing only
                # if (i >= 100000):
                #     break
                # print("instruction: " + str(i))
                #split by first white space
                label, value = line.split(maxsplit=1)

                label = int(label)

                if label == 0:
                    hit, evicted = self.cache[0].loadMemory(value)
                    if (not hit and evicted):
                        self.executionCycle += 201
                        self.idleCycles += 200
                        self.dataCacheMiss += 1
                    elif (not hit and not evicted):
                        self.executionCycle += 101
                        self.idleCycles += 100
                        self.dataCacheMiss += 1
                    else:
                        self.executionCycle += 1
                        self.dataCacheHit += 1
                        
                    self.loadCount += 1
                elif label == 1:
                    hit, evicted = self.cache[0].storeMemory(value)
                    if (not hit and evicted):
                        #if cache miss + eviction occurred -> write back + eviction = 100 + 100 = 200. +1 for L1 cache check
                        self.executionCycle += 201
                        
                        #Assume that store eviction 100 cycles counts as idle - to check with prof
                        self.idleCycles += 200
                        self.dataCacheMiss += 1
                    else:
                        #If miss but no eviction, assume write to cache = 0
                        if (not hit):
                            self.executionCycle += 101
                            self.idleCycles += 100
                            self.dataCacheMiss += 1
                        else:
                            self.executionCycle += 1
                            self.dataCacheHit += 1
                    
                    self.storeCount += 1
                elif label == 2:
                    valueConverted = int(value, 16)
                    self.computeCycles += int(valueConverted)
                    self.executionCycle += int(valueConverted)