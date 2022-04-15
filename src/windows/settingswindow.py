import shutil
import os
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFileSystemModel
from PyQt6.QtWidgets import QWidget, QMessageBox, QInputDialog, QFileDialog, QLineEdit

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

        self.pushButtonDelete.setEnabled(False)
        self.pushButtonRename.setEnabled(False)

    def initConnections(self):
        self.listWidgetProfiles.pressed.connect(self.onListWidgetProfilesPressed)
        self.pushButtonRename.pressed.connect(self.onButtonRenamePressed)
        self.pushButtonDelete.pressed.connect(self.deleteProfile)
        self.pushButtonNew.pressed.connect(self.createProfile)
        self.pushButtonBrowse.pressed.connect(self.onButtonBrowsePressed)
        self.comboBoxGames.currentTextChanged.connect(self.onComboBoxChange)
        # self.listWidgetProfiles.itemDelegate().closeEditor.connect(self.test)

    def initComponents(self):
        self.comboBoxGames.clear()
        for k, v in self.settings["savefiles"].items():
            self.comboBoxGames.addItem(k)
        self.onComboBoxChange()

    def onListWidgetProfilesPressed(self):
        if self.listWidgetProfiles.selectedIndexes():
            self.pushButtonDelete.setEnabled(True)
            self.pushButtonRename.setEnabled(True)

    def onButtonBrowsePressed(self):
        fileName = QFileDialog.getOpenFileName(self, "Select Savefile", str(Path.home()))[0]
        self.settings["savefiles"][self.comboBoxGames.currentText()] = fileName
        SaveSettings(self.settings)
        self.onComboBoxChange()
        self.source.refreshWindow()

    def onButtonRenamePressed(self):
        self.listWidgetProfiles.edit(self.listWidgetProfiles.selectedIndexes()[0])

    def onComboBoxChange(self):
        self.currentPath = Path(self.settings["savefiles"][self.comboBoxGames.currentText()])
        self.lineEditPath.setText(str(self.currentPath))
        self.updateListWidgetProfiles()

    def updateListWidgetProfiles(self):
        self.listWidgetProfiles.clear()
        for path in self.currentPath.parent.iterdir():
            if path.is_dir():
                self.listWidgetProfiles.addItem(path.name)
        for i in range(self.listWidgetProfiles.count()):
            item = self.listWidgetProfiles.item(i)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)

    def createProfile(self):
        profileName, dialogOk = QInputDialog().getText(
            self, "Create Profile", "Profile Name:")
        if dialogOk:
            msg, profileOk = CreateFolder(self.currentPath.parent, profileName)
            if profileOk:
                self.updateListWidgetProfiles()
                message = f"Profile created: {msg.name}"
            else:
                message = f"Error creating profile: {msg}"
        else:
            message = "Error creating profile: Invalid name"
        self.source.showMessage(message)

    def deleteProfile(self):
        currentItem = ""
        if self.listWidgetProfiles.selectedIndexes():
            currentItem = self.listWidgetProfiles.currentIndex().data()
            confirmDialog = QMessageBox()
            confirmDialog.setIcon(QMessageBox.Icon.Critical)
            confirmDialog.setWindowTitle("Deleting Item")
            confirmDialog.setText(f"Profile {currentItem} and all\nsavefiles will be deleted.")
            confirmDialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

            confirmValue = confirmDialog.exec()
            if confirmValue == QMessageBox.StandardButton.Ok:
                shutil.rmtree(self.currentPath.parent / self.listWidgetProfiles.selectedIndexes()[0].data())
        self.updateListWidgetProfiles()
        self.source.refreshWindow()
        self.source.showMessage("Profile deleted: " + currentItem)

