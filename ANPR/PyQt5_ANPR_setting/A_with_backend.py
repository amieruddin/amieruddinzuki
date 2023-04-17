# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ANPR_setting.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys

import chime
import os
import configparser


class Ui_MainWindow(object):
        def setupUi(self, MainWindow):  
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(667, 733)
                font = QtGui.QFont()
                font.setBold(False)
                font.setWeight(50)
                font.setStrikeOut(False)
                font.setKerning(True)
                MainWindow.setFont(font)
                MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
                self.tabWidget.setGeometry(QtCore.QRect(10, 70, 641, 591))
                font = QtGui.QFont()
                font.setPointSize(12)
                self.tabWidget.setFont(font)
                self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                self.tabWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
                self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
                self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
                self.tabWidget.setIconSize(QtCore.QSize(35, 35))
                self.tabWidget.setElideMode(QtCore.Qt.ElideMiddle)
                self.tabWidget.setMovable(False)
                self.tabWidget.setObjectName("tabWidget")
                self.tab = QtWidgets.QWidget()
                self.tab.setObjectName("tab")
                self.groupBox_controller_config = QtWidgets.QGroupBox(self.tab)
                self.groupBox_controller_config.setGeometry(QtCore.QRect(20, 30, 591, 211))
                self.groupBox_controller_config.setObjectName("groupBox_controller_config")
                self.label_host_port1 = QtWidgets.QLabel(self.groupBox_controller_config)
                self.label_host_port1.setGeometry(QtCore.QRect(50, 90, 91, 17))
                self.label_host_port1.setObjectName("label_host_port1")
                self.comboBox_controllerIP = QtWidgets.QComboBox(self.groupBox_controller_config)
                self.comboBox_controllerIP.setEnabled(True)
                self.comboBox_controllerIP.setGeometry(QtCore.QRect(200, 50, 311, 21))
                self.comboBox_controllerIP.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.comboBox_controllerIP.setMouseTracking(True)
                self.comboBox_controllerIP.setWhatsThis("")
                self.comboBox_controllerIP.setAutoFillBackground(False)
                self.comboBox_controllerIP.setEditable(False)
                self.comboBox_controllerIP.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
                self.comboBox_controllerIP.setMinimumContentsLength(5)
                self.comboBox_controllerIP.setObjectName("comboBox_controllerIP")
                self.comboBox_controllerIP.addItem("")
                self.comboBox_controllerIP.addItem("")
                self.comboBox_controllerIP.addItem("")
                self.comboBox_controllerIP.addItem("")
                self.comboBox_controllerIP.addItem("")
                self.comboBox_controllerIP.addItem("")
                self.comboBox_controllerIP.addItem("")
                self.comboBox_controllerIP.addItem("")
                self.comboBox_controllerIP.addItem("")
                self.comboBox_controllerIP.addItem("")
                self.comboBox_controllerIP.addItem("")
                self.comboBox_controllerIP.addItem("")
                self.comboBox_controllerIP.addItem("")
                self.comboBox_controllerIP.addItem("")
                self.label_controller_IP = QtWidgets.QLabel(self.groupBox_controller_config)
                self.label_controller_IP.setGeometry(QtCore.QRect(50, 50, 101, 17))
                self.label_controller_IP.setObjectName("label_controller_IP")
                self.comboBox_host_port1 = QtWidgets.QComboBox(self.groupBox_controller_config)
                self.comboBox_host_port1.setEnabled(True)
                self.comboBox_host_port1.setGeometry(QtCore.QRect(200, 90, 311, 21))
                self.comboBox_host_port1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.comboBox_host_port1.setMouseTracking(True)
                self.comboBox_host_port1.setWhatsThis("")
                self.comboBox_host_port1.setAutoFillBackground(False)
                self.comboBox_host_port1.setEditable(False)
                self.comboBox_host_port1.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
                self.comboBox_host_port1.setMinimumContentsLength(5)
                self.comboBox_host_port1.setObjectName("comboBox_host_port1")
                self.comboBox_host_port1.addItem("")
                self.comboBox_host_port1.addItem("")
                self.comboBox_host_port1.addItem("")
                self.comboBox_host_port1.addItem("")
                self.comboBox_host_port1.addItem("")
                self.comboBox_host_port1.addItem("")
                self.comboBox_host_port1.addItem("")
                self.comboBox_host_port1.addItem("")
                self.comboBox_host_port1.addItem("")
                self.comboBox_host_port1.addItem("")
                self.label_host_port2 = QtWidgets.QLabel(self.groupBox_controller_config)
                self.label_host_port2.setEnabled(True)
                self.label_host_port2.setGeometry(QtCore.QRect(50, 160, 91, 17))
                self.label_host_port2.setObjectName("label_host_port2")
                self.comboBox_host_port2 = QtWidgets.QComboBox(self.groupBox_controller_config)
                self.comboBox_host_port2.setEnabled(True)
                self.comboBox_host_port2.setGeometry(QtCore.QRect(200, 160, 311, 21))
                self.comboBox_host_port2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.comboBox_host_port2.setMouseTracking(True)
                self.comboBox_host_port2.setWhatsThis("")
                self.comboBox_host_port2.setAutoFillBackground(False)
                self.comboBox_host_port2.setEditable(False)
                self.comboBox_host_port2.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
                self.comboBox_host_port2.setMinimumContentsLength(5)
                self.comboBox_host_port2.setObjectName("comboBox_host_port2")
                self.comboBox_host_port2.addItem("")
                self.comboBox_host_port2.addItem("")
                self.comboBox_host_port2.addItem("")
                self.comboBox_host_port2.addItem("")
                self.comboBox_host_port2.addItem("")
                self.comboBox_host_port2.addItem("")
                self.comboBox_host_port2.addItem("")
                self.comboBox_host_port2.addItem("")
                self.comboBox_host_port2.addItem("")
                self.comboBox_host_port2.addItem("")
                self.checkBox_host_port2 = QtWidgets.QCheckBox(self.groupBox_controller_config)
                self.checkBox_host_port2.setGeometry(QtCore.QRect(200, 130, 111, 23))
                font = QtGui.QFont()
                font.setPointSize(11)
                self.checkBox_host_port2.setFont(font)
                self.checkBox_host_port2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.checkBox_host_port2.setObjectName("checkBox_host_port2")
                self.groupBox_anpr_config = QtWidgets.QGroupBox(self.tab)
                self.groupBox_anpr_config.setGeometry(QtCore.QRect(20, 270, 591, 241))
                self.groupBox_anpr_config.setObjectName("groupBox_anpr_config")
                self.label_plaza_id = QtWidgets.QLabel(self.groupBox_anpr_config)
                self.label_plaza_id.setGeometry(QtCore.QRect(50, 200, 67, 17))
                self.label_plaza_id.setObjectName("label_plaza_id")
                self.comboBox_plaza_id = QtWidgets.QComboBox(self.groupBox_anpr_config)
                self.comboBox_plaza_id.setEnabled(True)
                self.comboBox_plaza_id.setGeometry(QtCore.QRect(200, 200, 311, 21))
                self.comboBox_plaza_id.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.comboBox_plaza_id.setMouseTracking(True)
                self.comboBox_plaza_id.setWhatsThis("")
                self.comboBox_plaza_id.setAutoFillBackground(False)
                self.comboBox_plaza_id.setEditable(False)
                self.comboBox_plaza_id.setMaxVisibleItems(10)
                self.comboBox_plaza_id.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
                self.comboBox_plaza_id.setMinimumContentsLength(5)
                self.comboBox_plaza_id.setFrame(True)
                self.comboBox_plaza_id.setObjectName("comboBox_plaza_id")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_plaza_id.addItem("")
                self.comboBox_video = QtWidgets.QComboBox(self.groupBox_anpr_config)
                self.comboBox_video.setEnabled(True)
                self.comboBox_video.setGeometry(QtCore.QRect(200, 40, 311, 21))
                self.comboBox_video.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.comboBox_video.setMouseTracking(True)
                self.comboBox_video.setWhatsThis("")
                self.comboBox_video.setAutoFillBackground(False)
                self.comboBox_video.setEditable(False)
                self.comboBox_video.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
                self.comboBox_video.setMinimumContentsLength(5)
                self.comboBox_video.setObjectName("comboBox_video")
                self.comboBox_video.addItem("")
                self.comboBox_video.addItem("")
                self.comboBox_toll = QtWidgets.QComboBox(self.groupBox_anpr_config)
                self.comboBox_toll.setEnabled(True)
                self.comboBox_toll.setGeometry(QtCore.QRect(200, 80, 311, 21))
                self.comboBox_toll.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.comboBox_toll.setMouseTracking(True)
                self.comboBox_toll.setWhatsThis("")
                self.comboBox_toll.setAutoFillBackground(False)
                self.comboBox_toll.setEditable(False)
                self.comboBox_toll.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
                self.comboBox_toll.setMinimumContentsLength(5)
                self.comboBox_toll.setObjectName("comboBox_toll")
                self.comboBox_toll.addItem("")
                self.comboBox_toll.addItem("")
                self.comboBox_toll.addItem("")
                self.label_lane_type = QtWidgets.QLabel(self.groupBox_anpr_config)
                self.label_lane_type.setGeometry(QtCore.QRect(50, 160, 91, 17))
                self.label_lane_type.setObjectName("label_lane_type")
                self.label_mode = QtWidgets.QLabel(self.groupBox_anpr_config)
                self.label_mode.setGeometry(QtCore.QRect(50, 120, 91, 17))
                self.label_mode.setObjectName("label_mode")
                self.comboBox_lane_type = QtWidgets.QComboBox(self.groupBox_anpr_config)
                self.comboBox_lane_type.setEnabled(True)
                self.comboBox_lane_type.setGeometry(QtCore.QRect(200, 160, 311, 21))
                self.comboBox_lane_type.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.comboBox_lane_type.setMouseTracking(True)
                self.comboBox_lane_type.setWhatsThis("")
                self.comboBox_lane_type.setAutoFillBackground(False)
                self.comboBox_lane_type.setEditable(False)
                self.comboBox_lane_type.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
                self.comboBox_lane_type.setMinimumContentsLength(5)
                self.comboBox_lane_type.setObjectName("comboBox_lane_type")
                self.comboBox_lane_type.addItem("")
                self.comboBox_lane_type.addItem("")
                self.comboBox_lane_type.addItem("")
                self.comboBox_lane_type.addItem("")
                self.comboBox_mode = QtWidgets.QComboBox(self.groupBox_anpr_config)
                self.comboBox_mode.setEnabled(True)
                self.comboBox_mode.setGeometry(QtCore.QRect(200, 120, 311, 21))
                self.comboBox_mode.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.comboBox_mode.setMouseTracking(True)
                self.comboBox_mode.setWhatsThis("")
                self.comboBox_mode.setAutoFillBackground(False)
                self.comboBox_mode.setEditable(False)
                self.comboBox_mode.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
                self.comboBox_mode.setMinimumContentsLength(5)
                self.comboBox_mode.setObjectName("comboBox_mode")
                self.comboBox_mode.addItem("")
                self.comboBox_mode.addItem("")
                self.comboBox_mode.addItem("")
                self.label_toll = QtWidgets.QLabel(self.groupBox_anpr_config)
                self.label_toll.setGeometry(QtCore.QRect(50, 80, 91, 17))
                self.label_toll.setObjectName("label_toll")
                self.label_src_type = QtWidgets.QLabel(self.groupBox_anpr_config)
                self.label_src_type.setGeometry(QtCore.QRect(50, 40, 91, 17))
                self.label_src_type.setObjectName("label_src_type")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("controller.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.tabWidget.addTab(self.tab, icon, "")
                self.tab_2 = QtWidgets.QWidget()
                self.tab_2.setObjectName("tab_2")
                self.RTSP_address = QtWidgets.QGroupBox(self.tab_2)
                self.RTSP_address.setGeometry(QtCore.QRect(20, 20, 591, 511))
                self.RTSP_address.setAutoFillBackground(False)
                self.RTSP_address.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.RTSP_address.setObjectName("RTSP_address")
                self.label_cam2 = QtWidgets.QLabel(self.RTSP_address)
                self.label_cam2.setGeometry(QtCore.QRect(90, 100, 81, 17))
                self.label_cam2.setObjectName("label_cam2")
                self.label_cam5 = QtWidgets.QLabel(self.RTSP_address)
                self.label_cam5.setGeometry(QtCore.QRect(90, 240, 81, 17))
                self.label_cam5.setObjectName("label_cam5")
                self.label_cam6 = QtWidgets.QLabel(self.RTSP_address)
                self.label_cam6.setGeometry(QtCore.QRect(90, 290, 81, 17))
                self.label_cam6.setObjectName("label_cam6")
                self.label_cam1 = QtWidgets.QLabel(self.RTSP_address)
                self.label_cam1.setGeometry(QtCore.QRect(90, 50, 81, 17))
                self.label_cam1.setObjectName("label_cam1")
                self.label_cam8 = QtWidgets.QLabel(self.RTSP_address)
                self.label_cam8.setGeometry(QtCore.QRect(90, 390, 81, 17))
                self.label_cam8.setObjectName("label_cam8")
                self.label_cam7 = QtWidgets.QLabel(self.RTSP_address)
                self.label_cam7.setGeometry(QtCore.QRect(90, 340, 81, 17))
                self.label_cam7.setObjectName("label_cam7")
                self.label_cam3 = QtWidgets.QLabel(self.RTSP_address)
                self.label_cam3.setGeometry(QtCore.QRect(90, 150, 81, 17))
                self.label_cam3.setObjectName("label_cam3")
                self.label_cam4 = QtWidgets.QLabel(self.RTSP_address)
                self.label_cam4.setGeometry(QtCore.QRect(90, 200, 81, 17))
                self.label_cam4.setObjectName("label_cam4")
                self.lineEdit_cam8 = QtWidgets.QLineEdit(self.RTSP_address)
                self.lineEdit_cam8.setGeometry(QtCore.QRect(180, 390, 311, 31))
                self.lineEdit_cam8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.lineEdit_cam8.setObjectName("lineEdit_cam8")
                self.lineEdit_cam2 = QtWidgets.QLineEdit(self.RTSP_address)
                self.lineEdit_cam2.setGeometry(QtCore.QRect(180, 90, 311, 31))
                self.lineEdit_cam2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.lineEdit_cam2.setObjectName("lineEdit_cam2")
                self.lineEdit_cam5 = QtWidgets.QLineEdit(self.RTSP_address)
                self.lineEdit_cam5.setGeometry(QtCore.QRect(180, 240, 311, 31))
                self.lineEdit_cam5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.lineEdit_cam5.setObjectName("lineEdit_cam5")
                self.lineEdit_cam6 = QtWidgets.QLineEdit(self.RTSP_address)
                self.lineEdit_cam6.setGeometry(QtCore.QRect(180, 290, 311, 31))
                self.lineEdit_cam6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.lineEdit_cam6.setObjectName("lineEdit_cam6")
                self.lineEdit_cam4 = QtWidgets.QLineEdit(self.RTSP_address)
                self.lineEdit_cam4.setGeometry(QtCore.QRect(180, 190, 311, 31))
                self.lineEdit_cam4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.lineEdit_cam4.setObjectName("lineEdit_cam4")
                self.lineEdit_cam7 = QtWidgets.QLineEdit(self.RTSP_address)
                self.lineEdit_cam7.setGeometry(QtCore.QRect(180, 340, 311, 31))
                self.lineEdit_cam7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.lineEdit_cam7.setObjectName("lineEdit_cam7")
                self.lineEdit_cam3 = QtWidgets.QLineEdit(self.RTSP_address)
                self.lineEdit_cam3.setGeometry(QtCore.QRect(180, 140, 311, 31))
                self.lineEdit_cam3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.lineEdit_cam3.setObjectName("lineEdit_cam3")
                self.lineEdit_cam1 = QtWidgets.QLineEdit(self.RTSP_address)
                self.lineEdit_cam1.setGeometry(QtCore.QRect(180, 40, 311, 31))
                self.lineEdit_cam1.setText("")
                self.lineEdit_cam1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.lineEdit_cam1.setDragEnabled(False)
                self.lineEdit_cam1.setObjectName("lineEdit_cam1")
                self.line_barrierbottom = QtWidgets.QFrame(self.RTSP_address)
                self.line_barrierbottom.setGeometry(QtCore.QRect(20, 440, 551, 16))
                self.line_barrierbottom.setFrameShape(QtWidgets.QFrame.HLine)
                self.line_barrierbottom.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_barrierbottom.setObjectName("line_barrierbottom")
                self.label_eg = QtWidgets.QLabel(self.RTSP_address)
                self.label_eg.setGeometry(QtCore.QRect(20, 460, 67, 17))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setItalic(True)
                self.label_eg.setFont(font)
                self.label_eg.setStyleSheet("QLabel{\n"
                "color:rgb(186, 189, 182)\n"
                "}")
                self.label_eg.setObjectName("label_eg")
                self.label_1_milesight = QtWidgets.QLabel(self.RTSP_address)
                self.label_1_milesight.setGeometry(QtCore.QRect(80, 460, 481, 17))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setItalic(True)
                self.label_1_milesight.setFont(font)
                self.label_1_milesight.setStyleSheet("QLabel{\n"
                "color:rgb(186, 189, 182)\n"
                "}")
                self.label_1_milesight.setObjectName("label_1_milesight")
                self.label_komoto = QtWidgets.QLabel(self.RTSP_address)
                self.label_komoto.setGeometry(QtCore.QRect(80, 480, 481, 17))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setItalic(True)
                self.label_komoto.setFont(font)
                self.label_komoto.setStyleSheet("QLabel{\n"
                "color:rgb(186, 189, 182)\n"
                "}")
                self.label_komoto.setObjectName("label_komoto")
                icon1 = QtGui.QIcon()
                icon1.addPixmap(QtGui.QPixmap("camera.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.tabWidget.addTab(self.tab_2, icon1, "")
                self.line_2_vertical_2 = QtWidgets.QFrame(self.centralwidget)
                self.line_2_vertical_2.setGeometry(QtCore.QRect(10, 40, 641, 16))
                self.line_2_vertical_2.setFrameShape(QtWidgets.QFrame.HLine)
                self.line_2_vertical_2.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_2_vertical_2.setObjectName("line_2_vertical_2")
                self.line_vertical_1 = QtWidgets.QFrame(self.centralwidget)
                self.line_vertical_1.setGeometry(QtCore.QRect(10, 10, 641, 16))
                self.line_vertical_1.setFrameShape(QtWidgets.QFrame.HLine)
                self.line_vertical_1.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_vertical_1.setObjectName("line_vertical_1")
                self.label_ANPR_setting_page = QtWidgets.QLabel(self.centralwidget)
                self.label_ANPR_setting_page.setGeometry(QtCore.QRect(250, 20, 181, 21))
                font = QtGui.QFont()
                font.setPointSize(13)
                self.label_ANPR_setting_page.setFont(font)
                self.label_ANPR_setting_page.setObjectName("label_ANPR_setting_page")


                #------------------------------------------------------------------
                #save button 
                self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
                self.pushButton_save.setGeometry(QtCore.QRect(8, 680, 641, 31))
                font = QtGui.QFont()
                font.setPointSize(13)
                self.pushButton_save.setFont(font)
                self.pushButton_save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.pushButton_save.setStyleSheet("QPushButton{\n"
                "background-color:rgb(186, 189, 182)\n"
                "}")
                icon2 = QtGui.QIcon()
                icon2.addPixmap(QtGui.QPixmap("floppy-disk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.pushButton_save.setIcon(icon2)
                self.pushButton_save.setObjectName("pushButton_save")
                self.pushButton_save.clicked.connect(self.save_button)
                #------------------------------------------------------------------

                MainWindow.setCentralWidget(self.centralwidget)

                self.retranslateUi(MainWindow)
                self.tabWidget.setCurrentIndex(0)
                self.comboBox_controllerIP.setCurrentIndex(0)
                self.comboBox_host_port1.setCurrentIndex(0)
                self.comboBox_host_port2.setCurrentIndex(0)
                self.comboBox_plaza_id.setCurrentIndex(0)
                self.comboBox_video.setCurrentIndex(0)
                self.comboBox_toll.setCurrentIndex(0)
                self.comboBox_lane_type.setCurrentIndex(0)
                self.comboBox_mode.setCurrentIndex(0)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
                self.groupBox_controller_config.setTitle(_translate("MainWindow", "Controller configuration  "))
                self.label_host_port1.setText(_translate("MainWindow", "Host Port 1"))
                self.comboBox_controllerIP.setCurrentText(_translate("MainWindow", "-- Select IP --"))
                self.comboBox_controllerIP.setItemText(0, _translate("MainWindow", "-- Select IP --"))
                self.comboBox_controllerIP.setItemText(1, _translate("MainWindow", "10.20.3.15 - Gombak"))
                self.comboBox_controllerIP.setItemText(2, _translate("MainWindow", "10.20.4.15 - Bentong"))
                self.comboBox_controllerIP.setItemText(3, _translate("MainWindow", "10.20.5.5 - Karak 1 "))
                self.comboBox_controllerIP.setItemText(4, _translate("MainWindow", "10.20.5.6 - Karak 2"))
                self.comboBox_controllerIP.setItemText(5, _translate("MainWindow", "10.20.6.5 - Lanchang"))
                self.comboBox_controllerIP.setItemText(6, _translate("MainWindow", "10.20.7.5 - Temerloh"))
                self.comboBox_controllerIP.setItemText(7, _translate("MainWindow", "10.20.8.5 - Chenor"))
                self.comboBox_controllerIP.setItemText(8, _translate("MainWindow", "10.20.9.5 - Maran"))
                self.comboBox_controllerIP.setItemText(9, _translate("MainWindow", "10.20.10.5 - Srijaya"))
                self.comboBox_controllerIP.setItemText(10, _translate("MainWindow", "10.20.11.5 - Gambang"))
                self.comboBox_controllerIP.setItemText(11, _translate("MainWindow", "10.20.12.5 - Kuantan"))
                self.comboBox_controllerIP.setItemText(12, _translate("MainWindow", "10.20.13.5 - Jabor 1"))
                self.comboBox_controllerIP.setItemText(13, _translate("MainWindow", "10.20.13.6 - Jabor 2"))
                self.label_controller_IP.setText(_translate("MainWindow", "Controller IP"))
                self.comboBox_host_port1.setCurrentText(_translate("MainWindow", "-- Select Port 1 --"))
                self.comboBox_host_port1.setItemText(0, _translate("MainWindow", "-- Select Port 1 --"))
                self.comboBox_host_port1.setItemText(1, _translate("MainWindow", "1000"))
                self.comboBox_host_port1.setItemText(2, _translate("MainWindow", "2000"))
                self.comboBox_host_port1.setItemText(3, _translate("MainWindow", "3000"))
                self.comboBox_host_port1.setItemText(4, _translate("MainWindow", "4000"))
                self.comboBox_host_port1.setItemText(5, _translate("MainWindow", "5000"))
                self.comboBox_host_port1.setItemText(6, _translate("MainWindow", "6000"))
                self.comboBox_host_port1.setItemText(7, _translate("MainWindow", "7000"))
                self.comboBox_host_port1.setItemText(8, _translate("MainWindow", "8000"))
                self.comboBox_host_port1.setItemText(9, _translate("MainWindow", "9000"))
                self.label_host_port2.setText(_translate("MainWindow", "Host Port 2"))
                self.comboBox_host_port2.setCurrentText(_translate("MainWindow", "-- Select Port 2 --"))
                self.comboBox_host_port2.setItemText(0, _translate("MainWindow", "-- Select Port 2 --"))
                self.comboBox_host_port2.setItemText(1, _translate("MainWindow", "1000"))
                self.comboBox_host_port2.setItemText(2, _translate("MainWindow", "2000"))
                self.comboBox_host_port2.setItemText(3, _translate("MainWindow", "3000"))
                self.comboBox_host_port2.setItemText(4, _translate("MainWindow", "4000"))
                self.comboBox_host_port2.setItemText(5, _translate("MainWindow", "5000"))
                self.comboBox_host_port2.setItemText(6, _translate("MainWindow", "6000"))
                self.comboBox_host_port2.setItemText(7, _translate("MainWindow", "7000"))
                self.comboBox_host_port2.setItemText(8, _translate("MainWindow", "8000"))
                self.comboBox_host_port2.setItemText(9, _translate("MainWindow", "9000"))
                self.checkBox_host_port2.setText(_translate("MainWindow", "Host Port 2"))
                self.groupBox_anpr_config.setTitle(_translate("MainWindow", "ANPR configuration"))
                self.label_plaza_id.setText(_translate("MainWindow", "Plaza ID"))
                self.comboBox_plaza_id.setCurrentText(_translate("MainWindow", "-- Select Plaza ID--"))
                self.comboBox_plaza_id.setItemText(0, _translate("MainWindow", "-- Select Plaza ID--"))
                self.comboBox_plaza_id.setItemText(1, _translate("MainWindow", "101 - Gombak"))
                self.comboBox_plaza_id.setItemText(2, _translate("MainWindow", "100 - Bentong"))
                self.comboBox_plaza_id.setItemText(3, _translate("MainWindow", "801 - Karak 1 "))
                self.comboBox_plaza_id.setItemText(4, _translate("MainWindow", "801 - Karak 2"))
                self.comboBox_plaza_id.setItemText(5, _translate("MainWindow", "802 - Lanchang"))
                self.comboBox_plaza_id.setItemText(6, _translate("MainWindow", "803 - Temerloh"))
                self.comboBox_plaza_id.setItemText(7, _translate("MainWindow", "804 - Chenor"))
                self.comboBox_plaza_id.setItemText(8, _translate("MainWindow", "805 - Maran"))
                self.comboBox_plaza_id.setItemText(9, _translate("MainWindow", "806 - Srijaya"))
                self.comboBox_plaza_id.setItemText(10, _translate("MainWindow", "807 - Gambang"))
                self.comboBox_plaza_id.setItemText(11, _translate("MainWindow", "808 - Kuantan"))
                self.comboBox_plaza_id.setItemText(12, _translate("MainWindow", "809 - Jabor 1"))
                self.comboBox_plaza_id.setItemText(13, _translate("MainWindow", "809 - Jabor 2"))
                self.comboBox_video.setCurrentText(_translate("MainWindow", "Video"))
                self.comboBox_video.setItemText(0, _translate("MainWindow", "Video"))
                self.comboBox_video.setItemText(1, _translate("MainWindow", "Image"))
                self.comboBox_toll.setCurrentText(_translate("MainWindow", "-- Select Toll --"))
                self.comboBox_toll.setItemText(0, _translate("MainWindow", "-- Select Toll --"))
                self.comboBox_toll.setItemText(1, _translate("MainWindow", "KLK"))
                self.comboBox_toll.setItemText(2, _translate("MainWindow", "LPT 1"))
                self.label_lane_type.setText(_translate("MainWindow", "Lane type"))
                self.label_mode.setText(_translate("MainWindow", "Mode"))
                self.comboBox_lane_type.setCurrentText(_translate("MainWindow", "-- Select Lane --"))
                self.comboBox_lane_type.setItemText(0, _translate("MainWindow", "-- Select Lane --"))
                self.comboBox_lane_type.setItemText(1, _translate("MainWindow", "Offline"))
                self.comboBox_lane_type.setItemText(2, _translate("MainWindow", "Quatriz"))
                self.comboBox_lane_type.setItemText(3, _translate("MainWindow", "Teras"))
                self.comboBox_mode.setCurrentText(_translate("MainWindow", "-- Select Mode --"))
                self.comboBox_mode.setItemText(0, _translate("MainWindow", "-- Select Mode --"))
                self.comboBox_mode.setItemText(1, _translate("MainWindow", "Online"))
                self.comboBox_mode.setItemText(2, _translate("MainWindow", "Offline"))
                self.label_toll.setText(_translate("MainWindow", "Toll"))
                self.label_src_type.setText(_translate("MainWindow", "Source type"))
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "  Controller"))
                self.RTSP_address.setTitle(_translate("MainWindow", "RTSP address"))
                self.label_cam2.setText(_translate("MainWindow", "Camera 2"))
                self.label_cam5.setText(_translate("MainWindow", "Camera 5"))
                self.label_cam6.setText(_translate("MainWindow", "Camera 6"))
                self.label_cam1.setText(_translate("MainWindow", "Camera 1"))
                self.label_cam8.setText(_translate("MainWindow", "Camera 8"))
                self.label_cam7.setText(_translate("MainWindow", "Camera 7"))
                self.label_cam3.setText(_translate("MainWindow", "Camera 3"))
                self.label_cam4.setText(_translate("MainWindow", "Camera 4"))
                self.lineEdit_cam8.setPlaceholderText(_translate("MainWindow", "rtsp://"))
                self.lineEdit_cam2.setPlaceholderText(_translate("MainWindow", "rtsp://"))
                self.lineEdit_cam5.setPlaceholderText(_translate("MainWindow", "rtsp://"))
                self.lineEdit_cam6.setPlaceholderText(_translate("MainWindow", "rtsp://"))
                self.lineEdit_cam4.setPlaceholderText(_translate("MainWindow", "rtsp://"))
                self.lineEdit_cam7.setPlaceholderText(_translate("MainWindow", "rtsp://"))
                self.lineEdit_cam3.setPlaceholderText(_translate("MainWindow", "rtsp://"))
                self.lineEdit_cam1.setPlaceholderText(_translate("MainWindow", "rtsp://"))
                self.label_eg.setText(_translate("MainWindow", "*e.g : "))
                self.label_1_milesight.setText(_translate("MainWindow", "1. Milesight : rtsp://admin:Milesight12345@10.20.12.31/main"))
                self.label_komoto.setText(_translate("MainWindow", "2. Komoto   : rtsp://root:Komoto@172.18.117.115/cam0_0"))
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Camera"))
                self.label_ANPR_setting_page.setText(_translate("MainWindow", "ANPR Setting Page"))
                self.pushButton_save.setText(_translate("MainWindow", "  Save"))



        # all action in interface @ backend of setting_gui
        def save_button(self):
                chime.success()
                os.system('notify-send "Setting saved !!!"')

        



class ApplicationWindow(QtWidgets.QMainWindow):
        def __init__(self):
                super(ApplicationWindow, self).__init__()

                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)

def read_setting():

        config = configparser.ConfigParser()
        if os.path.isfile('./config.ini'):
                config.read('./config.ini')
        else:
                if os.path.isfile('./setting.ini'):
                        config.read('./setting.ini')
                else:
                        print("ERROR: config.ini or setting.ini file not found.")
                        sys.exit(0)

        #load parameter value
        
        host_IP = config.get('host_setup','host_IP')
        host_port = config.get('host_setup','host_port')

        src_type = config.get('src','input_type')
        toll = config.get('toll','toll_input')
        mode = config.get('src_mode','toll_input')




        print("host_IP", host_IP)

def main():
        app = QtWidgets.QApplication(sys.argv)
        application = ApplicationWindow()
        application.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
        
        
        
        main()