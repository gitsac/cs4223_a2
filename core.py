from .cache import Cache
from .mainmem import mainMemory

class Core:
    def __init__(self, cacheSize, blockSize, assoc, mainMemory: mainMemory):
        self.size = cacheSize
        self.blockSize = blockSize
        self.assoc = assoc
        self.mainMem = mainMemory
        self.executionCycle = 0
        self.computeCycles = 0
        self.memoryOpCount = 0
        self.idleCycles = 0
        self.dataCacheHit = 0
        self.dataCacheMiss = 0

        #creating a cache for each core first
        self.cache = [Cache(self.cacheSize, self.blockSize, self.associativity, mainMemory) for _ in range(1)]

        #need to attach to bus

    def run(self, inputFile):
        #start reading from input file
        with open(inputFile, 'r') as file:
            for line in file:

                #split by first white space
                label, value = line.split(maxsplit=1)

                label = int(label)

                if label == 0:
                    self.cache.loadMemory(value)
                elif label == 1:
                    self.cache.storeMemory(value)
                elif label == 2:
                    self.computeCycles += int(value)
