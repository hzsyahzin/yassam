from pathlib import Path

from PyQt6.QtCore import Qt, QDir, pyqtSignal
from PyQt6.QtGui import QIcon, QFileSystemModel, QKeySequence
from PyQt6.QtWidgets import QWidget, QFileDialog, QVBoxLayout, QMessageBox

from controllers.filecontroller import FileController
from ui.SettingsWindow import Ui_SettingsWindow


class SettingsWindow(QWidget, Ui_SettingsWindow):
    aboutToClose = pyqtSignal()

    def __init__(self, settingsController, *args, **kwargs):
        super(SettingsWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon("icons:speedsouls.ico"))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.setupUi(self)

        self.settingsController = settingsController

        self.fileModel = QFileSystemModel()
        self.fileModel.setReadOnly(False)
        self.fileModel.setFilter(QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot)

        self.listView.setModel(self.fileModel)
        self.listView.setLayout(QVBoxLayout())
        self.listView.layout().addWidget(self.labelHelp)

        self.comboBoxGames.populate(self.settingsController.getGameList())

        self.setupConnections()
        self.setupHotkeys()
        self.refresh()

    def refresh(self):
        """ Re-triggers combobox selection to re-update widgets. """
        self.onComboBoxChange()

    def setupConnections(self):
        self.keyInputLoad.editingFinished.connect(self.onHotkeySet)
        self.keyInputReplace.editingFinished.connect(self.onHotkeySet)
        self.keyInputImport.editingFinished.connect(self.onHotkeySet)
        self.pushButtonRename.pressed.connect(self.onProfileRename)
        self.pushButtonBrowse.pressed.connect(self.onSavefileBrowse)
        self.pushButtonAdd.pressed.connect(self.onProfileAdd)
        self.pushButtonDelete.pressed.connect(self.onProfileDelete)
        self.comboBoxGames.currentTextChanged.connect(self.onComboBoxChange)
        self.checkBoxHotkey.stateChanged.connect(self.onGlobalHotkeyCheck)
        self.listView.pressed.connect(self.onListViewPress)
        self.listView.itemDelegate().closeEditor.connect(self.refresh)

    def setupHotkeys(self):
        self.checkBoxHotkey.setChecked(self.settingsController.isGlobalHotkey())
        self.keyInputLoad.setKeySequence(QKeySequence(self.settingsController.getHotkey("Load")))
        self.keyInputReplace.setKeySequence(QKeySequence(self.settingsController.getHotkey("Replace")))
        self.keyInputImport.setKeySequence(QKeySequence(self.settingsController.getHotkey("Import")))

    def setFileModelRoot(self, path: Path) -> None:
        self.fileModel.setRootPath(str(path))
        self.listView.setRootIndex(self.fileModel.index(str(path)))

    def onGlobalHotkeyCheck(self, state: int) -> None:
        self.settingsController.setGlobalHotkey(bool(state))

    def onHotkeySet(self) -> None:
        self.settingsController.setHotkey("Load", self.keyInputLoad.keySequence().toString())
        self.settingsController.setHotkey("Replace", self.keyInputReplace.keySequence().toString())
        self.settingsController.setHotkey("Import", self.keyInputImport.keySequence().toString())

    def onComboBoxChange(self) -> None:
        savefileDirectory = self.settingsController.getSavefileDirectory(self.comboBoxGames.getSelectedGameID())
        if savefileDirectory:
            self.showActiveView()
            self.setFileModelRoot(savefileDirectory)
            self.lineEditPath.setText(str(savefileDirectory))
        else:
            self.showErrorView()

    def onListViewPress(self) -> None:
        if self.listView.selectedIndexes():
            self.pushButtonDelete.setEnabled(True)
            self.pushButtonRename.setEnabled(True)
        else:
            self.pushButtonDelete.setEnabled(False)
            self.pushButtonRename.setEnabled(False)

    def onProfileRename(self) -> None:
        self.listView.edit(self.listView.currentIndex())

    def onProfileAdd(self) -> None:
        if not FileController.createProfile(self.comboBoxGames.getSelectedGameID()):
            QMessageBox.critical(self, "Error creating profile", "Profile was unable to be created.")

    def onProfileDelete(self) -> None:
        if not FileController.deleteProfile(
                self.comboBoxGames.getSelectedGameID(), self.listView.currentIndex().data()):
            QMessageBox.critical(self, "Error creating profile", "Profile was unable to be deleted.")

    def onSavefileBrowse(self) -> None:
        savefilePath = QFileDialog.getOpenFileName(self, "Select Savefile")[0]
        if savefilePath:
            self.settingsController.setSavefilePath(self.comboBoxGames.getSelectedGameID(), Path(savefilePath))
        self.refresh()

    def showActiveView(self) -> None:
        self.listView.clearSelection()
        self.pushButtonDelete.setEnabled(False)
        self.pushButtonRename.setEnabled(False)
        self.pushButtonAdd.setEnabled(True)
        self.listView.setModel(self.fileModel)
        self.labelHelp.hide()

    def showErrorView(self, noSavefile=True) -> None:
        self.listView.setModel(None)
        self.listView.clearSelection()
        self.pushButtonDelete.setEnabled(False)
        self.pushButtonRename.setEnabled(False)
        self.pushButtonAdd.setEnabled(False)

        if noSavefile:
            self.lineEditPath.clear()
            self.labelHelp.setText(f"No savefile location set for {self.comboBoxGames.currentText()}")
        self.labelHelp.show()

    def closeEvent(self, event) -> None:
        self.aboutToClose.emit()
