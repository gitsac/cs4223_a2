import argparse
from structures.mainmem import mainMemory
from structures.core import Core
from structures.bus import Bus

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('protocol')
    parser.add_argument('input_file')
    parser.add_argument('cache_size')
    parser.add_argument('associativity')
    parser.add_argument('block_size')

    arguments = parser.parse_args()

    protocol = arguments.protocol
    inputFile = arguments.input_file
    cacheSize = arguments.cache_size
    associativity = arguments.associativity
    blockSize = arguments.block_size

    #creating a memory used by all caches
    memory = mainMemory()
    
    #creating a bus
    bus = Bus()

    #creating a core
    core = [Core(i, bus, int(cacheSize), int(blockSize), int(associativity), memory, protocol) for i in range(4)]

    actualInputFile0 = inputFile + "/" + inputFile + "_0.data"
    actualInputFile1 = inputFile + "/" + inputFile + "_1.data"
    actualInputFile2 = inputFile + "/" + inputFile + "_2.data"
    actualInputFile3 = inputFile + "/" + inputFile + "_3.data"
    #run input file on first core first

    core[0].run(actualInputFile0)
    core[1].run(actualInputFile1)
    core[2].run(actualInputFile2)
    core[3].run(actualInputFile3)

    def printStats(singleCore):
        print("Stats:")
        print("Overall execution cycles: " + str(singleCore.executionCycle) + " cycles")
        print("Number of compute cycles: " + str(singleCore.computeCycles) + " cycles")
        print("Number of load instructions: " + str(singleCore.loadCount) + " instructions")
        print("Number of store instructions: " + str(singleCore.storeCount) + " instructions")
        print("Number of idle cycles: " + str(singleCore.idleCycles) + " cycles")
        print("Number of cache hits: " + str(singleCore.dataCacheHit) + " hits")
        print("Number of cache misses: " + str(singleCore.dataCacheMiss) + " misses")
        # print("Data traffic: " + str((bus.busRd + bus.busRdX) * 4) + "B")
        print("Data traffic: 0B")
        print("Number of invalidations: " + str(bus.invalidations))
        print("Number of updates: " + str(bus.updates))
        print("Number of accesses to private data: " + str(bus.privateDataAccesses)) 
        print("Number of accesses to shared data: " + str(bus.sharedDataAccesses))
    
    for i in range(4):
        printStats(core[i])
    # Output statistics from main instead of core.


if __name__ == "__main__":
    main()