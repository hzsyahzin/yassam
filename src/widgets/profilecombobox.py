from pathlib import Path

from PyQt6.QtWidgets import QComboBox


class ProfileComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ProfileComboBox, self).__init__(parent)

    def populate(self, path: Path):
        self.clear()
        try:
            for path in path.iterdir():
                if path.is_dir():
                    self.addItem(path.name)
        except AttributeError:
            print("Error: Loading savefile")
