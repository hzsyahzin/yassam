import shutil
from pathlib import Path

from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QIcon, QFileSystemModel
from PyQt6.QtWidgets import QWidget, QMessageBox, QInputDialog, QFileDialog

from helpers.filecontrol import CreateFolder
from helpers.database import LoadSettings, SaveSettings
from ui.SettingsWindow import Ui_SettingsWindow


class SettingsWindow(QWidget, Ui_SettingsWindow):
    def __init__(self, source, *args, **kwargs):
        super(SettingsWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon("../res/SpeedSoulsFlameSmallSquare.png"))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.currentPath = None
        self.settings = LoadSettings()
        self.model = QFileSystemModel()

        self.source = source
        self.setupUi(self)
        self.initComponents()
        self.initConnections()

        self.model.setReadOnly(False)
        self.model.setFilter(QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot)
        self.listView.setModel(self.model)
        self.setModelRoot()

        self.lineEditPath.setReadOnly(True)

        self.pushButtonDelete.setEnabled(False)
        self.pushButtonRename.setEnabled(False)

    def initConnections(self):
        self.pushButtonRename.pressed.connect(self.renameProfile)
        self.pushButtonBrowse.pressed.connect(self.browseSavefiles)
        self.pushButtonNew.pressed.connect(self.createProfile)
        self.pushButtonDelete.pressed.connect(self.deleteProfile)
        self.comboBoxGames.currentTextChanged.connect(self.onComboBoxChange)
        self.listView.pressed.connect(self.onListViewPressed)
        self.listView.itemDelegate().closeEditor.connect(self.onRename)

    def initComponents(self):
        self.comboBoxGames.clear()
        for k, v in self.settings["savefiles"].items():
            self.comboBoxGames.addItem(k)
        self.onComboBoxChange()

    def noSavefileError(self):
        self.listView.hide()
        self.pushButtonDelete.hide()
        self.pushButtonRename.hide()
        self.pushButtonNew.hide()
        self.currentPath = Path.home() / "Documents"
        self.setModelRoot()
        self.lineEditPath.clear()

    def setModelRoot(self):
        self.model.setRootPath(str(self.currentPath.parent))
        self.listView.setRootIndex(self.model.index(str(self.currentPath.parent)))

    def onListViewPressed(self):
        if self.listView.selectedIndexes():
            self.pushButtonDelete.setEnabled(True)
            self.pushButtonRename.setEnabled(True)

    def onRename(self, e):
        self.source.refreshWindow()
        self.source.showMessage("Profile renamed to: " + e.text())

    def renameProfile(self):
        self.listView.edit(self.listView.currentIndex())

    def browseSavefiles(self):
        fileName = QFileDialog.getOpenFileName(self, "Select Savefile", str(Path.home()))[0]
        if fileName != "":
            self.settings["savefiles"][self.comboBoxGames.currentText()] = fileName
        SaveSettings(self.settings)
        self.onComboBoxChange()
        self.source.refreshWindow()

    def onComboBoxChange(self):
        try:
            self.listView.show()
            self.pushButtonDelete.show()
            self.pushButtonRename.show()
            self.pushButtonNew.show()
            self.currentPath = Path(self.settings["savefiles"][self.comboBoxGames.currentText()])
            self.lineEditPath.setText(str(self.currentPath))
            self.setModelRoot()
        except TypeError:
            self.noSavefileError()

    def createProfile(self):
        profileName, dialogOk = QInputDialog().getText(
            self, "Create Profile", "Profile Name:")
        if dialogOk:
            msg, profileOk = CreateFolder(self.currentPath.parent, profileName)
            if profileOk:
                message = f"Profile created: {msg.name}"
            else:
                message = f"Error creating profile: {msg}"
        else:
            message = "Error creating profile: Invalid name"
        self.source.refreshWindow()
        self.source.showMessage(message)

    def deleteProfile(self):
        currentItem = ""
        if self.listView.selectedIndexes():
            currentItem = self.listView.currentIndex().data()
            confirmDialog = QMessageBox()
            confirmDialog.setIcon(QMessageBox.Icon.Critical)
            confirmDialog.setWindowTitle("Deleting Item")
            confirmDialog.setText(f"Profile {currentItem} and all\nsavefiles will be deleted.")
            confirmDialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

            confirmValue = confirmDialog.exec()
            if confirmValue == QMessageBox.StandardButton.Ok:
                shutil.rmtree(self.currentPath.parent / self.listView.selectedIndexes()[0].data())
        self.source.refreshWindow()
        self.source.showMessage("Profile deleted: " + currentItem)

