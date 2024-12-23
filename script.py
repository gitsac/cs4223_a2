import subprocess
import argparse


def toRun(outputFile, paramName, paramSize, protocol, file):
    cacheSize = 1024
    assoc = 2
    blockSize = 32
    if (paramName == "cs"):
        cacheSize = paramSize
    elif (paramName == "as"):
        assoc = paramSize
    #Must run with bs
    else:
        blockSize = paramSize
        
    process = subprocess.run(["python", "main.py", protocol, file, str(cacheSize), str(assoc), str(blockSize)], capture_output=True, text=True, check=True)
    with open(outputFile, 'a') as f:
        f.write("=== Output ===\n")
        f.write("STDOUT:\n")
        f.write(process.stdout)
        f.write("\nSTDERR:\n")
        f.write(process.stderr)
        
    return

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('protocol')
    parser.add_argument('paramName')
    parser.add_argument("dataSet")
    arguments = parser.parse_args()

    protocol = arguments.protocol
    param = arguments.paramName
    dataSet = arguments.dataSet

    sizes = []
    if (param == "cs"):
        sizes = [128, 512, 1024, 2048, 8192]
    elif (param == "as"):
        sizes = [1, 2, 4, 16, 64]
    elif (param == "bs"):
        sizes = [4, 16, 64, 128, 256]
    else:
        print("Invalid argument")

    for size in sizes:
        toRun("./outputs/newData/" + protocol + "_" + param  + "_" + dataSet + "_" + "outputs.txt", param, size, protocol, dataSet)


if __name__ == "__main__":
    main()