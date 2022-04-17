# Form implementation generated from reading ui file 'src/ui/mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(285, 215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelHelp = QtWidgets.QLabel(self.centralwidget)
        self.labelHelp.setEnabled(True)
        self.labelHelp.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelHelp.setObjectName("labelHelp")
        self.verticalLayout.addWidget(self.labelHelp, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxProfile = ProfileComboBox(self.centralwidget)
        self.comboBoxProfile.setObjectName("comboBoxProfile")
        self.horizontalLayout.addWidget(self.comboBoxProfile)
        self.pushButtonAddProfile = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAddProfile.sizePolicy().hasHeightForWidth())
        self.pushButtonAddProfile.setSizePolicy(sizePolicy)
        self.pushButtonAddProfile.setObjectName("pushButtonAddProfile")
        self.horizontalLayout.addWidget(self.pushButtonAddProfile)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeView = FileTreeView(self.centralwidget)
        self.treeView.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeView.setAcceptDrops(True)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked)
        self.treeView.setDragEnabled(True)
        self.treeView.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.treeView.setDefaultDropAction(QtCore.Qt.DropAction.MoveAction)
        self.treeView.setAlternatingRowColors(False)
        self.treeView.setUniformRowHeights(True)
        self.treeView.setAnimated(False)
        self.treeView.setHeaderHidden(True)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.labelHelp.raise_()
        self.treeView.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuGames = QtWidgets.QMenu(self.menuFile)
        self.menuGames.setObjectName("menuGames")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad = QtGui.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionReplace = QtGui.QAction(MainWindow)
        self.actionReplace.setObjectName("actionReplace")
        self.actionImport = QtGui.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionDS1_PTDE = QtGui.QAction(MainWindow)
        self.actionDS1_PTDE.setCheckable(True)
        self.actionDS1_PTDE.setObjectName("actionDS1_PTDE")
        self.actionDS1_Remastered = QtGui.QAction(MainWindow)
        self.actionDS1_Remastered.setCheckable(True)
        self.actionDS1_Remastered.setObjectName("actionDS1_Remastered")
        self.actionDS2_Vanilla = QtGui.QAction(MainWindow)
        self.actionDS2_Vanilla.setCheckable(True)
        self.actionDS2_Vanilla.setObjectName("actionDS2_Vanilla")
        self.actionDS2_SOTFS = QtGui.QAction(MainWindow)
        self.actionDS2_SOTFS.setCheckable(True)
        self.actionDS2_SOTFS.setObjectName("actionDS2_SOTFS")
        self.actionDS3 = QtGui.QAction(MainWindow)
        self.actionDS3.setCheckable(True)
        self.actionDS3.setObjectName("actionDS3")
        self.actionCopy = QtGui.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtGui.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionDelete = QtGui.QAction(MainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.actionRename = QtGui.QAction(MainWindow)
        self.actionRename.setObjectName("actionRename")
        self.actionNew_Folder = QtGui.QAction(MainWindow)
        self.actionNew_Folder.setObjectName("actionNew_Folder")
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.menuGames.addAction(self.actionDS1_PTDE)
        self.menuGames.addAction(self.actionDS1_Remastered)
        self.menuGames.addAction(self.actionDS2_Vanilla)
        self.menuGames.addAction(self.actionDS2_SOTFS)
        self.menuGames.addAction(self.actionDS3)
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionReplace)
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuGames.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionReplace)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addAction(self.actionRename)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionNew_Folder)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelHelp.setText(_translate("MainWindow", "TextLabel"))
        self.pushButtonAddProfile.setText(_translate("MainWindow", "Add"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuGames.setTitle(_translate("MainWindow", "Games"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionLoad.setShortcut(_translate("MainWindow", "F1"))
        self.actionReplace.setText(_translate("MainWindow", "Replace"))
        self.actionReplace.setShortcut(_translate("MainWindow", "F2"))
        self.actionImport.setText(_translate("MainWindow", "Import"))
        self.actionImport.setShortcut(_translate("MainWindow", "F3"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionDS1_PTDE.setText(_translate("MainWindow", "DS1: PTDE"))
        self.actionDS1_PTDE.setProperty("id", _translate("MainWindow", "0"))
        self.actionDS1_Remastered.setText(_translate("MainWindow", "DS1: Remastered"))
        self.actionDS1_Remastered.setProperty("id", _translate("MainWindow", "1"))
        self.actionDS2_Vanilla.setText(_translate("MainWindow", "DS2: Vanilla"))
        self.actionDS2_Vanilla.setProperty("id", _translate("MainWindow", "2"))
        self.actionDS2_SOTFS.setText(_translate("MainWindow", "DS2: SOTFS"))
        self.actionDS2_SOTFS.setProperty("id", _translate("MainWindow", "3"))
        self.actionDS3.setText(_translate("MainWindow", "DS3"))
        self.actionDS3.setProperty("id", _translate("MainWindow", "4"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionDelete.setShortcut(_translate("MainWindow", "Del"))
        self.actionRename.setText(_translate("MainWindow", "Rename"))
        self.actionRename.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionNew_Folder.setText(_translate("MainWindow", "New Folder"))
        self.actionNew_Folder.setShortcut(_translate("MainWindow", "Ctrl+Shift+N"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
from widgets.filetreeview import FileTreeView
from widgets.profilecombobox import ProfileComboBox
