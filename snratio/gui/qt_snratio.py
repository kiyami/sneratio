# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'snratio/gui/qt_snratio.ui',
# licensing of 'snratio/gui/qt_snratio.ui' applies.
#
# Created: Wed Apr 29 16:47:46 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(941, 646)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_7.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setMaximumSize(QtCore.QSize(200, 16777215))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_9.setContentsMargins(5, -1, 5, -1)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_snIa = QtWidgets.QLabel(self.frame_3)
        self.label_snIa.setMinimumSize(QtCore.QSize(50, 20))
        self.label_snIa.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.label_snIa.setFont(font)
        self.label_snIa.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_snIa.setAlignment(QtCore.Qt.AlignCenter)
        self.label_snIa.setObjectName("label_snIa")
        self.gridLayout_8.addWidget(self.label_snIa, 0, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_snIa_table = QtWidgets.QLabel(self.frame_3)
        self.label_snIa_table.setMinimumSize(QtCore.QSize(65, 20))
        self.label_snIa_table.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_snIa_table.setFont(font)
        self.label_snIa_table.setObjectName("label_snIa_table")
        self.gridLayout_4.addWidget(self.label_snIa_table, 0, 0, 1, 1)
        self.box_snIa_table = QtWidgets.QComboBox(self.frame_3)
        self.box_snIa_table.setMinimumSize(QtCore.QSize(120, 20))
        self.box_snIa_table.setMaximumSize(QtCore.QSize(140, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.box_snIa_table.setFont(font)
        self.box_snIa_table.setObjectName("box_snIa_table")
        self.box_snIa_table.addItem("")
        self.gridLayout_4.addWidget(self.box_snIa_table, 0, 1, 1, 1)
        self.label_snIa_model = QtWidgets.QLabel(self.frame_3)
        self.label_snIa_model.setMinimumSize(QtCore.QSize(65, 20))
        self.label_snIa_model.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_snIa_model.setFont(font)
        self.label_snIa_model.setObjectName("label_snIa_model")
        self.gridLayout_4.addWidget(self.label_snIa_model, 1, 0, 1, 1)
        self.box_snIa_model = QtWidgets.QComboBox(self.frame_3)
        self.box_snIa_model.setMinimumSize(QtCore.QSize(120, 20))
        self.box_snIa_model.setMaximumSize(QtCore.QSize(140, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.box_snIa_model.setFont(font)
        self.box_snIa_model.setObjectName("box_snIa_model")
        self.box_snIa_model.addItem("")
        self.box_snIa_model.addItem("")
        self.box_snIa_model.addItem("")
        self.box_snIa_model.addItem("")
        self.box_snIa_model.addItem("")
        self.box_snIa_model.addItem("")
        self.box_snIa_model.addItem("")
        self.gridLayout_4.addWidget(self.box_snIa_model, 1, 1, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_4, 1, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_8, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_9.addItem(spacerItem, 9, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_9.addItem(spacerItem1, 7, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_load = QtWidgets.QLineEdit(self.frame_3)
        self.lineEdit_load.setMinimumSize(QtCore.QSize(130, 20))
        self.lineEdit_load.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_load.setFont(font)
        self.lineEdit_load.setObjectName("lineEdit_load")
        self.horizontalLayout.addWidget(self.lineEdit_load)
        self.button_load = QtWidgets.QPushButton(self.frame_3)
        self.button_load.setMinimumSize(QtCore.QSize(40, 25))
        self.button_load.setMaximumSize(QtCore.QSize(60, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(75)
        font.setBold(True)
        self.button_load.setFont(font)
        self.button_load.setObjectName("button_load")
        self.horizontalLayout.addWidget(self.button_load)
        self.gridLayout_9.addLayout(self.horizontalLayout, 8, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.frame_3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_9.addWidget(self.line, 6, 0, 1, 1)
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_fit = QtWidgets.QLabel(self.frame_3)
        self.label_fit.setMinimumSize(QtCore.QSize(50, 20))
        self.label_fit.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.label_fit.setFont(font)
        self.label_fit.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_fit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_fit.setScaledContents(False)
        self.label_fit.setAlignment(QtCore.Qt.AlignCenter)
        self.label_fit.setObjectName("label_fit")
        self.gridLayout_10.addWidget(self.label_fit, 0, 0, 1, 1)
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.box_ref = QtWidgets.QComboBox(self.frame_3)
        self.box_ref.setMinimumSize(QtCore.QSize(120, 20))
        self.box_ref.setMaximumSize(QtCore.QSize(140, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.box_ref.setFont(font)
        self.box_ref.setObjectName("box_ref")
        self.box_ref.addItem("")
        self.box_ref.addItem("")
        self.gridLayout_11.addWidget(self.box_ref, 0, 1, 1, 1)
        self.label_ref = QtWidgets.QLabel(self.frame_3)
        self.label_ref.setMinimumSize(QtCore.QSize(65, 20))
        self.label_ref.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_ref.setFont(font)
        self.label_ref.setObjectName("label_ref")
        self.gridLayout_11.addWidget(self.label_ref, 0, 0, 1, 1)
        self.label_sigma = QtWidgets.QLabel(self.frame_3)
        self.label_sigma.setMinimumSize(QtCore.QSize(65, 20))
        self.label_sigma.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_sigma.setFont(font)
        self.label_sigma.setObjectName("label_sigma")
        self.gridLayout_11.addWidget(self.label_sigma, 1, 0, 1, 1)
        self.box_sigma = QtWidgets.QComboBox(self.frame_3)
        self.box_sigma.setMinimumSize(QtCore.QSize(120, 20))
        self.box_sigma.setMaximumSize(QtCore.QSize(140, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.box_sigma.setFont(font)
        self.box_sigma.setObjectName("box_sigma")
        self.box_sigma.addItem("")
        self.box_sigma.addItem("")
        self.gridLayout_11.addWidget(self.box_sigma, 1, 1, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_11, 1, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_10, 5, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_sncc = QtWidgets.QLabel(self.frame_3)
        self.label_sncc.setMinimumSize(QtCore.QSize(50, 20))
        self.label_sncc.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.label_sncc.setFont(font)
        self.label_sncc.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_sncc.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_sncc.setScaledContents(False)
        self.label_sncc.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sncc.setObjectName("label_sncc")
        self.gridLayout_6.addWidget(self.label_sncc, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_sncc_table = QtWidgets.QLabel(self.frame_3)
        self.label_sncc_table.setMinimumSize(QtCore.QSize(65, 20))
        self.label_sncc_table.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_sncc_table.setFont(font)
        self.label_sncc_table.setObjectName("label_sncc_table")
        self.gridLayout_3.addWidget(self.label_sncc_table, 0, 0, 1, 1)
        self.box_sncc_table = QtWidgets.QComboBox(self.frame_3)
        self.box_sncc_table.setMinimumSize(QtCore.QSize(120, 20))
        self.box_sncc_table.setMaximumSize(QtCore.QSize(140, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.box_sncc_table.setFont(font)
        self.box_sncc_table.setObjectName("box_sncc_table")
        self.box_sncc_table.addItem("")
        self.box_sncc_table.addItem("")
        self.box_sncc_table.addItem("")
        self.gridLayout_3.addWidget(self.box_sncc_table, 0, 1, 1, 1)
        self.label_sncc_abund = QtWidgets.QLabel(self.frame_3)
        self.label_sncc_abund.setMinimumSize(QtCore.QSize(65, 20))
        self.label_sncc_abund.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_sncc_abund.setFont(font)
        self.label_sncc_abund.setObjectName("label_sncc_abund")
        self.gridLayout_3.addWidget(self.label_sncc_abund, 1, 0, 1, 1)
        self.box_sncc_abund = QtWidgets.QComboBox(self.frame_3)
        self.box_sncc_abund.setMinimumSize(QtCore.QSize(120, 20))
        self.box_sncc_abund.setMaximumSize(QtCore.QSize(140, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.box_sncc_abund.setFont(font)
        self.box_sncc_abund.setObjectName("box_sncc_abund")
        self.box_sncc_abund.addItem("")
        self.box_sncc_abund.addItem("")
        self.box_sncc_abund.addItem("")
        self.box_sncc_abund.addItem("")
        self.box_sncc_abund.addItem("")
        self.box_sncc_abund.addItem("")
        self.gridLayout_3.addWidget(self.box_sncc_abund, 1, 1, 1, 1)
        self.label_sncc_mass = QtWidgets.QLabel(self.frame_3)
        self.label_sncc_mass.setMinimumSize(QtCore.QSize(65, 20))
        self.label_sncc_mass.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_sncc_mass.setFont(font)
        self.label_sncc_mass.setObjectName("label_sncc_mass")
        self.gridLayout_3.addWidget(self.label_sncc_mass, 2, 0, 1, 1)
        self.box_sncc_mass = QtWidgets.QComboBox(self.frame_3)
        self.box_sncc_mass.setMinimumSize(QtCore.QSize(120, 20))
        self.box_sncc_mass.setMaximumSize(QtCore.QSize(140, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.box_sncc_mass.setFont(font)
        self.box_sncc_mass.setObjectName("box_sncc_mass")
        self.box_sncc_mass.addItem("")
        self.box_sncc_mass.addItem("")
        self.gridLayout_3.addWidget(self.box_sncc_mass, 2, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_6, 3, 0, 1, 1)
        self.label_parameter_selection = QtWidgets.QLabel(self.frame_3)
        self.label_parameter_selection.setMinimumSize(QtCore.QSize(0, 30))
        self.label_parameter_selection.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setWeight(75)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setBold(True)
        self.label_parameter_selection.setFont(font)
        self.label_parameter_selection.setFrameShape(QtWidgets.QFrame.Box)
        self.label_parameter_selection.setAlignment(QtCore.Qt.AlignCenter)
        self.label_parameter_selection.setObjectName("label_parameter_selection")
        self.gridLayout_9.addWidget(self.label_parameter_selection, 0, 0, 1, 1)
        self.gridLayout_13 = QtWidgets.QGridLayout()
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.label_solar = QtWidgets.QLabel(self.frame_3)
        self.label_solar.setMinimumSize(QtCore.QSize(50, 20))
        self.label_solar.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.label_solar.setFont(font)
        self.label_solar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_solar.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_solar.setScaledContents(False)
        self.label_solar.setAlignment(QtCore.Qt.AlignCenter)
        self.label_solar.setObjectName("label_solar")
        self.gridLayout_13.addWidget(self.label_solar, 0, 0, 1, 1)
        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.label_solar_table = QtWidgets.QLabel(self.frame_3)
        self.label_solar_table.setMinimumSize(QtCore.QSize(65, 20))
        self.label_solar_table.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_solar_table.setFont(font)
        self.label_solar_table.setObjectName("label_solar_table")
        self.gridLayout_14.addWidget(self.label_solar_table, 0, 0, 1, 1)
        self.box_solar_table = QtWidgets.QComboBox(self.frame_3)
        self.box_solar_table.setMinimumSize(QtCore.QSize(120, 20))
        self.box_solar_table.setMaximumSize(QtCore.QSize(140, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.box_solar_table.setFont(font)
        self.box_solar_table.setObjectName("box_solar_table")
        self.box_solar_table.addItem("")
        self.box_solar_table.addItem("")
        self.box_solar_table.addItem("")
        self.gridLayout_14.addWidget(self.box_solar_table, 0, 1, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_14, 1, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_13, 4, 0, 1, 1)
        self.gridLayout_7.addWidget(self.frame_3, 0, 0, 2, 1)
        self.frame_5 = QtWidgets.QFrame(self.frame)
        self.frame_5.setMinimumSize(QtCore.QSize(400, 300))
        self.frame_5.setMaximumSize(QtCore.QSize(800, 600))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.widget_plot_area = QtWidgets.QWidget(self.frame_5)
        self.widget_plot_area.setObjectName("widget_plot_area")
        self.gridLayout_12.addWidget(self.widget_plot_area, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.frame_5, 0, 1, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setMinimumSize(QtCore.QSize(400, 80))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 80))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_5.setSpacing(5)
        self.gridLayout_5.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.plainTextEdit_terminal = QtWidgets.QPlainTextEdit(self.frame_4)
        self.plainTextEdit_terminal.setObjectName("plainTextEdit_terminal")
        self.gridLayout_5.addWidget(self.plainTextEdit_terminal, 1, 0, 1, 1)
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setMinimumSize(QtCore.QSize(0, 25))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_C = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox_C.setObjectName("checkBox_C")
        self.horizontalLayout_2.addWidget(self.checkBox_C)
        self.checkBox_N = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox_N.setObjectName("checkBox_N")
        self.horizontalLayout_2.addWidget(self.checkBox_N)
        self.checkBox_O = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox_O.setObjectName("checkBox_O")
        self.horizontalLayout_2.addWidget(self.checkBox_O)
        self.checkBox_Ne = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox_Ne.setObjectName("checkBox_Ne")
        self.horizontalLayout_2.addWidget(self.checkBox_Ne)
        self.checkBox_Mg = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox_Mg.setObjectName("checkBox_Mg")
        self.horizontalLayout_2.addWidget(self.checkBox_Mg)
        self.checkBox_Al = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox_Al.setObjectName("checkBox_Al")
        self.horizontalLayout_2.addWidget(self.checkBox_Al)
        self.checkBox_Si = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox_Si.setObjectName("checkBox_Si")
        self.horizontalLayout_2.addWidget(self.checkBox_Si)
        self.checkBox_S = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox_S.setObjectName("checkBox_S")
        self.horizontalLayout_2.addWidget(self.checkBox_S)
        self.checkBox_Ar = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox_Ar.setObjectName("checkBox_Ar")
        self.horizontalLayout_2.addWidget(self.checkBox_Ar)
        self.checkBox_Ca = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox_Ca.setObjectName("checkBox_Ca")
        self.horizontalLayout_2.addWidget(self.checkBox_Ca)
        self.checkBox_Fe = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox_Fe.setObjectName("checkBox_Fe")
        self.horizontalLayout_2.addWidget(self.checkBox_Fe)
        self.checkBox_Ni = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox_Ni.setObjectName("checkBox_Ni")
        self.horizontalLayout_2.addWidget(self.checkBox_Ni)
        self.gridLayout_5.addWidget(self.frame_6, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.frame_4, 1, 1, 1, 2)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(140, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(140, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.line_4 = QtWidgets.QFrame(self.frame_2)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 7, 0, 1, 1)
        self.button_save_plots = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setBold(False)
        self.button_save_plots.setFont(font)
        self.button_save_plots.setObjectName("button_save_plots")
        self.gridLayout.addWidget(self.button_save_plots, 18, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 17, 0, 1, 1)
        self.button_fit = QtWidgets.QPushButton(self.frame_2)
        self.button_fit.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setWeight(75)
        font.setBold(True)
        self.button_fit.setFont(font)
        self.button_fit.setObjectName("button_fit")
        self.gridLayout.addWidget(self.button_fit, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 25, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.frame_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 16, 0, 1, 1)
        self.button_plot_fit = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setBold(False)
        self.button_plot_fit.setFont(font)
        self.button_plot_fit.setObjectName("button_plot_fit")
        self.gridLayout.addWidget(self.button_plot_fit, 11, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 15, 0, 1, 1)
        self.button_save_stats = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setBold(False)
        self.button_save_stats.setFont(font)
        self.button_save_stats.setObjectName("button_save_stats")
        self.gridLayout.addWidget(self.button_save_stats, 19, 0, 1, 1)
        self.plainTextEdit_fit_results = QtWidgets.QPlainTextEdit(self.frame_2)
        self.plainTextEdit_fit_results.setMinimumSize(QtCore.QSize(125, 140))
        self.plainTextEdit_fit_results.setObjectName("plainTextEdit_fit_results")
        self.gridLayout.addWidget(self.plainTextEdit_fit_results, 8, 0, 1, 1)
        self.button_save_all = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setBold(False)
        self.button_save_all.setFont(font)
        self.button_save_all.setObjectName("button_save_all")
        self.gridLayout.addWidget(self.button_save_all, 20, 0, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.frame_2)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout.addWidget(self.line_5, 9, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.frame_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 4, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 10, 0, 1, 1)
        self.button_plot_likelihood = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setBold(False)
        self.button_plot_likelihood.setFont(font)
        self.button_plot_likelihood.setObjectName("button_plot_likelihood")
        self.gridLayout.addWidget(self.button_plot_likelihood, 13, 0, 1, 1)
        self.button_plot_chi = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setBold(False)
        self.button_plot_chi.setFont(font)
        self.button_plot_chi.setObjectName("button_plot_chi")
        self.gridLayout.addWidget(self.button_plot_chi, 14, 0, 1, 1)
        self.gridLayout_7.addWidget(self.frame_2, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 941, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionPackage = QtWidgets.QAction(MainWindow)
        self.actionPackage.setObjectName("actionPackage")
        self.actionAuthors = QtWidgets.QAction(MainWindow)
        self.actionAuthors.setObjectName("actionAuthors")
        self.actionAuthors_2 = QtWidgets.QAction(MainWindow)
        self.actionAuthors_2.setObjectName("actionAuthors_2")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionPackage)
        self.menuHelp.addAction(self.actionAuthors)
        self.menuHelp.addAction(self.actionAuthors_2)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.box_sncc_abund.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label_snIa.setText(QtWidgets.QApplication.translate("MainWindow", "SN Ia", None, -1))
        self.label_snIa_table.setText(QtWidgets.QApplication.translate("MainWindow", "Table:", None, -1))
        self.box_snIa_table.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "Iwamoto (1999)", None, -1))
        self.label_snIa_model.setText(QtWidgets.QApplication.translate("MainWindow", "Model:", None, -1))
        self.box_snIa_model.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "W7", None, -1))
        self.box_snIa_model.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "W70", None, -1))
        self.box_snIa_model.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "WDD1", None, -1))
        self.box_snIa_model.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "WDD2", None, -1))
        self.box_snIa_model.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "WDD3", None, -1))
        self.box_snIa_model.setItemText(5, QtWidgets.QApplication.translate("MainWindow", "CDD1", None, -1))
        self.box_snIa_model.setItemText(6, QtWidgets.QApplication.translate("MainWindow", "CDD2", None, -1))
        self.button_load.setText(QtWidgets.QApplication.translate("MainWindow", "Load", None, -1))
        self.label_fit.setText(QtWidgets.QApplication.translate("MainWindow", "Fit Parameters", None, -1))
        self.box_ref.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "Fe", None, -1))
        self.box_ref.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "H", None, -1))
        self.label_ref.setText(QtWidgets.QApplication.translate("MainWindow", "Ref. Element", None, -1))
        self.label_sigma.setText(QtWidgets.QApplication.translate("MainWindow", "Sigma:", None, -1))
        self.box_sigma.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "1.0", None, -1))
        self.box_sigma.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "2.0", None, -1))
        self.label_sncc.setText(QtWidgets.QApplication.translate("MainWindow", "SN cc", None, -1))
        self.label_sncc_table.setText(QtWidgets.QApplication.translate("MainWindow", "Table:", None, -1))
        self.box_sncc_table.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "Nomoto (2013)", None, -1))
        self.box_sncc_table.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "Nomoto (2006)", None, -1))
        self.box_sncc_table.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "Tsujimoto (1995)", None, -1))
        self.label_sncc_abund.setText(QtWidgets.QApplication.translate("MainWindow", "Abundance:", None, -1))
        self.box_sncc_abund.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "0.0", None, -1))
        self.box_sncc_abund.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "0.001", None, -1))
        self.box_sncc_abund.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "0.004", None, -1))
        self.box_sncc_abund.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "0.008", None, -1))
        self.box_sncc_abund.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "0.02", None, -1))
        self.box_sncc_abund.setItemText(5, QtWidgets.QApplication.translate("MainWindow", "0.05", None, -1))
        self.label_sncc_mass.setText(QtWidgets.QApplication.translate("MainWindow", "Mass Range:", None, -1))
        self.box_sncc_mass.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "10-50 M sun", None, -1))
        self.box_sncc_mass.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "10-70 M sun", None, -1))
        self.label_parameter_selection.setText(QtWidgets.QApplication.translate("MainWindow", "Parameter Selection", None, -1))
        self.label_solar.setText(QtWidgets.QApplication.translate("MainWindow", "Solar Values", None, -1))
        self.label_solar_table.setText(QtWidgets.QApplication.translate("MainWindow", "Table", None, -1))
        self.box_solar_table.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "Lodd", None, -1))
        self.box_solar_table.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "Angr", None, -1))
        self.box_solar_table.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "Aspl", None, -1))
        self.checkBox_C.setText(QtWidgets.QApplication.translate("MainWindow", "C", None, -1))
        self.checkBox_N.setText(QtWidgets.QApplication.translate("MainWindow", "N", None, -1))
        self.checkBox_O.setText(QtWidgets.QApplication.translate("MainWindow", "O", None, -1))
        self.checkBox_Ne.setText(QtWidgets.QApplication.translate("MainWindow", "Ne", None, -1))
        self.checkBox_Mg.setText(QtWidgets.QApplication.translate("MainWindow", "Mg", None, -1))
        self.checkBox_Al.setText(QtWidgets.QApplication.translate("MainWindow", "Al", None, -1))
        self.checkBox_Si.setText(QtWidgets.QApplication.translate("MainWindow", "Si", None, -1))
        self.checkBox_S.setText(QtWidgets.QApplication.translate("MainWindow", "S", None, -1))
        self.checkBox_Ar.setText(QtWidgets.QApplication.translate("MainWindow", "Ar", None, -1))
        self.checkBox_Ca.setText(QtWidgets.QApplication.translate("MainWindow", "Ca", None, -1))
        self.checkBox_Fe.setText(QtWidgets.QApplication.translate("MainWindow", "Fe", None, -1))
        self.checkBox_Ni.setText(QtWidgets.QApplication.translate("MainWindow", "Ni", None, -1))
        self.button_save_plots.setText(QtWidgets.QApplication.translate("MainWindow", "Save: Plots", None, -1))
        self.button_fit.setText(QtWidgets.QApplication.translate("MainWindow", "Fit", None, -1))
        self.button_plot_fit.setText(QtWidgets.QApplication.translate("MainWindow", "Plot: Fit", None, -1))
        self.button_save_stats.setText(QtWidgets.QApplication.translate("MainWindow", "Save: Stats", None, -1))
        self.button_save_all.setText(QtWidgets.QApplication.translate("MainWindow", "Save: All", None, -1))
        self.button_plot_likelihood.setText(QtWidgets.QApplication.translate("MainWindow", "Plot: Likelihood", None, -1))
        self.button_plot_chi.setText(QtWidgets.QApplication.translate("MainWindow", "Plot: Chi-squared", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("MainWindow", "About", None, -1))
        self.actionNew.setText(QtWidgets.QApplication.translate("MainWindow", "New", None, -1))
        self.actionOpen.setText(QtWidgets.QApplication.translate("MainWindow", "Open", None, -1))
        self.actionExit.setText(QtWidgets.QApplication.translate("MainWindow", "Exit", None, -1))
        self.actionPackage.setText(QtWidgets.QApplication.translate("MainWindow", "Package", None, -1))
        self.actionAuthors.setText(QtWidgets.QApplication.translate("MainWindow", "Methods", None, -1))
        self.actionAuthors_2.setText(QtWidgets.QApplication.translate("MainWindow", "Authors", None, -1))

