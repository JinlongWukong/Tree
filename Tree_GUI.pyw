# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
import re

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(QtGui.QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1108, 805)

        self.retranslateUi(Dialog)
        self.setAcceptDrops(True)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # init widgets
        self.view = QtGui.QTreeView(Dialog)
        self.view.setGeometry(QtCore.QRect(20, 20, 1061, 771))
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Router configuration'])
        self.view.setModel(self.model)
        self.view.setUniformRowHeights(True)

    def loadConf(self,inputFile):
        # populate data
        f = open(inputFile)
        t = f.readlines()
        m = [item.strip("\n").strip("\r") for item in t]
        m = [item for item in m if not re.match("^ *! *$", item)]
        m = [item for item in m if not re.match("^ *end *$", item)]
        conf = [item for item in m if not re.match("^!+", item)]

        for item in conf:
            depth = len(item) - len(item.lstrip(' '))
            if depth == 0:
                first_branch = QStandardItem(str(item))
                hierachy = {depth: first_branch}
                self.model.appendRow(first_branch)
            else:
                new_branch = QStandardItem(str(item))
                hierachy[depth - 1].appendRow(new_branch)
                hierachy[depth] = new_branch
        #self.view.show()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))

    # The following three methods set up dragging and dropping for the app
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            #e.setDropAction(QtCore.Qt.CopyAction)
            e.accept()
            for url in e.mimeData().urls():
                fname = str(url.toLocalFile())
                print("Input file: " + fname)
                self.loadConf(fname)
        else:
            e.ignore()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())

