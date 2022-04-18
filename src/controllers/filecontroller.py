import os
import shutil
from distutils import dir_util
from pathlib import PurePath

from PyQt6.QtCore import QDir, QFile
from PyQt6.QtWidgets import QInputDialog, QMessageBox, QWidget

from controllers.settingscontroller import SettingsController


class FileController:
    @staticmethod
    def createProfile(gameID: int) -> bool:
        profileName, ok = QInputDialog().getText(QWidget(), "Create Profile", "Profile Name:")
        if profileName and ok:
            path, ok = FileController.createFolder(
                SettingsController().getSavefileDirectory(gameID), profileName)
            if ok:
                return True
        return False

    @staticmethod
    def deleteProfile(gameID: int, profileName: str) -> bool:
        ok = QMessageBox.warning(QWidget(), "Delete Profile",
                                 f"Profile {profileName} and all\n"
                                 f"associated savefiles will be deleted",
                                 QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        if ok == QMessageBox.StandardButton.Ok:
            shutil.rmtree(SettingsController().getSavefileDirectory(gameID) / profileName)
            return True
        return False

    @staticmethod
    def createFolder(destination, name):
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

    @staticmethod
    def deleteFolder(path):
        try:
            shutil.rmtree(path)
            message = path
            ok = True
        except Exception as e:
            message = e
            ok = False
        return message, ok

    @staticmethod
    def deleteFile(path):
        try:
            QFile.remove(str(path))
            message = PurePath(path)
            ok = True
        except Exception as e:
            message = e
            ok = False
        return message, ok

    @staticmethod
    def copyFile(source, destination, overwrite=False, suffix=True):
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
                FileController.deleteFile(destinationPath)
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
