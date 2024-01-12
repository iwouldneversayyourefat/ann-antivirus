from PyQt5.QtWidgets import QAbstractItemView
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object) :

    def setupUi(self, Dialog) :
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(662, 664)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(337, 316))
        Dialog.setMaximumSize(QtCore.QSize(100000, 100000))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        Dialog.setFont(font)
        self.select_file = QtWidgets.QPushButton(Dialog)
        self.select_file.setGeometry(QtCore.QRect(10, 10, 161, 61))
        self.select_file.setObjectName("select_file")
        self.select_folder = QtWidgets.QPushButton(Dialog)
        self.select_folder.setGeometry(QtCore.QRect(250, 10, 161, 61))
        self.select_folder.setObjectName("select_folder")
        self.delete_selected = QtWidgets.QPushButton(Dialog)
        self.delete_selected.setGeometry(QtCore.QRect(490, 10, 161, 61))
        self.delete_selected.setObjectName("delete_selected")
        self.resultlist = QtWidgets.QListWidget(Dialog)
        self.resultlist.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.resultlist.setGeometry(QtCore.QRect(10, 90, 641, 561))
        self.resultlist.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.resultlist.setObjectName("resultlist")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog) :
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "风险文件检测系统"))
        self.select_file.setText(_translate("Dialog", "选取文件"))
        self.select_folder.setText(_translate("Dialog", "选取文件夹"))
        self.delete_selected.setText(_translate("Dialog", "删除选中文件"))

