import os
from pathlib import PurePath
from distutils import dir_util

from PyQt6.QtCore import QDir, QFile


def CreateFolder(destination, name):
    try:
        path = PurePath(destination, name)
        if os.path.exists(path):
            i = 1
            while os.path.exists(path):
                path = PurePath(destination, f"{name} ({i})")
                i += 1
        QDir(str(path.parent)).mkdir(path.name)
        message = path
        ok = True
    except Exception as e:
        message = e
        ok = False
    return message, ok


def DeleteFile(path):
    try:
        QFile.remove(str(path))
        message = PurePath(path)
        ok = True
    except Exception as e:
        message = e
        ok = False
    return message, ok


def CopyFile(source, destination, overwrite=False, suffix=True):
    try:
        sourcePath = PurePath(source)
        destinationPath = PurePath(destination)
        if suffix:
            destinationStem = destinationPath.stem
        else:
            destinationStem = destinationPath
        if not overwrite:
            if os.path.exists(destinationPath):
                i = 1
                while os.path.exists(destinationPath):
                    if suffix:
                        destinationPath = PurePath(
                            destinationPath.parent,
                            f"{destinationStem} ({i}){destinationPath.suffix}")
                    else:
                        destinationPath = PurePath(
                            destinationPath.parent,
                            f"{destinationStem} ({i})"
                        )
                    i += 1
        else:
            DeleteFile(destinationPath)
        if not os.path.isdir(sourcePath):
            QFile.copy(str(sourcePath), str(destinationPath))
        else:
            dir_util.copy_tree(str(sourcePath), str(destinationPath))
        message = destinationPath
        ok = True
    except Exception as e:
        message = e
        ok = False
    return message, ok

