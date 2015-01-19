# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mapcoloring.ui'
#
# Created: Mon Oct  1 09:59:22 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MapColoring(object):
    def setupUi(self, MapColoring):
        MapColoring.setObjectName(_fromUtf8("MapColoring"))
        MapColoring.resize(400, 310)
        self.verticalLayout = QtGui.QVBoxLayout(MapColoring)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(MapColoring)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.inputLayerCombo = QtGui.QComboBox(MapColoring)
        self.inputLayerCombo.setObjectName(_fromUtf8("inputLayerCombo"))
        self.verticalLayout.addWidget(self.inputLayerCombo)
        self.label_2 = QtGui.QLabel(MapColoring)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.outputLayerEdit = QtGui.QLineEdit(MapColoring)
        self.outputLayerEdit.setObjectName(_fromUtf8("outputLayerEdit"))
        self.horizontalLayout.addWidget(self.outputLayerEdit)
        self.saveAsButton = QtGui.QPushButton(MapColoring)
        self.saveAsButton.setObjectName(_fromUtf8("saveAsButton"))
        self.horizontalLayout.addWidget(self.saveAsButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_3 = QtGui.QLabel(MapColoring)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.colorField = QtGui.QLineEdit(MapColoring)
        self.colorField.setObjectName(_fromUtf8("colorField"))
        self.verticalLayout.addWidget(self.colorField)
        self.label_4 = QtGui.QLabel(MapColoring)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.algorithmeCombo = QtGui.QComboBox(MapColoring)
        self.algorithmeCombo.setObjectName(_fromUtf8("algorithmeCombo"))
        self.verticalLayout.addWidget(self.algorithmeCombo)
        self.keepFieldsCheckBox = QtGui.QCheckBox(MapColoring)
        self.keepFieldsCheckBox.setChecked(True)
        self.keepFieldsCheckBox.setObjectName(_fromUtf8("keepFieldsCheckBox"))
        self.verticalLayout.addWidget(self.keepFieldsCheckBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.stateLabel = QtGui.QLabel(MapColoring)
        self.stateLabel.setText(_fromUtf8(""))
        self.stateLabel.setObjectName(_fromUtf8("stateLabel"))
        self.verticalLayout.addWidget(self.stateLabel)
        self.progressBar = QtGui.QProgressBar(MapColoring)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.line = QtGui.QFrame(MapColoring)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.buttonBox = QtGui.QDialogButtonBox(MapColoring)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MapColoring)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MapColoring.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MapColoring.reject)
        QtCore.QMetaObject.connectSlotsByName(MapColoring)

    def retranslateUi(self, MapColoring):
        MapColoring.setWindowTitle(QtGui.QApplication.translate("MapColoring", "MapColoringPlugin", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MapColoring", "Input vector layer of polygons :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MapColoring", "Output layer file name :", None, QtGui.QApplication.UnicodeUTF8))
        self.saveAsButton.setText(QtGui.QApplication.translate("MapColoring", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MapColoring", "Row attribute to store color index :", None, QtGui.QApplication.UnicodeUTF8))
        self.colorField.setText(QtGui.QApplication.translate("MapColoring", "COLORID", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MapColoring", "Algorithm :", None, QtGui.QApplication.UnicodeUTF8))
        self.keepFieldsCheckBox.setText(QtGui.QApplication.translate("MapColoring", "Keep existing attributes", None, QtGui.QApplication.UnicodeUTF8))

