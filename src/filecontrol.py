import os
from pathlib import PurePath

from PyQt6.QtCore import QDir, QFile


def CreateFolder(destination, name):
    try:
        path = PurePath(destination, name)
        if os.path.exists(path):
            i = 1
            while os.path.exists(path):
                path = PurePath(destination, f"New Folder ({i})")
                i += 1
        QDir(str(path.parent)).mkdir(path.name)
        message = f"Folder created: {path.name}"
        ok = True
    except Exception as e:
        message = f"Error creating folder: {e}"
        ok = False
    return message, ok


def CopyFile(source, destination):
    try:
        sourcePath = PurePath(source)
        destinationPath = PurePath(destination)
        destinationStem = destinationPath.stem
        if os.path.exists(destinationPath):
            i = 1
            while os.path.exists(destinationPath):
                destinationPath = PurePath(
                    destinationPath.parent,
                    f"{destinationStem} ({i}){destinationPath.suffix}")
                i += 1
        QFile.copy(str(sourcePath), str(destinationPath))
        message = f"File copied: {destinationPath.name}"
        ok = True
    except Exception as e:
        message = f"Error copying file: {e}"
        ok = False
    return message, ok

