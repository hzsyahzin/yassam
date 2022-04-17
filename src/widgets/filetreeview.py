import os
from pathlib import Path, PurePath

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QTreeView, QMessageBox, QApplication

from controllers.settingscontroller import SettingsController
from controllers.filecontroller import FileController


class FileTreeView(QTreeView):

    postStatusMessage = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super(FileTreeView, self).__init__(parent)

        self.fileModel = QFileSystemModel()
        self.fileModel.setReadOnly(False)
        self.setModel(self.fileModel)

        for i in range(1, 4):
            self.setColumnHidden(i, True)

        self.fileModel.fileRenamed.connect(self.onItemChange)

    def getSelectedPath(self, relative=False) -> Path | None:
        if not relative:
            return Path(self.fileModel.filePath(self.currentIndex()))
        return Path(self.fileModel.filePath(self.currentIndex())).relative_to(self.fileModel.rootPath())

    def setFileModelRoot(self, path: Path) -> None:
        self.fileModel.setRootPath(str(path))
        self.setRootIndex(self.fileModel.index(str(path)))

    def onSavefileLoad(self) -> None:
        if self.selectedIndexes():
            ok = FileController.loadSavefile(SettingsController().getActiveGameID(), self.getSelectedPath())
            message = "Savefile loaded" if ok else "Error loading savefile: Invalid file selected"
        else:
            message = "Error loading savefile: No file selected"
        self.postStatusMessage.emit(message)

    def onSavefileImport(self) -> None:
        sourcePath = SettingsController().getActiveSavefilePath()
        destinationPath = self.fileModel.rootPath()
        if self.selectedIndexes():
            selectedItem = self.getSelectedPath()
            destinationPath = selectedItem if os.path.isdir(selectedItem) else selectedItem.parent
        path, ok = FileController.copyFile(sourcePath, destinationPath / sourcePath.name)
        message = f"Savefile imported to: {path.relative_to(self.fileModel.rootPath())}" if ok else \
            f"Error importing savefile: {path}"
        self.postStatusMessage.emit(message)

    def onSavefileReplace(self) -> None:
        if self.selectedIndexes() and os.path.isfile(self.getSelectedPath()):
            message = ""
            ok = QMessageBox.warning(self, "Replace Savefile",
                                     f"Savefile {self.getSelectedPath().name} will be replaced",
                                     QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if ok == QMessageBox.StandardButton.Ok:
                path, ok = FileController.copyFile(
                    SettingsController().getActiveSavefilePath(), self.getSelectedPath(), overwrite=True)
                message = f"Savefile replaced: {self.getSelectedPath(relative=True)}" if ok else \
                    f"Error replacing savefile: {path}"
        else:
            message = f"Error replacing savefile: Invalid selection"
        self.postStatusMessage.emit(message)

    def onItemCopy(self) -> None:
        QApplication.clipboard().setMimeData(
            self.fileModel.mimeData(self.selectionModel().selectedIndexes()))
        self.postStatusMessage.emit(f"Item copied: {self.getSelectedPath(relative=True)}")

    def onItemPaste(self) -> None:
        sourcePaths = [PurePath(item.path()[1:]) for item in QApplication.clipboard().mimeData().urls()]
        destinationPath = self.getSelectedPath() if self.selectedIndexes() else Path(self.fileModel.rootPath())
        for path in sourcePaths:
            if not os.path.isdir(destinationPath):
                destinationPath = destinationPath.parent
            path, _ = FileController.copyFile(path, destinationPath / path.name, suffix=False)
            self.postStatusMessage.emit(f"Item pasted to: {path.relative_to(self.fileModel.rootPath())}")

    def onItemRename(self) -> None:
        self.edit(self.currentIndex())

    def onItemDelete(self) -> None:
        if self.selectedIndexes():
            message = ""
            ok = QMessageBox.warning(self, "Delete Item", f"Item {self.getSelectedPath().name} will be deleted",
                                     QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if ok == QMessageBox.StandardButton.Ok:
                message = f"Item deleted: {self.getSelectedPath(relative=True)}"
                self.fileModel.remove(self.currentIndex())
        else:
            message = "Error deleting item: No item selected"
        self.postStatusMessage.emit(message)

    def onFolderCreate(self) -> None:
        path = self.getSelectedPath() if self.selectedIndexes() else self.fileModel.rootPath()
        path, ok = FileController.createFolder(path, "New Folder")
        message = f"Folder created: {path.relative_to(self.fileModel.rootPath())}" if ok else \
            f"Error creating folder: {path} "
        self.postStatusMessage.emit(message)

    def onItemChange(self, _, oldName: str, newName: str) -> None:
        self.postStatusMessage.emit(f"{oldName} renamed to: {newName}")

    def mousePressEvent(self, event) -> None:
        self.clearSelection()
        QTreeView.mousePressEvent(self, event)
