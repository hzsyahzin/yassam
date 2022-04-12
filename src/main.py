"""

To implement:
    - Replace
    - Cut
    - Copy
    - Paste
    - Game Select
    - Settings
    - Persist cbx index
    - Profile deletion

"""

import sys
from pathlib import Path, PurePath

from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog

from filecontrol import CreateFolder
from ui.MainWindow import Ui_MainWindow

rootPath = Path.home() / "Documents/Test"
savefileName = "DRAKS0005.sl2"


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.rootPath = rootPath / "Documents/NBGI/DarkSouls"
        self.activePath = self.rootPath
        self.treeViewPath = PurePath(rootPath)

        self.setupUi(self)
        self.treeView.parent = self

        self.menuEdit.insertAction(self.actionCut, self.actionReplace)
        self.menuEdit.insertSeparator(self.actionCut)

        self.updateComboBox()
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
        self.actionRename.triggered.connect(self.treeView.renameItem)
        self.actionDelete.triggered.connect(self.treeView.deleteItem)
        self.actionNew_Folder.triggered.connect(self.treeView.createFolder)

        self.pushButtonAddProfile.pressed.connect(self.onAddProfile)
        self.menubar.hovered.connect(self.updateMenu)
        self.treeView.customContextMenuRequested.connect(self.onContextMenuRequested)

    def updateMenu(self):
        if not self.treeView.selectedIndexes():
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
        self.activePath = self.rootPath / str(self.comboBoxProfile.currentText())
        self.treeView.setRootPath(self.activePath)

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
