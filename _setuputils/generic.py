import os
import re
import sys
import stat
import json
import shutil
import pathlib
import functools

_globals = set(globals().keys())

onLinux = sys.platform.startswith("linux")
onWindows = sys.platform.startswith("win")
onMacOS = sys.platform == "darwin"

if not (onLinux or onWindows or onMacOS):
    raise Exception("unknown OS")

def getPlatformSummary():
    summary = {
        "sys.version" : sys.version,
        "sys.platform" : sys.platform,
        "sys.api_version" : sys.api_version,
        "sys.version_info" : sys.version_info,
        "os.name" : os.name
    }
    try:
        import Cython
        summary["Cython.__version__"] = Cython.__version__
    except: pass
    return summary

def printHeader(text):
    print()
    print()
    print(text)
    print("-"*50)
    print()

def executePythonFile(path):
    code = readTextFile(path)
    context = {"__file__" : path}
    exec(code, context)
    return context

def iterPathsWithExtension(basepath, extension):
    extensions = setOfStrings(extension)
    for root, dirs, files in os.walk(basepath):
        for filename in files:
            _, ext = os.path.splitext(filename)
            if ext in extensions:
                yield os.path.join(root, filename)

def setOfStrings(strings):
    if isinstance(strings, str):
        return {strings}
    else:
        return set(strings)

def iterPathsWithFileName(basepath, filename):
    for root, dirs, files in os.walk(basepath):
        if filename in files:
            yield os.path.join(root, filename)

def iterAllFilePathsRecursive(directory):
    for root, dirs, files in os.walk(directory):
        for name in files:
            yield os.path.join(root, name)

def overwriteFile(source, target):
    removeFile(target)
    copyFile(source, target)

def copyFile(source, target):
    directory = os.path.dirname(target)
    if not directoryExists(directory):
        os.makedirs(directory)
    shutil.copyfile(source, target)

def removeFile(path):
    try:
        os.remove(path)
    except:
        if tryGetFileAccessPermission(path):
            os.remove(path)

def removeDirectory(path):
    try: shutil.rmtree(path, onerror = handlePermissionError)
    except FileNotFoundError: pass

def handlePermissionError(func, path, exc):
    if tryGetFileAccessPermission(path):
        func(path)
    else:
        raise

def tryGetFileAccessPermission(path):
    try:
        if os.access(path, os.W_OK):
            return False
        else:
            os.chmod(path, stat.S_IWUSR)
            return True
    except:
        return False

def readBinaryFile(path):
    with open(path, "rb") as f:
        return f.read()

def writeBinaryFile(path, content):
    with open(path, "wb") as f:
        f.write(content)

def readTextFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeTextFile(path, content):
    with open(path, "wt") as f:
        f.write(content)

def readJsonFile(path):
    return json.loads(readTextFile(path))

def writeJsonFile(path, content):
    writeTextFile(path, json.dumps(content, sort_keys = True, indent = 2))

def changeFileName(path, newName):
    return os.path.join(os.path.dirname(path), newName)

def changeFileExtension(path, newExtension):
    return os.path.splitext(path)[0] + newExtension

def filesExist(paths):
    assert all(fileExists(path) for path in paths)

def fileExists(path):
    return os.path.isfile(path)

def directoryExists(path):
    return os.path.isdir(path)

def dependenciesChanged(target, dependencies):
    targetTime = tryGetLastModificationTime(target)
    for path in dependencies:
        if tryGetLastModificationTime(path) > targetTime:
            return True
    return False

def getNewestPath(paths):
    pathsWithTime = [(path, tryGetLastModificationTime(path)) for path in paths]
    return max(pathsWithTime, key = lambda x: x[1])[0]

def tryGetLastModificationTime(path):
    try: return os.stat(path).st_mtime
    except: return 0

def getFileNameWithoutExtension(path):
    return os.path.basename(os.path.splitext(path)[0])

def splitPath(path):
    return pathlib.PurePath(path).parts

def multiReplace(text, **replacements):
    pattern = "|".join(re.escape(key) for key in replacements.keys())
    return re.sub(pattern, lambda m: replacements[m.group(0)], text)

def readLinesBetween(path, start, stop):
    lines = []
    with open(path, "rt") as f:
        while True:
            line = f.readline()
            if line == "":
                raise Exception("Line containing '{}' not found in {}".format(start, path))
            if start in line:
                break

        while True:
            line = f.readline()
            if line == "":
                raise Exception("Line containing '{}' not found in  {}".format(stop, path))
            if stop not in line:
                lines.append(line)
            else:
                break
    return "".join(lines)

def getPyxTargetLanguage(path):
    text = readTextFile(path)
    if re.search(r"^#\s*distutils\s*:\s*language\s*=\s*c\+\+", text, flags = re.MULTILINE):
        return "c++"
    else:
        return "c"

def syncDirectories(source, target, relpathSelector):
    if not directoryExists(target):
        os.mkdir(target)

    existingFilesInSource = set(relpathSelector(source))
    existingFilesInTarget = set(relpathSelector(target))

    removedFiles = []
    createdFiles = []
    updatedFiles = []

    filesToRemove = existingFilesInTarget - existingFilesInSource
    for relativePath in filesToRemove:
        path = os.path.join(target, relativePath)
        removeFile(path)
        removedFiles.append(path)

    filesToCreate = existingFilesInSource - existingFilesInTarget
    for relativePath in filesToCreate:
        sourcePath = os.path.join(source, relativePath)
        targetPath = os.path.join(target, relativePath)
        copyFile(sourcePath, targetPath)
        createdFiles.append(targetPath)

    filesToUpdate = existingFilesInSource.intersection(existingFilesInTarget)
    for relativePath in filesToUpdate:
        sourcePath = os.path.join(source, relativePath)
        targetPath = os.path.join(target, relativePath)
        lastSourceModification = tryGetLastModificationTime(sourcePath)
        lastTargetModification = tryGetLastModificationTime(targetPath)
        if lastSourceModification > lastTargetModification:
            overwriteFile(sourcePath, targetPath)
            updatedFiles.append(targetPath)

    return {
        "removed" : removedFiles,
        "created" : createdFiles,
        "updated" : updatedFiles
    }

def returnChangedFileStates(directory):
    def _returnChangedFileStates(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            before = getAllFilesWithTimestamps(directory)
            function(*args, **kwargs)
            after = getAllFilesWithTimestamps(directory)

            newFiles = set(after.keys()) - set(before.keys())
            removedFiles = set(before.keys()) - set(after.keys())
            changedFiles = {path for path, t in after.items() if t > before.get(path, 0)} - newFiles

            return {
                "new" : newFiles,
                "removed" : removedFiles,
                "changed" : changedFiles
            }
        return wrapper
    return _returnChangedFileStates

def getAllFilesWithTimestamps(directory):
    result = {}
    for path in iterAllFilePathsRecursive(directory):
        result[path] = tryGetLastModificationTime(path)
    return result

def getAddonVersion(initPath):
    match = re.search(r'"version"\s*:\s*(\(\s*[0-9]+\s*,\s*[0-9]+\s*,\s*[0-9]+\s*\))', readTextFile(initPath))
    if match is None:
        raise Exception("cannot determine addon version")
    return eval(match.group(1))


allFunctions = list(set(globals().keys()) - _globals - {"_globals"})


class Utils:
    pass

for fName in allFunctions:
    setattr(Utils, fName, globals()[fName])


__all__ = allFunctions + ["Utils"]
