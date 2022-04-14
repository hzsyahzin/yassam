"""

To implement:
    - Copy/paste folders
    - Game Select
    - Settings
    - Persist cbx index
    - Profile deletion
    - Readme

"""
import os
import sys
from pathlib import Path, PurePath

from PyQt6.QtGui import QActionGroup, QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog

from filecontrol import CreateFolder
from ui.MainWindow import Ui_MainWindow

rootPath = Path.home() / "Documents/Test"
savefileName = "DRAKS0005.sl2"

paths = {
    "DS1: PTDE": Path.home() / "Documents/NBGI/DarkSouls/DRAKS0005.sl2",
    "DS1: Remastered": None,
    "DS2: Vanilla": None,
    "DS2: SOTFS": None,
    "DS3": None,
}


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon("../res/SpeedSoulsFlameSmallWhite.png"))

        self.rootPath = None
        self.activePath = None
        self.treeViewPath = None

        self.setupUi(self)
        self.treeView.parent = self

        self.gameGroup = QActionGroup(self)
        self.gameGroup.addAction(self.actionDS1_PTDE)
        self.gameGroup.addAction(self.actionDS1_Remastered)
        self.gameGroup.addAction(self.actionDS2_Vanilla)
        self.gameGroup.addAction(self.actionDS2_SOTFS)
        self.gameGroup.addAction(self.actionDS3)

        self.actionDS1_PTDE.setChecked(True)

        self.menuEdit.insertAction(self.actionCopy, self.actionReplace)
        self.menuEdit.insertSeparator(self.actionCopy)

        self.updateGame(self.gameGroup.checkedAction())
        self.updateMenu()
        self.initConnections()

    def getCurrentProfile(self):
        return self.comboBoxProfile.currentText()

    def getSavefileLocation(self):
        return self.rootPath / savefileName

    def initConnections(self):
        self.comboBoxProfile.currentTextChanged.connect(self.onComboBoxChanged)

        self.actionImport.triggered.connect(self.treeView.importSavefile)
        self.actionReplace.triggered.connect(self.treeView.replaceSavefile)
        self.actionLoad.triggered.connect(self.treeView.loadSavefile)

        self.actionCopy.triggered.connect(self.treeView.copyItem)
        self.actionPaste.triggered.connect(self.treeView.pasteItem)

        self.actionRename.triggered.connect(self.treeView.renameItem)
        self.actionDelete.triggered.connect(self.treeView.deleteItem)
        self.actionNew_Folder.triggered.connect(self.treeView.createFolder)

        self.gameGroup.triggered.connect(self.updateGame)

        self.pushButtonAddProfile.pressed.connect(self.onAddProfile)
        self.menubar.hovered.connect(self.updateMenu)
        self.treeView.customContextMenuRequested.connect(self.onContextMenuRequested)

    def updateGame(self, action: QAction):
        self.setWindowTitle(f"yassam - {action.text()}")

        self.rootPath = paths[action.text()].parent
        self.activePath = self.rootPath
        self.treeViewPath = PurePath(self.rootPath)
        self.updateComboBox()

    def updateMenu(self):
        if not self.treeView.selectedIndexes():
            self.actionCopy.setEnabled(False)
            self.actionRename.setEnabled(False)
            self.actionDelete.setEnabled(False)
            self.actionReplace.setEnabled(False)
        else:
            self.actionCopy.setEnabled(True)
            self.actionRename.setEnabled(True)
            self.actionDelete.setEnabled(True)
            if not os.path.isdir(self.treeView.getSelectedPath()):
                self.actionReplace.setEnabled(True)
            else:
                self.actionReplace.setEnabled(False)

        if not QApplication.clipboard().mimeData().urls():
            self.actionPaste.setEnabled(False)
        else:
            self.actionPaste.setEnabled(True)

    def updateComboBox(self):
        self.comboBoxProfile.clear()
        for path in self.rootPath.iterdir():
            if path.is_dir():
                self.comboBoxProfile.addItem(path.name)
        self.updatePath()

    def updatePath(self):
        self.treeView.savefileRootPath = self.rootPath
        self.activePath = self.rootPath / str(self.comboBoxProfile.currentText())
        self.treeView.setModelRootPath(self.activePath)

    def onContextMenuRequested(self, position):
        self.updateMenu()
        self.menuEdit.exec(self.treeView.viewport().mapToGlobal(position))

    def onComboBoxChanged(self):
        self.updatePath()
        self.showMessage(f"Profile changed to: {self.comboBoxProfile.currentText()}")

    def onAddProfile(self):
        profileName, dialogOk = QInputDialog().getText(
            self, "Create Profile", "Profile Name:")
        if dialogOk:
            msg, profileOk = CreateFolder(self.rootPath, profileName)
            if profileOk:
                self.updateComboBox()
                message = f"Profile created: {msg.name}"
            else:
                message = f"Error creating profile: {msg}"
        else:
            message = "Error creating profile: Invalid name"
        self.showMessage(message)

    def showMessage(self, message):
        self.statusbar.showMessage(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
