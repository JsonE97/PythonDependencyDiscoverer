import os
import glob

fileDepsMap = {}

def obtainFiles(dir):
    return glob.glob(dir + "/*")


def processLines(lines, filesToProcess, f):
    for l in lines:
        if "include" in l:
            includeFile = l.split(" ")[1]
            if not "<" in includeFile:
                newDep = includeFile.replace("\"", "").replace("\n","")
                if newDep not in fileDepsMap[f]:
                    fileDepsMap[f].append(newDep)
                    filesToProcess = [newDep] + filesToProcess
    return filesToProcess

def processFiles(fileList):
    filesToProcess = []

    for f in fileList:
        if os.path.isfile(f):
            f = f.replace("./Dataset/", "")
            if f not in fileDepsMap.keys():
                fileDepsMap[f] = []
            filesToProcess = [f]
            while len(filesToProcess) != 0:
                newFile = filesToProcess.pop()
                if os.path.isfile('./Dataset/' + newFile):
                    with open('./Dataset/' + newFile) as curFile:
                        lines = curFile.readlines()
                    filesToProcess = processLines(lines, filesToProcess, f)


if __name__ == "__main__":
    fileList = obtainFiles("./Dataset")
    processFiles(fileList)
