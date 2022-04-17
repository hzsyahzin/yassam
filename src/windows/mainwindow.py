import os
from pathlib import Path

from PyQt6.QtGui import QIcon, QActionGroup, QAction
from PyQt6.QtWidgets import QMainWindow, QApplication
from global_hotkeys import register_hotkeys, start_checking_hotkeys

from controllers.filecontroller import FileController
from controllers.settingscontroller import SettingsController
from ui.MainWindow import Ui_MainWindow
from windows.settingswindow import NeoSettingsWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon('speedsouls.ico'))

        self.setupUi(self)

        self.settingsController = SettingsController()

        self.settingsWindow = None

        self.gameActionGroup = QActionGroup(self)
        self.gameActions = [
            self.actionDS1_PTDE, self.actionDS1_Remastered,
            self.actionDS2_Vanilla, self.actionDS2_SOTFS, self.actionDS3]
        for index, action in enumerate(self.gameActions):
            action.setProperty("id", str(index))
            self.gameActionGroup.addAction(action)

        self.editActions = [
            self.actionCopy, self.actionRename, self.actionDelete, self.actionReplace]

        self.setupConnections()
        self.refresh()

    def setupConnections(self) -> None:
        self.menuEdit.aboutToShow.connect(self.onEditMenuOpen)
        self.gameActionGroup.triggered.connect(self.onGameChange)
        self.comboBoxProfile.currentTextChanged.connect(self.onProfileChange)
        self.pushButtonAddProfile.pressed.connect(self.onProfileAdd)

        self.actionImport.triggered.connect(self.treeView.onSavefileImport)
        self.actionReplace.triggered.connect(self.treeView.onSavefileReplace)
        self.actionLoad.triggered.connect(self.treeView.onSavefileLoad)
        self.actionCopy.triggered.connect(self.treeView.onItemCopy)
        self.actionPaste.triggered.connect(self.treeView.onItemPaste)
        self.actionRename.triggered.connect(self.treeView.onItemRename)
        self.actionDelete.triggered.connect(self.treeView.onItemDelete)
        self.actionNew_Folder.triggered.connect(self.treeView.onFolderCreate)
        self.actionSettings.triggered.connect(self.onSettingsOpen)
        self.treeView.postStatusMessage.connect(self.statusbar.showMessage)
        self.treeView.customContextMenuRequested.connect(self.onCxtMenuOpen)

    def refresh(self):
        """ Re-triggers active game selection to re-update widgets. """
        self.gameActions[self.settingsController.getActiveGameID()].trigger()

    def getActiveProfileDirectory(self) -> Path | None:
        return self.settingsController.getActiveSavefileDirectory() / self.comboBoxProfile.currentText()

    def setActiveGame(self, gameID: int) -> None:
        try:
            self.settingsController.setActiveGame(gameID)
            if self.settingsController.isSavefileValid(gameID):
                self.comboBoxProfile.populate(self.settingsController.getActiveSavefileDirectory())
                self.treeView.setFileModelRoot(self.getActiveProfileDirectory())
                self.showActiveView()
            else:
                raise AttributeError
        except AttributeError:
            self.showErrorView()

    def onProfileChange(self) -> None:
        self.treeView.setFileModelRoot(self.getActiveProfileDirectory())

    def onGameChange(self, gameAction: QAction) -> None:
        self.setWindowTitle(gameAction.text())
        self.setActiveGame(int(gameAction.property("id")))

    def onProfileAdd(self) -> None:
        if not FileController.createProfile(self.settingsController.getActiveGameID()):
            print("rip")  # TODO: Error message here
        self.comboBoxProfile.populate(self.settingsController.getActiveSavefileDirectory())

    def onSettingsOpen(self) -> None:
        self.settingsWindow = NeoSettingsWindow(self.settingsController)
        self.settingsWindow.aboutToClose.connect(self.refresh)
        self.settingsWindow.show()

    def onCxtMenuOpen(self, position) -> None:
        self.menuEdit.exec(self.treeView.viewport().mapToGlobal(position))

    def onEditMenuOpen(self) -> None:
        if not self.treeView.selectedIndexes():
            for action in self.editActions:
                action.setEnabled(False)
        else:
            for action in self.editActions:
                action.setEnabled(True)
            if os.path.isdir(self.treeView.getSelectedPath()):
                self.actionReplace.setEnabled(False)

        if not QApplication.clipboard().mimeData().urls():
            self.actionPaste.setEnabled(False)
        else:
            self.actionPaste.setEnabled(True)

    def showActiveView(self) -> None:
        self.treeView.show()
        self.comboBoxProfile.show()
        self.pushButtonAddProfile.show()
        self.labelHelp.hide()

    def showErrorView(self) -> None:
        self.treeView.hide()
        self.comboBoxProfile.hide()
        self.pushButtonAddProfile.hide()

        self.labelHelp.setText(f'Error retrieving savefile data for {self.settingsController.getActiveGameName()}')
        self.labelHelp.show()
