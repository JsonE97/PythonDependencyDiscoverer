import os
import glob

fileDepsMap = {}

def obtainFiles(dir):
    return glob.glob(dir + "/*")

def processFiles(fileList):
    filesToProcess = []

    # this file breaks it
    for f in fileList:
        print("on file " + f)
        if os.path.isfile(f):
            if f not in fileDepsMap.keys():
                fileDepsMap[f] = []
            with open(f) as curFile:
                lines = curFile.readlines()
            for l in lines:
                if "include" in l:
                    includeFile = l.split(" ")[1]
                    if not "<" in includeFile:
                        newDep = includeFile.replace("\"", "").replace("\n","")
                        filesToProcess = [newDep] + filesToProcess
                        fileDepsMap[f].append(newDep)
            while len(filesToProcess) != 0:
                newFile = filesToProcess.pop()
                if os.path.isfile('./Dataset/' + newFile):
                    with open('./Dataset/' + newFile) as curFile:
                        lines = curFile.readlines()
                    for l in lines:
                        if "include" in l:
                            includeFile = l.split(" ")[1]
                            if not "<" in includeFile:
                                newDep = includeFile.replace("\"", "").replace("\n","")
                                if newDep not in fileDepsMap[f]:
                                    fileDepsMap[f].append(newDep)
                                    filesToProcess = [newDep] + filesToProcess

    print(fileDepsMap)



if __name__ == "__main__":
    fileList = obtainFiles("./Dataset")
    processFiles(fileList)
