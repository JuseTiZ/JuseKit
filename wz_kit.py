# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wz.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class wzkit(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(360, 156)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.file_dir = QtWidgets.QToolButton(Dialog)
        self.file_dir.setObjectName("file_dir")
        self.horizontalLayout.addWidget(self.file_dir)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.now_wz = QtWidgets.QTextEdit(Dialog)
        self.now_wz.setMaximumSize(QtCore.QSize(16777215, 30))
        self.now_wz.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.now_wz.setObjectName("now_wz")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.now_wz)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.to_wz = QtWidgets.QTextEdit(Dialog)
        self.to_wz.setMaximumSize(QtCore.QSize(16777215, 30))
        self.to_wz.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.to_wz.setObjectName("to_wz")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.to_wz)
        self.verticalLayout.addLayout(self.formLayout)
        self.running = QtWidgets.QPushButton(Dialog)
        self.running.setObjectName("running")
        self.verticalLayout.addWidget(self.running)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Juse帮您批量替换尾缀"))
        self.file_dir.setText(_translate("Dialog", "..."))
        self.label.setText(_translate("Dialog", "未选择文件夹"))
        self.label_2.setText(_translate("Dialog", "现尾缀："))
        self.label_3.setText(_translate("Dialog", "目标尾缀："))
        self.running.setText(_translate("Dialog", "Start!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
