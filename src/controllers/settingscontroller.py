import json
from pathlib import Path
from typing import List


class SettingsController:
    def __init__(self):
        with open("./settings.json") as settingsFile:
            self.settings = json.load(settingsFile)

    def isSavefileValid(self, gameID: int) -> bool:
        if self.getSavefilePath(gameID):
            return True
        return False

    def getGameList(self) -> List[str]:
        return self.settings["games"].values()

    def getGameIDFromName(self, gameName: str) -> int:
        return {v: gameID for gameID, v in self.settings["games"].items()}[gameName]

    def getActiveGameID(self) -> int:
        return int(self.settings["current_game"])

    def getActiveGameName(self) -> str:
        return self.settings["games"][self.settings["current_game"]]

    def getSavefilePath(self, gameID: int) -> Path | None:
        try:
            return Path(self.settings["savefiles"][str(gameID)])
        except (TypeError, AttributeError):
            return None

    def getSavefileDirectory(self, gameID: int) -> Path | None:
        try:
            return self.getSavefilePath(gameID).parent
        except (TypeError, AttributeError):
            return None

    def getActiveSavefileDirectory(self) -> Path | None:
        try:
            return self.getActiveSavefilePath().parent
        except (TypeError, AttributeError):
            return None

    def getActiveSavefileName(self) -> str | None:
        try:
            return self.getActiveSavefilePath().name
        except (TypeError, AttributeError):
            return None

    def getActiveSavefilePath(self) -> Path | None:
        try:
            return self.getSavefilePath(self.getActiveGameID())
        except (TypeError, AttributeError):
            return None

    def setSavefilePath(self, gameID: int, path: Path) -> None:
        self.settings["savefiles"][str(gameID)] = str(path)

    def setActiveGame(self, gameID: int) -> None:
        self.settings["current_game"] = str(gameID)
        self.saveSettings()

    def saveSettings(self) -> None:
        with open("./settings.json", "w") as settingsFile:
            settingsFile.write(json.dumps(self.settings))
