import shutil

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox, QInputDialog

from globals import paths
from helpers.filecontrol import CreateFolder
from ui.SettingsWindow import Ui_SettingsWindow


class SettingsWindow(QWidget, Ui_SettingsWindow):
    def __init__(self, source, *args, **kwargs):
        super(SettingsWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon("../res/SpeedSoulsFlameSmallSquare.png"))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.currentPath = None

        self.source = source
        self.setupUi(self)
        self.initComponents()
        self.initConnections()

    def initConnections(self):
        self.pushButtonDelete.pressed.connect(self.deleteProfile)
        self.pushButtonNew.pressed.connect(self.createProfile)
        self.comboBoxGames.currentTextChanged.connect(self.onComboBoxChange)

    def initComponents(self):
        self.comboBoxGames.clear()
        for k, v in paths.items():
            self.comboBoxGames.addItem(k)
        self.onComboBoxChange()

    def onComboBoxChange(self):
        self.currentPath = paths[self.comboBoxGames.currentText()]
        self.lineEditPath.setText(str(self.currentPath))
        self.updateListWidgetProfiles()

    def updateListWidgetProfiles(self):
        self.listWidgetProfiles.clear()
        for path in self.currentPath.parent.iterdir():
            if path.is_dir():
                self.listWidgetProfiles.addItem(path.name)

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
        self.source.updateComboBox()
        self.source.showMessage("Profile deleted: " + currentItem)

