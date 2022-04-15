import os
from pathlib import PurePath, Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QActionGroup, QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QInputDialog, QLabel
from global_hotkeys import register_hotkeys, start_checking_hotkeys

from helpers.filecontrol import CreateFolder
from helpers.database import LoadSettings, SaveSettings
from ui.MainWindow import Ui_MainWindow
from windows.settingswindow import SettingsWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon('speedsouls.ico'))

        self.savefilePaths = None

        self.rootPath = None
        self.activePath = None
        self.treeViewPath = None
        self.savefileName = None

        self.settingsWindow = None

        self.setupUi(self)
        self.treeView.parent = self

        self.gameGroup = QActionGroup(self)
        self.gameGroup.addAction(self.actionDS1_PTDE)
        self.gameGroup.addAction(self.actionDS1_Remastered)
        self.gameGroup.addAction(self.actionDS2_Vanilla)
        self.gameGroup.addAction(self.actionDS2_SOTFS)
        self.gameGroup.addAction(self.actionDS3)

        self.games = {
            "DS1: PTDE": self.actionDS1_PTDE,
            "DS1: Remastered": self.actionDS1_Remastered,
            "DS2: Vanilla": self.actionDS2_Vanilla,
            "DS2: SOTFS": self.actionDS2_SOTFS,
            "DS3": self.actionDS3
        }

        self.games[LoadSettings()["current_game"]].setChecked(True)

        self.menuEdit.insertAction(self.actionCopy, self.actionReplace)
        self.menuEdit.insertSeparator(self.actionCopy)

        self.noSavefileLabel = QLabel(f'No savefile set for {LoadSettings()["current_game"]}\nSet the savefile '
                                      f'location in File > Settings')
        self.noSavefileLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.noSavefileLabel)

        self.refreshWindow()
        self.initConnections()

        self.registerHotkeys()
        start_checking_hotkeys()

    def registerHotkeys(self):
        bindings = [
            [[self.actionLoad.shortcut().toString()], None, self.treeView.loadSavefile],
            [[self.actionImport.shortcut().toString()], None, self.treeView.importSavefile],
            [[self.actionReplace.shortcut().toString()], None, self.treeView.replaceSavefile],
        ]
        register_hotkeys(bindings)

    def getCurrentProfile(self):
        return self.comboBoxProfile.currentText()

    def getSavefileLocation(self):
        return self.rootPath / self.savefileName

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

        self.actionSettings.triggered.connect(self.openSettings)

        self.gameGroup.triggered.connect(self.updateGame)

        self.pushButtonAddProfile.pressed.connect(self.onAddProfile)
        self.menubar.hovered.connect(self.updateMenu)
        self.treeView.customContextMenuRequested.connect(self.onContextMenuRequested)

    def updateGame(self, action: QAction):
        self.setWindowTitle(f"yassam - {action.text()}")
        try:
            self.noSavefileLabel.setText(f'No savefile set for {action.text()}\nSet the savefile '
                                         f'location in File > Settings')
            self.showWidgets()
            self.pushButtonAddProfile.setEnabled(True)
            newPath = Path(self.savefilePaths[action.text()])
            self.rootPath = newPath.parent
            self.savefileName = newPath.name
            self.activePath = self.rootPath
            self.treeViewPath = PurePath(self.rootPath)
            self.updateComboBox()
        except TypeError:
            self.noSavefileError()

    def openSettings(self):
        self.settingsWindow = SettingsWindow(source=self)
        self.settingsWindow.show()

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

    def refreshWindow(self):
        self.showWidgets()
        self.pushButtonAddProfile.setEnabled(True)
        self.savefilePaths = LoadSettings()["savefiles"]
        self.updateGame(self.gameGroup.checkedAction())
        self.updateMenu()

    def updateComboBox(self):
        self.comboBoxProfile.clear()
        try:
            for path in self.rootPath.iterdir():
                if path.is_dir():
                    self.comboBoxProfile.addItem(path.name)
            self.updatePath()
        except AttributeError:
            self.noSavefileError()

    def noSavefileError(self):
        self.comboBoxProfile.clear()
        self.treeView.setModelRootPath(Path.home())
        self.hideWidgets()

    def hideWidgets(self):
        self.noSavefileLabel.show()
        self.treeView.hide()
        self.pushButtonAddProfile.hide()
        self.comboBoxProfile.hide()
        self.statusbar.hide()

    def showWidgets(self):
        self.noSavefileLabel.hide()
        self.treeView.show()
        self.pushButtonAddProfile.show()
        self.comboBoxProfile.show()
        self.statusbar.show()

    def updatePath(self):
        try:
            self.treeView.savefileRootPath = self.rootPath
            self.activePath = self.rootPath / str(self.comboBoxProfile.currentText())
            self.treeView.setModelRootPath(self.activePath)
        except AttributeError:
            self.noSavefileError()

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

    def closeEvent(self, event) -> None:
        if self.settingsWindow:
            self.settingsWindow.close()
        settings = LoadSettings()
        settings["current_game"] = {v: k for k, v in self.games.items()}[self.gameGroup.checkedAction()]
        SaveSettings(settings)
