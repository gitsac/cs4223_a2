import argparse
from .mainmem import mainMemory
from .core import Core

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

    #creating a core
    core = [Core(cacheSize, blockSize, associativity, memory) for _ in range(1)]

    #run input file on first core first
    core[0].run(inputFile)

if __name__ == "__main__":
    main()