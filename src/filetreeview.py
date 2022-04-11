from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QTreeView


class FileTreeView(QTreeView):
    #
    # def __init__(self, parent=None):
    #     super(FileTreeView, self).__init__(parent)
    #     self.model = QFileSystemModel()
    #     self.model.setRootPath("")
    #     self.model.setReadOnly(False)
    #
    #     self.rootPath = ""
    #
    #     self.setModel(self.model)
    #     self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    #
    #     self.setHeaderHidden(True)
    #     self.setColumnHidden(1, True)
    #     self.setColumnHidden(2, True)
    #     self.setColumnHidden(3, True)
    #
    # def setRootPath(self, path: Path):
    #     self.rootPath = path.as_posix()
    #     self.model.setRootPath(self.rootPath)
    #     self.setRootIndex(self.model.index(self.rootPath))

    def mousePressEvent(self, event) -> None:
        self.clearSelection()
        QTreeView.mousePressEvent(self, event)
