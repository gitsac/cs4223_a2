import argparse
from structures.mainmem import mainMemory
from structures.core import Core
from structures.bus import Bus
import threading

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

    # core[0].run(actualInputFile0)
    # core[1].run(actualInputFile1)
    # core[2].run(actualInputFile2)
    # core[3].run(actualInputFile3)
    t0 = threading.Thread(target=core[0].run, args=(actualInputFile0,))
    t1 = threading.Thread(target=core[1].run, args=(actualInputFile1,))
    t2 = threading.Thread(target=core[2].run, args=(actualInputFile2,))
    t3 = threading.Thread(target=core[3].run, args=(actualInputFile3,))

    threading.Event()
    
    threads = [t0, t1, t2, t3]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    def printStats(singleCore: Core):
        print("Core " + str(singleCore.coreID) + " Number of execution cycles: " + str(singleCore.executionCycle) + " cycles")
        print("Core " + str(singleCore.coreID) + " Number of compute cycles: " + str(singleCore.computeCycles) + " cycles")
        print("Core " + str(singleCore.coreID) + " Number of load instructions: " + str(singleCore.loadCount) + " instructions")
        print("Core " + str(singleCore.coreID) + " Number of store instructions: " + str(singleCore.storeCount) + " instructions")
        print("Core " + str(singleCore.coreID) + " Number of idle cycles: " + str(singleCore.idleCycles) + " cycles")
        print("Core " + str(singleCore.coreID) + " Number of cache hits: " + str(singleCore.dataCacheHit) + " hits")
        print("Core " + str(singleCore.coreID) + " Number of cache misses: " + str(singleCore.dataCacheMiss) + " misses")
    
    maxExecCycle = max(core, key=lambda core: core.executionCycle)

    print("Stats:")
    print("Overall execution cycles: " + str(maxExecCycle.executionCycle) + " cycles")
    for i in range(4):
        printStats(core[i])

    print("Data traffic: " + str(bus.traffic) + "B")
    print("Number of invalidations: " + str(bus.invalidations))
    print("Number of updates: " + str(bus.updates))
    print("Number of accesses to private data: " + str(bus.privateDataAccesses)) 
    print("Number of accesses to shared data: " + str(bus.sharedDataAccesses))
    # Output statistics from main instead of core.


if __name__ == "__main__":
    main()