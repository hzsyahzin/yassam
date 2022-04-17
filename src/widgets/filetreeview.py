import os
from pathlib import Path, PurePath

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QTreeView, QMessageBox, QAbstractItemView, QApplication

from controllers.settingscontroller import SettingsController
from controllers.filecontroller import FileController


class FileTreeView(QTreeView):

    postStatusMessage = pyqtSignal(str)
    requestMenuUpdate = pyqtSignal()

    def __init__(self, parent=None):
        super(FileTreeView, self).__init__(parent)
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.model.setReadOnly(False)

        self.savefileRootPath = ""
        self.modelRootPath = ""

        self.setModel(self.model)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)

        self.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)

        self.setHeaderHidden(True)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)

        self.initConnections()

    def getSelectedPath(self):
        return PurePath(self.model.filePath(self.selectedIndexes()[0]))

    def hideTree(self):
        self.setColumnHidden(0, True)

    def showTree(self):
        self.setColumnHidden(0, False)

    def initConnections(self):
        self.model.fileRenamed.connect(self.onItemChange)

    def setModelRootPath(self, path: Path):
        self.modelRootPath = path.as_posix()
        self.model.setRootPath(self.modelRootPath)
        self.setRootIndex(self.model.index(self.modelRootPath))

    def copyItem(self):
        selectedItems = self.selectionModel().selectedIndexes()
        mimeData = self.model.mimeData(selectedItems)
        QApplication.clipboard().setMimeData(mimeData)
        self.postStatusMessage.emit(f"Item copied: {self.getSelectedPath().relative_to(self.modelRootPath)}")

    def pasteItem(self):
        sourcePaths = [PurePath(item.path()[1:]) for item in QApplication.clipboard().mimeData().urls()]
        if not self.selectedIndexes():
            destinationPath = PurePath(self.modelRootPath)
        else:
            destinationPath = self.getSelectedPath()
        for path in sourcePaths:
            if not os.path.isdir(destinationPath):
                destinationPath = destinationPath.parent
            msg, ok = FileController.copyFile(path, destinationPath / path.name, suffix=False)
            self.postStatusMessage.emit(f"Item pasted to: {msg.relative_to(self.modelRootPath)}")

    def createFolder(self):
        if not self.selectedIndexes():
            path = self.modelRootPath
        else:
            path = self.getSelectedPath()
        msg, ok = FileController.createFolder(path, "New Folder")
        if ok:
            message = f"Folder created: {msg.relative_to(self.modelRootPath)}"
        else:
            message = f"Error creating folder: {msg}"
        self.postStatusMessage.emit(message)

    def importSavefile(self):
        sourcePath = SettingsController().getSavefileLocation()
        destinationPath = self.modelRootPath

        indexes = self.selectedIndexes()
        if indexes:
            parentPath = PurePath(self.model.filePath(self.selectedIndexes()[0].parent()))
            if os.path.isdir(self.getSelectedPath()):
                destinationPath = self.getSelectedPath()
            elif os.path.isdir(parentPath):
                destinationPath = parentPath
        destinationPath = PurePath(destinationPath, sourcePath.name)
        msg, ok = FileController.copyFile(sourcePath, destinationPath)
        if ok:
            message = f"Savefile imported to: {msg.relative_to(self.modelRootPath)}"
        else:
            message = msg
        self.postStatusMessage.emit(message)

    def replaceSavefile(self):
        indexes = self.selectedIndexes()
        if len(indexes) == 1:
            sourcePath = SettingsController().getSavefileLocation()
            destinationPath = self.getSelectedPath()
            if not os.path.isdir(destinationPath):
                currentItem = self.currentIndex().data()
                confirmDialog = QMessageBox()
                confirmDialog.setIcon(QMessageBox.Icon.Warning)
                confirmDialog.setWindowTitle("Replacing Savefile")

                confirmDialog.setText(f"Savefile {currentItem} will be replaced.\nData will be lost.")
                confirmDialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

                confirmValue = confirmDialog.exec()
                if confirmValue == QMessageBox.StandardButton.Ok:
                    msg, ok = FileController.copyFile(sourcePath, destinationPath, overwrite=True)
                    if ok:
                        message = f"Savefile replaced: {msg.relative_to(self.modelRootPath)}"
                    else:
                        message = msg
                else:
                    message = ""
            else:
                message = "Error replacing savefile: Directory selected"
        elif len(indexes) > 1:
            message = "Error replacing savefile: More than one file selected"
        else:
            message = "Error replacing savefile: No file selected"
        self.postStatusMessage.emit(message)

    def loadSavefile(self):
        indexes = self.selectedIndexes()
        if len(indexes) == 1:
            savefilePath = SettingsController().getActiveSavefilePath()
            activePath = self.getSelectedPath()
            if not os.path.isdir(activePath):
                FileController.deleteFile(savefilePath)
                msg, ok = FileController.copyFile(activePath, savefilePath, overwrite=True)
                if ok:
                    message = f"Savefile loaded: {activePath.relative_to(self.modelRootPath)}"
                else:
                    message = f"Error loading savefile: {msg}"
            else:
                message = "Error loading savefile: Directory selected"
        elif len(indexes) > 1:
            message = "Error loading savefile: More than one file selected"
        else:
            message = "Error loading savefile: No file selected"
        self.postStatusMessage.emit(message)

    def renameItem(self):
        self.edit(self.currentIndex())

    def deleteItem(self):
        indexes = self.selectedIndexes()
        if len(indexes) == 1:
            currentItem = self.currentIndex().data()
            confirmDialog = QMessageBox()
            confirmDialog.setIcon(QMessageBox.Icon.Critical)
            confirmDialog.setWindowTitle("Deleting Item")

            if os.path.isdir(self.getSelectedPath()):
                msg = f"{currentItem} and any\nchildren will be deleted."
            else:
                msg = f"{currentItem} will be deleted."

            confirmDialog.setText(msg)
            confirmDialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

            confirmValue = confirmDialog.exec()
            if confirmValue == QMessageBox.StandardButton.Ok:
                message = f"Deleted item: {self.getSelectedPath().relative_to(self.modelRootPath)}"
                self.model.remove(self.currentIndex())
            else:
                message = ""
        elif len(indexes) > 1:
            message = "Error deleting item: No support for multiple items"
        else:
            message = "Error deleting item: No item selected."
        self.postStatusMessage.emit(message)

    def onItemChange(self, _, old, new) -> None:
        self.postStatusMessage.emit(f"{old} renamed to: {new}")

    def mousePressEvent(self, event) -> None:
        self.clearSelection()
        QTreeView.mousePressEvent(self, event)
        self.requestMenuUpdate.emit()
