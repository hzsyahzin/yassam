import os
from pathlib import Path, PurePath

from PyQt6.QtCore import Qt, QDir
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

        self.setHeaderHidden(True)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)

        self.initConnections()

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
            path = self.model.filePath(self.selectedIndexes()[0])
        message, _ = CreateFolder(path, "New Folder")
        self.parent.showMessage(message)

    def importSavefile(self):
        sourcePath = self.parent.getSavefileLocation()
        print(sourcePath)
        if not self.selectedIndexes():
            destinationPath = self.rootPath
        else:
            destinationPath = self.model.filePath(self.selectedIndexes()[0])
        destinationPath = PurePath(destinationPath, sourcePath.name)
        message, _ = CopyFile(sourcePath, destinationPath)
        self.parent.showMessage(message)

    def renameItem(self):
        self.edit(self.currentIndex())

    def deleteItem(self):
        if self.selectedIndexes():
            currentItem = self.currentIndex().data()
            confirmDialog = QMessageBox()
            confirmDialog.setIcon(QMessageBox.Icon.Critical)
            confirmDialog.setWindowTitle("Deleting Item")

            if os.path.isdir(self.model.filePath(self.currentIndex())):
                message = f"{currentItem} and all children will be deleted."
            else:
                message = f"{currentItem} will be deleted."

            confirmDialog.setText(message)
            confirmDialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

            confirmValue = confirmDialog.exec()
            if confirmValue == QMessageBox.StandardButton.Ok:
                self.parent.showMessage(f"Deleted item: {currentItem}")
                self.model.remove(self.currentIndex())
        else:
            self.parent.showMessage(f"Error deleting item: No item selected.")

    def onItemChange(self, _, old, new) -> None:
        self.parent.showMessage(f"{old} renamed to: {new}")

    def mousePressEvent(self, event) -> None:
        self.clearSelection()
        QTreeView.mousePressEvent(self, event)
        self.parent.updateMenu()
