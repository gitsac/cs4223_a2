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
    for i in range(1):
        core = [Core(i, bus, int(cacheSize), int(blockSize), int(associativity), memory) for _ in range(1)]

    actualInputFile = inputFile + "/" + inputFile + "_0.data"
    #run input file on first core first

    core[0].run(actualInputFile)

    singleCore = core[0]
    # Output statistics from main instead of core.
    print("Stats:")
    print("Overall execution cycles: " + str(singleCore.executionCycle) + " cycles")
    print("Number of compute cycles: " + str(singleCore.computeCycles) + " cycles")
    print("Number of load instructions: " + str(singleCore.loadCount) + " instructions")
    print("Number of store instructions: " + str(singleCore.storeCount) + " instructions")
    print("Number of idle cycles: " + str(singleCore.idleCycles) + " cycles")
    print("Number of cache hits: " + str(singleCore.dataCacheHit) + " hits")
    print("Number of cache misses: " + str(singleCore.dataCacheMiss) + " misses")
    print("Data traffic: " + str(bus.busRd + bus.busRdX))
    print("Number of invalidations/updates: " + str(0))
    print("Number of accesses to private data: ") 
    print("Number of accesses to shared data: ")


if __name__ == "__main__":
    main()