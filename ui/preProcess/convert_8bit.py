# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'convert_8bit.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_convert8bit(object):
    def setupUi(self, Dialog_convert8bit):
        Dialog_convert8bit.setObjectName("Dialog_convert8bit")
        Dialog_convert8bit.resize(512, 277)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_convert8bit)
        self.buttonBox.setGeometry(QtCore.QRect(300, 230, 156, 23))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(Dialog_convert8bit)
        self.widget.setGeometry(QtCore.QRect(29, 10, 461, 181))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_imagpath = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_imagpath.setObjectName("lineEdit_imagpath")
        self.horizontalLayout.addWidget(self.lineEdit_imagpath)
        self.pushButton_imagepath = QtWidgets.QPushButton(self.widget)
        self.pushButton_imagepath.setObjectName("pushButton_imagepath")
        self.horizontalLayout.addWidget(self.pushButton_imagepath)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_outputpath = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_outputpath.setObjectName("lineEdit_outputpath")
        self.horizontalLayout_2.addWidget(self.lineEdit_outputpath)
        self.pushButton_outputpath = QtWidgets.QPushButton(self.widget)
        self.pushButton_outputpath.setObjectName("pushButton_outputpath")
        self.horizontalLayout_2.addWidget(self.pushButton_outputpath)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.comboBox_scale = QtWidgets.QComboBox(self.widget)
        self.comboBox_scale.setMinimumSize(QtCore.QSize(0, 22))
        self.comboBox_scale.setObjectName("comboBox_scale")
        self.comboBox_scale.addItem("")
        self.comboBox_scale.addItem("")
        self.comboBox_scale.addItem("")
        self.comboBox_scale.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_scale)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.spinBox = QtWidgets.QSpinBox(self.widget)
        self.spinBox.setMinimumSize(QtCore.QSize(0, 22))
        self.spinBox.setMaximum(1000000000)
        self.spinBox.setProperty("value", 65535)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_4.addWidget(self.spinBox)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Dialog_convert8bit)
        self.buttonBox.accepted.connect(Dialog_convert8bit.slot_ok)
        self.buttonBox.rejected.connect(Dialog_convert8bit.reject)
        self.pushButton_imagepath.clicked.connect(Dialog_convert8bit.slot_select_samplepath)
        self.pushButton_outputpath.clicked.connect(Dialog_convert8bit.slot_select_outputpath)
        QtCore.QMetaObject.connectSlotsByName(Dialog_convert8bit)

    def retranslateUi(self, Dialog_convert8bit):
        _translate = QtCore.QCoreApplication.translate
        Dialog_convert8bit.setWindowTitle(_translate("Dialog_convert8bit", "图像转8bit"))
        self.label.setText(_translate("Dialog_convert8bit", "imagepath"))
        self.pushButton_imagepath.setText(_translate("Dialog_convert8bit", "open"))
        self.label_2.setText(_translate("Dialog_convert8bit", "outputpath"))
        self.pushButton_outputpath.setText(_translate("Dialog_convert8bit", "open"))
        self.label_3.setText(_translate("Dialog_convert8bit", "Strench type"))
        self.comboBox_scale.setCurrentText(_translate("Dialog_convert8bit", "Percent clip"))
        self.comboBox_scale.setItemText(0, _translate("Dialog_convert8bit", "Percent clip"))
        self.comboBox_scale.setItemText(1, _translate("Dialog_convert8bit", "Min Maxinum"))
        self.comboBox_scale.setItemText(2, _translate("Dialog_convert8bit", "Hist specification"))
        self.comboBox_scale.setItemText(3, _translate("Dialog_convert8bit", "Stand deviation"))
        self.label_4.setText(_translate("Dialog_convert8bit", "Nodata"))

