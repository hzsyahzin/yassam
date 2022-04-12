import os
from pathlib import Path, PurePath

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QTreeView, QMessageBox, QAbstractItemView

from filecontrol import CreateFolder, CopyFile
from main import MainWindow


class FileTreeView(QTreeView):

    def __init__(self, parent=None):
        super(FileTreeView, self).__init__(parent)
        self.parent: MainWindow = parent
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.model.setReadOnly(False)

        self.rootPath = ""

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

    def initConnections(self):
        self.model.fileRenamed.connect(self.onItemChange)

    def setRootPath(self, path: Path):
        self.rootPath = path.as_posix()
        self.model.setRootPath(self.rootPath)
        self.setRootIndex(self.model.index(self.rootPath))

    def createFolder(self):
        if not self.selectedIndexes():
            path = self.rootPath
        else:
            path = self.getSelectedPath()
        msg, ok = CreateFolder(path, "New Folder")
        if ok:
            message = f"Folder created: {msg.relative_to(self.rootPath)}"
        else:
            message = f"Error creating folder: {msg}"
        self.parent.showMessage(message)

    def importSavefile(self):
        sourcePath = self.parent.getSavefileLocation()
        destinationPath = self.rootPath
        if self.selectedIndexes() and os.path.isdir(self.getSelectedPath()):
            destinationPath = self.getSelectedPath()
        destinationPath = PurePath(destinationPath, sourcePath.name)
        msg, ok = CopyFile(sourcePath, destinationPath)
        if ok:
            message = f"Savefile imported to: {msg.relative_to(self.rootPath)}"
        else:
            message = msg
        self.parent.showMessage(message)

    def replaceSavefile(self):
        indexes = self.selectedIndexes()
        if len(indexes) == 1:
            sourcePath = self.parent.getSavefileLocation()
            destinationPath = self.getSelectedPath()
            if not os.path.isdir(destinationPath):
                msg, ok = CopyFile(sourcePath, destinationPath, overwrite=True)
                if ok:
                    message = f"Savefile replaced: {msg.relative_to(self.rootPath)}"
                else:
                    message = msg
            else:
                message = f"Error replacing savefile: Directory selected"
        elif len(indexes) > 1:
            message = f"Error replacing savefile: More than one file selected"
        else:
            message = f"Error replacing savefile: No file selected"
        self.parent.showMessage(message)

    def loadSavefile(self):
        indexes = self.selectedIndexes()
        if len(indexes) == 1:
            savefilePath = self.parent.getSavefileLocation()
            activePath = self.getSelectedPath()
            if not os.path.isdir(activePath):
                msg, ok = CopyFile(activePath, savefilePath, overwrite=True)
                if ok:
                    message = f"Savefile loaded: {activePath.relative_to(self.rootPath)}"
                else:
                    message = f"Error loading savefile: {msg}"
            else:
                message = "Error loading savefile: Directory selected"
        elif len(indexes) > 1:
            message = f"Error loading savefile: More than one file selected"
        else:
            message = f"Error loading savefile: No file selected"
        self.parent.showMessage(message)

    def renameItem(self):
        self.edit(self.currentIndex())

    def deleteItem(self):
        if self.selectedIndexes():
            currentItem = self.currentIndex().data()
            confirmDialog = QMessageBox()
            confirmDialog.setIcon(QMessageBox.Icon.Critical)
            confirmDialog.setWindowTitle("Deleting Item")

            if os.path.isdir(self.getSelectedPath()):
                message = f"{currentItem} and all children will be deleted."
            else:
                message = f"{currentItem} will be deleted."

            confirmDialog.setText(message)
            confirmDialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

            confirmValue = confirmDialog.exec()
            if confirmValue == QMessageBox.StandardButton.Ok:
                self.parent.showMessage(f"Deleted item: {self.getSelectedPath().relative_to(self.rootPath)}")
                self.model.remove(self.currentIndex())
        else:
            self.parent.showMessage(f"Error deleting item: No item selected.")

    def onItemChange(self, _, old, new) -> None:
        self.parent.showMessage(f"{old} renamed to: {new}")

    def mousePressEvent(self, event) -> None:
        self.clearSelection()
        QTreeView.mousePressEvent(self, event)
        self.parent.updateMenu()
