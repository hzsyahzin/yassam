from typing import List

from PyQt6.QtWidgets import QComboBox


class GameComboBox(QComboBox):

    def __init__(self, parent=None):
        super(GameComboBox, self).__init__(parent)

    def populate(self, gamesList: List):
        for game in gamesList:
            self.addItem(game)

    def getSelectedGameID(self) -> int:
        return self.currentIndex()
