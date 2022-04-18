import keyboard
from PyQt6.QtCore import pyqtSignal, QObject


class HotkeyController(QObject):

    loadSignal = pyqtSignal()
    replaceSignal = pyqtSignal()
    importSignal = pyqtSignal()

    def register_hotkeys(self, loadKey, replaceKey, importKey):
        self.clear_hotkeys()
        keyboard.add_hotkey(loadKey, self.loadSignal.emit, suppress=True)
        keyboard.add_hotkey(replaceKey, self.replaceSignal.emit, suppress=True)
        keyboard.add_hotkey(importKey, self.importSignal.emit, suppress=True)

    def clear_hotkeys(self):
        keyboard.unhook_all()
