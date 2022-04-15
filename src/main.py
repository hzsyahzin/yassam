"""

To implement:
    - Settings
    - Persist cbx index
    - Profile deletion
    - Readme

"""

import sys
import ctypes

from PyQt6.QtWidgets import QApplication

from mainwindow import MainWindow

if __name__ == '__main__':
    app_id = 'hzsyahzin.yassam.0.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()
