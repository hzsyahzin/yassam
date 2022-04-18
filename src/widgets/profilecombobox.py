from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QComboBox


class ProfileComboBox(QComboBox):

    noProfileFound = pyqtSignal()

    def __init__(self, parent=None):
        super(ProfileComboBox, self).__init__(parent)

    def populate(self, path: Path) -> bool:
        self.clear()
        try:
            for path in path.iterdir():
                if path.is_dir():
                    self.addItem(path.name)
            if self.count():
                return True
        except AttributeError:
            print("Error: Loading savefile")
        return False
