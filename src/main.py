"""

To implement:
    - Load
    - Replace
    - Cut
    - Copy
    - Paste
    - New Folder
    - Game Select
    - Settings
    - Persist cbx index
    - Profile deletion

"""

import sys
import os
import shutil
from pathlib import Path, PurePath

from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import Qt, QDir

from ui.MainWindow import Ui_MainWindow

rootPath = Path.home() / "Documents/Test"
savefileName = "DRAKS0005.sl2"


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.treeModel = QFileSystemModel()

        self.rootPath = rootPath / "Documents/NBGI/DarkSouls"
        self.treeViewPath = PurePath(rootPath)

        self.setupUi(self)

        self.initTreeView()
        self.initConnections()

        self.updateComboBox()

    def getCurrentProfile(self):
        return self.comboBoxProfile.currentText()

    def initConnections(self):

        self.treeView.customContextMenuRequested.connect(self.onContextMenuRequested)
        # noinspection PyUnresolvedReferences
        self.treeModel.fileRenamed.connect(self.onItemChanged)

        self.comboBoxProfile.currentTextChanged.connect(self.onComboBoxChanged)

        self.actionImport.triggered.connect(self.onImport)
        self.actionRename.triggered.connect(self.onRename)
        self.actionDelete.triggered.connect(self.onDelete)
        self.actionNew_Folder.triggered.connect(self.onNewFolder)

        self.pushButtonAddProfile.pressed.connect(self.onAddProfile)

        self.menubar.hovered.connect(self.updateMenu)

    def initTreeView(self):
        self.treeModel.setRootPath(str(self.rootPath))
        self.treeModel.setReadOnly(False)

        self.treeView.setModel(self.treeModel)
        self.treeView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.updateTreeView()

        self.treeView.setHeaderHidden(True)
        self.treeView.setColumnHidden(1, True)
        self.treeView.setColumnHidden(2, True)
        self.treeView.setColumnHidden(3, True)

    def updateMenu(self):
        indexes = self.treeView.selectedIndexes()
        if not indexes:
            self.actionCut.setEnabled(False)
            self.actionCopy.setEnabled(False)
            self.actionRename.setEnabled(False)
            self.actionDelete.setEnabled(False)
            self.actionReplace.setEnabled(False)
        else:
            self.actionCut.setEnabled(True)
            self.actionCopy.setEnabled(True)
            self.actionRename.setEnabled(True)
            self.actionDelete.setEnabled(True)
            self.actionReplace.setEnabled(True)

    def updateComboBox(self):
        self.comboBoxProfile.clear()
        for path in self.rootPath.iterdir():
            if path.is_dir():
                self.comboBoxProfile.addItem(path.name)
        self.updatePath()

    def updatePath(self):
        self.treeViewPath = self.rootPath / str(self.comboBoxProfile.currentText())

    def updateTreeView(self):
        self.treeView.setRootIndex(self.treeModel.index(self.treeViewPath.as_posix()))

    def onNewFolder(self):
        try:
            QDir(str(self.rootPath / self.getCurrentProfile())).mkdir("New Folder")
        except Exception as e:
            self.statusbar.showMessage(e)

    def onContextMenuRequested(self, position):
        self.updateMenu()
        self.menuEdit.exec(self.treeView.viewport().mapToGlobal(position))

    def onComboBoxChanged(self):
        self.updatePath()
        self.updateTreeView()
        self.statusbar.showMessage(f"Profile changed to: {self.comboBoxProfile.currentText()}")

    def onImport(self):
        try:
            sourcePath = self.rootPath / savefileName
            destinationPath = self.treeViewPath / savefileName
            if os.path.exists(destinationPath):
                newDestinationPath = destinationPath
                i = 1
                while os.path.exists(newDestinationPath):
                    newDestinationPath = PurePath(
                        destinationPath.parents[0], f"{destinationPath.stem} ({i}){destinationPath.suffix}")
                    i += 1
                destinationPath = newDestinationPath
            shutil.copyfile(sourcePath, destinationPath)
            message = f"Savefile imported as: {destinationPath.name}"
        except Exception as e:
            message = f"Error importing savefile: {e}"
        self.statusbar.showMessage(message)

    def onDelete(self):
        indexes = self.treeView.selectedIndexes()
        if indexes:
            currentItem = self.treeView.currentIndex().data()
            confirmDialog = QMessageBox()
            confirmDialog.setIcon(QMessageBox.Icon.Critical)
            confirmDialog.setWindowTitle("Deleting Item")

            if os.path.isdir(self.treeModel.filePath(self.treeView.currentIndex())):
                message = f"{currentItem} and all children will be deleted."
            else:
                message = f"{currentItem} will be deleted."

            confirmDialog.setText(message)
            confirmDialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

            confirmValue = confirmDialog.exec()
            if confirmValue == QMessageBox.StandardButton.Ok:
                self.statusbar.showMessage(f"Deleted item: {currentItem}")
                self.treeModel.remove(self.treeView.currentIndex())
        else:
            self.statusbar.showMessage(f"Error deleting item: No item selected.")

    def onRename(self):
        self.treeView.edit(self.treeView.currentIndex())

    def onItemChanged(self, path, oldName, newName):
        print(path)
        self.statusbar.showMessage(f"{oldName} renamed to: {newName}")

    def onAddProfile(self):
        profileName, ok = QInputDialog().getText(
            self, "Create Profile", "Profile Name:")
        if ok:
            try:
                QDir(self.rootPath.as_posix()).mkdir(profileName)
                self.updateComboBox()
                message = f"Profile created as: {profileName}"
            except Exception as e:
                message = f"Error creating profile: {e}"
        else:
            message = "Error creating profile: Invalid name"
        self.statusbar.showMessage(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
