"""

To implement:
    - Readme.md
    - Better settings window for no savefile location
    - Multi-file support
    - QAction update on no game
    - Other bugs?
    - Major refactor

"""

import sys
import ctypes

from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication

from windows.mainwindow import MainWindow

if __name__ == '__main__':
    app_id = 'hzsyahzin.yassam.0.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    QtCore.QDir.addSearchPath('icons', 'res/')

    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()
