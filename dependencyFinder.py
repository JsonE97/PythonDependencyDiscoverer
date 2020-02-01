# -*- coding: utf-8 -*-

"""
Dependency Discoverer implementation for .c files

NOTE  - this is a reimplementation of the java dependency discoverer in my repository
USAGE - the user can simply run the python script without args to run with the base data in "./Dataset/" or
        they can pass in 1 command arg for their own custom directory
"""

# required imports
import errno
import os
import sys
import glob


# may as well keep this global as almost every function uses it
# in the format { <string - format> : <list <string> - dependencies> }
fileDepsMap = {}


""" Takes in a directory name and returns a list of all the files in the directory. IOError if there is a problem
Args:
    dir (string) - given directory to traverse files
Returns:
    list - of all files in directory
"""

def obtainFiles(dir):
    if os.path.isdir(dir):
        return glob.glob(dir + "/*")
    else:
        raise IOError("Directory {0} not found!".format(dir))


""" Takes in a list of lines and searches for #include occurrences. It extracts these and stores them for returning
Args:
    lines (list)          - a list of lines to traverse
    filesToProcess (list) - a list of files that still need to be processed for the current file {f}
    f (string)            - the current file being traversed for dependencies
Returns:
    filesToProcess (list) - a new list of files to process with the current one processed removed
"""

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


""" Takes in a list of files and prepares them for being traversed
Args:
    fileList (list) - list of files to traverse
"""

def processFiles(fileList):
    for f in fileList:
        if os.path.isfile(f):
            lastDirPath = f.rfind("/")
            f = f[lastDirPath + 1:]
            if f not in fileDepsMap.keys():
                fileDepsMap[f] = []
            processCurrentFile(f)


""" Takes a given file and obtains all the lines and prepares them for being processed
Args:
    f (string) - given file to obtain lines for
"""

def processCurrentFile(f):
    filesToProcess = [f]
    while len(filesToProcess) != 0:
        newFile = filesToProcess.pop()
        if os.path.isfile(inDir + newFile):
            with open(inDir + newFile) as curFile:
                lines = curFile.readlines()
            filesToProcess = processLines(lines, filesToProcess, f)


""" Iterates over the dependency map and prints out the dependencies for each file
No args/return values
"""

def printDependencies():
    for k,v in fileDepsMap.items():
        if (".c" in k):
            print("File {0} has dependencies - {1}".format(k, ', '.join(v)))

if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise ValueError("Too many command args passed in!")
    if len(sys.argv) == 2:
        inDir = sys.argv[1]
    else:
        inDir = "./Dataset/"
    fileList = obtainFiles(inDir)
    processFiles(fileList)
    printDependencies()