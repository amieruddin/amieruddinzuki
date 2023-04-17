#!/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ANPR_setting.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

import chime    #notification library
import os
import configparser


config_path = os.path.dirname(os.getcwd()) + '/config.ini'
setting_path = os.path.dirname(os.getcwd()) + '/setting.ini'


#------------------------------------------------------------------------------------------------------------------------------------
host_port_i = 0
host_IP_i = 0
# read all parameter value from setting/config

def read_setting():
    main_folder_path = os.path.dirname(os.getcwd())
    config = configparser.ConfigParser()
    if os.path.isfile(config_path):
            config.read(config_path)
            read = "Config"
    else:
            if os.path.isfile(setting_path):
                    config.read(setting_path)
                    read = "Setting"
            else:
                    print("ERROR: config.ini or setting.ini file not found.")
                    sys.exit(0)

    #load parameter value

    global host_IP_i, host_port_i, host_port2_i, src_type_i, toll_i, src_mode0_i, src_mode1_i, src_mode2_i, src_mode3_i, src_mode4_i, src_mode5_i, src_mode6_i, src_mode7_i, lane_type0_i, lane_type1_i, lane_type2_i, lane_type3_i, lane_type4_i, lane_type5_i, lane_type6_i, lane_type7_i, input_src0, input_src1, input_src2, input_src3, input_src4, input_src5, input_src6, input_src7, plaza_ID0_i, plaza_ID1_i, plaza_ID2_i, plaza_ID3_i, plaza_ID4_i, plaza_ID5_i, plaza_ID6_i, plaza_ID7_i, lane_ID0, lane_ID1, lane_ID2, lane_ID3, lane_ID4, lane_ID5, lane_ID6, lane_ID7

    #host setup
    host_IP = config.get('host_setup','host_ip')
    if host_IP == "" : host_IP_i = 0
    if host_IP == "10.20.3.15": host_IP_i = 1
    if host_IP == "10.20.4.15": host_IP_i = 2
    if host_IP == "10.20.5.5": host_IP_i = 3
    if host_IP == "10.20.5.6": host_IP_i = 4
    if host_IP == "10.20.6.5": host_IP_i = 5
    if host_IP == "10.20.7.5": host_IP_i = 6
    if host_IP == "10.20.8.5": host_IP_i = 7
    if host_IP == "10.20.9.5": host_IP_i = 8
    if host_IP == "10.20.10.5": host_IP_i = 9
    if host_IP == "10.20.11.5": host_IP_i = 10
    if host_IP == "10.20.12.5": host_IP_i = 11
    if host_IP == "10.20.13.5": host_IP_i = 12
    if host_IP == "10.20.13.6": host_IP_i = 13
    if host_IP == "local": host_IP_i = 14


    host_port = config.get('host_setup','host_port')
    global host_port_i
    if host_port == "1000": host_port_i = 1
    if host_port == "2000": host_port_i = 2
    if host_port == "3000": host_port_i = 3
    if host_port == "4000": host_port_i = 4
    if host_port == "5000": host_port_i = 5
    if host_port == "6000": host_port_i = 6
    if host_port == "7000": host_port_i = 7
    if host_port == "8000": host_port_i = 8
    if host_port == "9000": host_port_i = 9


    host_port2 = config.get('host_setup', 'host_port2')
    if host_port2 == "": host_port2_i = 0
    if host_port2 == "1000": host_port2_i = 1
    if host_port2 == "2000": host_port2_i = 2
    if host_port2 == "3000": host_port2_i = 3
    if host_port2 == "4000": host_port2_i = 4
    if host_port2 == "5000": host_port2_i = 5
    if host_port2 == "6000": host_port2_i = 6
    if host_port2 == "7000": host_port2_i = 7
    if host_port2 == "8000": host_port2_i = 8
    if host_port2 == "9000": host_port2_i = 9

    #src
    src_type = config.get('src','input_type')
    if src_type == "": src_type_i = 0
    if src_type == "video": src_type_i = 1
    if src_type == "image": src_type_i = 2


    toll = config.get('toll','toll_input')
    if toll == "": toll_i = 0
    if toll == "KLK": toll_i = 1
    if toll == "LPT": toll_i = 2


    #src_mode
    src_mode0 = config.get('src_mode', 'input_mode0')
    src_mode1 = config.get('src_mode', 'input_mode1')
    src_mode2 = config.get('src_mode', 'input_mode2')
    src_mode3 = config.get('src_mode', 'input_mode3')
    src_mode4 = config.get('src_mode', 'input_mode4')
    src_mode5 = config.get('src_mode', 'input_mode5')
    src_mode6 = config.get('src_mode', 'input_mode6')
    src_mode7 = config.get('src_mode', 'input_mode7')

    src_mode0_i = 1 if src_mode0 == "plaza_toll" else 2 if src_mode0 == "offline" else 0
    src_mode1_i = 1 if src_mode1 == "plaza_toll" else 2 if src_mode1 == "offline" else 0
    src_mode2_i = 1 if src_mode2 == "plaza_toll" else 2 if src_mode2 == "offline" else 0
    src_mode3_i = 1 if src_mode3 == "plaza_toll" else 2 if src_mode3 == "offline" else 0
    src_mode4_i = 1 if src_mode4 == "plaza_toll" else 2 if src_mode4 == "offline" else 0
    src_mode5_i = 1 if src_mode5 == "plaza_toll" else 2 if src_mode5 == "offline" else 0
    src_mode6_i = 1 if src_mode6 == "plaza_toll" else 2 if src_mode6 == "offline" else 0
    src_mode7_i = 1 if src_mode7 == "plaza_toll" else 2 if src_mode7 == "offline" else 0


    #lane type
    lane_type0 = config.get('lane_type', 'lane_type0')
    lane_type1 = config.get('lane_type', 'lane_type1')
    lane_type2 = config.get('lane_type', 'lane_type2')
    lane_type3 = config.get('lane_type', 'lane_type3')
    lane_type4 = config.get('lane_type', 'lane_type4')
    lane_type5 = config.get('lane_type', 'lane_type5')
    lane_type6 = config.get('lane_type', 'lane_type6')
    lane_type7 = config.get('lane_type', 'lane_type7')

    lane_type0_i = 1 if lane_type0 == "offline" else 2 if lane_type0 == "QUATRIZ" else 3 if lane_type0 == "TERAS" else 0
    lane_type1_i = 1 if lane_type1 == "offline" else 2 if lane_type1 == "QUATRIZ" else 3 if lane_type1 == "TERAS" else 0
    lane_type2_i = 1 if lane_type2 == "offline" else 2 if lane_type2 == "QUATRIZ" else 3 if lane_type2 == "TERAS" else 0
    lane_type3_i = 1 if lane_type3 == "offline" else 2 if lane_type3 == "QUATRIZ" else 3 if lane_type3 == "TERAS" else 0
    lane_type4_i = 1 if lane_type4 == "offline" else 2 if lane_type4 == "QUATRIZ" else 3 if lane_type4 == "TERAS" else 0
    lane_type5_i = 1 if lane_type5 == "offline" else 2 if lane_type5 == "QUATRIZ" else 3 if lane_type5 == "TERAS" else 0
    lane_type6_i = 1 if lane_type6 == "offline" else 2 if lane_type6 == "QUATRIZ" else 3 if lane_type6 == "TERAS" else 0
    lane_type7_i = 1 if lane_type7 == "offline" else 2 if lane_type7 == "QUATRIZ" else 3 if lane_type7 == "TERAS" else 0


    #plaza ID
    plaza_ID0 = config.get('src_id', 'input_id0')[:3]
    plaza_ID1 = config.get('src_id', 'input_id1')[:3]
    plaza_ID2 = config.get('src_id', 'input_id2')[:3]
    plaza_ID3 = config.get('src_id', 'input_id3')[:3]
    plaza_ID4 = config.get('src_id', 'input_id4')[:3]
    plaza_ID5 = config.get('src_id', 'input_id5')[:3]
    plaza_ID6 = config.get('src_id', 'input_id6')[:3]
    plaza_ID7 = config.get('src_id', 'input_id7')[:3]
    

    plaza_ID0_i = 1 if plaza_ID0 == "101" else 2 if plaza_ID0 == "100" else 3 if plaza_ID0 == "801" else 4 if plaza_ID0 == "802" else 5 if plaza_ID0 == "803" else 6 if plaza_ID0 == "804" else 7 if plaza_ID0 == "805" else 8 if plaza_ID0 == "806" else 9 if plaza_ID0 == "807" else 10 if plaza_ID0 == "808" else 11 if plaza_ID0 == "809" else 0    
    plaza_ID1_i = 1 if plaza_ID1 == "101" else 2 if plaza_ID1 == "100" else 3 if plaza_ID1 == "801" else 4 if plaza_ID1 == "802" else 5 if plaza_ID1 == "803" else 6 if plaza_ID1 == "804" else 7 if plaza_ID1 == "805" else 8 if plaza_ID1 == "806" else 9 if plaza_ID1 == "807" else 10 if plaza_ID1 == "808" else 11 if plaza_ID1 == "809" else 0    
    plaza_ID2_i = 1 if plaza_ID2 == "101" else 2 if plaza_ID2 == "100" else 3 if plaza_ID2 == "801" else 4 if plaza_ID2 == "802" else 5 if plaza_ID2 == "803" else 6 if plaza_ID2 == "804" else 7 if plaza_ID2 == "805" else 8 if plaza_ID2 == "806" else 9 if plaza_ID2 == "807" else 10 if plaza_ID2 == "808" else 11 if plaza_ID2 == "809" else 0    
    plaza_ID3_i = 1 if plaza_ID3 == "101" else 2 if plaza_ID3 == "100" else 3 if plaza_ID3 == "801" else 4 if plaza_ID3 == "802" else 5 if plaza_ID3 == "803" else 6 if plaza_ID3 == "804" else 7 if plaza_ID3 == "805" else 8 if plaza_ID3 == "806" else 9 if plaza_ID3 == "807" else 10 if plaza_ID3 == "808" else 11 if plaza_ID3 == "809" else 0    
    plaza_ID4_i = 1 if plaza_ID4 == "101" else 2 if plaza_ID4 == "100" else 3 if plaza_ID4 == "801" else 4 if plaza_ID4 == "802" else 5 if plaza_ID4 == "803" else 6 if plaza_ID4 == "804" else 7 if plaza_ID4 == "805" else 8 if plaza_ID4 == "806" else 9 if plaza_ID4 == "807" else 10 if plaza_ID4 == "808" else 11 if plaza_ID4 == "809" else 0    
    plaza_ID5_i = 1 if plaza_ID5 == "101" else 2 if plaza_ID5 == "100" else 3 if plaza_ID5 == "801" else 4 if plaza_ID5 == "802" else 5 if plaza_ID5 == "803" else 6 if plaza_ID5 == "804" else 7 if plaza_ID5 == "805" else 8 if plaza_ID5 == "806" else 9 if plaza_ID5 == "807" else 10 if plaza_ID5 == "808" else 11 if plaza_ID5 == "809" else 0    
    plaza_ID6_i = 1 if plaza_ID6 == "101" else 2 if plaza_ID6 == "100" else 3 if plaza_ID6 == "801" else 4 if plaza_ID6 == "802" else 5 if plaza_ID6 == "803" else 6 if plaza_ID6 == "804" else 7 if plaza_ID6 == "805" else 8 if plaza_ID6 == "806" else 9 if plaza_ID6 == "807" else 10 if plaza_ID6 == "808" else 11 if plaza_ID6 == "809" else 0    
    plaza_ID7_i = 1 if plaza_ID7 == "101" else 2 if plaza_ID7 == "100" else 3 if plaza_ID7 == "801" else 4 if plaza_ID7 == "802" else 5 if plaza_ID7 == "803" else 6 if plaza_ID7 == "804" else 7 if plaza_ID7 == "805" else 8 if plaza_ID7 == "806" else 9 if plaza_ID7 == "807" else 10 if plaza_ID7 == "808" else 11 if plaza_ID7 == "809" else 0    


    #lane ID
    lane_ID0 = config.get('src_id', 'input_id0')[4:]
    lane_ID1 = config.get('src_id', 'input_id1')[4:]
    lane_ID2 = config.get('src_id', 'input_id2')[4:]
    lane_ID3 = config.get('src_id', 'input_id3')[4:]
    lane_ID4 = config.get('src_id', 'input_id4')[4:]
    lane_ID5 = config.get('src_id', 'input_id5')[4:]
    lane_ID6 = config.get('src_id', 'input_id6')[4:]
    lane_ID7 = config.get('src_id', 'input_id7')[4:]


    #src input
    input_src0 = config.get('src_input', 'input_src0')
    input_src1 = config.get('src_input', 'input_src1')
    input_src2 = config.get('src_input', 'input_src2')
    input_src3 = config.get('src_input', 'input_src3')
    input_src4 = config.get('src_input', 'input_src4')
    input_src5 = config.get('src_input', 'input_src5')
    input_src6 = config.get('src_input', 'input_src6')
    input_src7 = config.get('src_input', 'input_src7')

    


    
    return read, host_IP_i, host_port_i, host_port2_i, src_type_i, toll_i, src_mode0_i, src_mode1_i, src_mode2_i, src_mode3_i, src_mode4_i, src_mode5_i, src_mode6_i, src_mode7_i, lane_type0_i, lane_type1_i, lane_type2_i, lane_type3_i, lane_type4_i, lane_type5_i, lane_type6_i, lane_type7_i, input_src0, input_src1, input_src2, input_src3, input_src4, input_src5, input_src6, input_src7, plaza_ID0_i, plaza_ID1_i, plaza_ID2_i, plaza_ID3_i, plaza_ID4_i, plaza_ID5_i, plaza_ID6_i, plaza_ID7_i, lane_ID0, lane_ID1, lane_ID2, lane_ID3, lane_ID4, lane_ID5, lane_ID6, lane_ID7
    



#read setting 
read, host_IP_i, host_port_i, host_port2_i , src_type_i, toll_i, src_mode0_i, src_mode1_i, src_mode2_i, src_mode3_i, src_mode4_i, src_mode5_i, src_mode6_i, src_mode7_i, lane_type0_i, lane_type1_i, lane_type2_i, lane_type3_i, lane_type4_i, lane_type5_i, lane_type6_i, lane_type7_i, input_src0, input_src1, input_src2, input_src3, input_src4, input_src5, input_src6, input_src7, plaza_ID0_i, plaza_ID1_i, plaza_ID2_i, plaza_ID3_i, plaza_ID4_i, plaza_ID5_i, plaza_ID6_i, plaza_ID7_i, lane_ID0, lane_ID1, lane_ID2, lane_ID3, lane_ID4, lane_ID5, lane_ID6, lane_ID7 = read_setting()

# index already specific follow sequence in setting
# 0 = host_IP ; 1 = host_port ; 2 = host_port2 ; 3 = input_type ; 4 = toll 
# setting_changed_list = ["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""] 
setting_changed_list = [""]*45      #initialize 45 empty list


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(663, 727)

        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        MainWindow.setFont(font)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/service.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
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
        self.tab_controller = QtWidgets.QWidget()
        self.tab_controller.setObjectName("tab_controller")
        self.groupBox_controller_config = QtWidgets.QGroupBox(self.tab_controller)
        self.groupBox_controller_config.setGeometry(QtCore.QRect(20, 30, 591, 381))
        self.groupBox_controller_config.setObjectName("groupBox_controller_config")


        #--------------------------------------------------------------------------------
        #controller IP

        self.label_controller_IP = QtWidgets.QLabel(self.groupBox_controller_config)
        self.label_controller_IP.setGeometry(QtCore.QRect(50, 50, 101, 17))
        self.label_controller_IP.setObjectName("label_controller_IP")

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
        self.comboBox_controllerIP.addItem("")

        #when select list
        self.comboBox_controllerIP.currentIndexChanged.connect(self.select_controller_IP)

        #------------------------------------------------------------------------------
        # host port 1
        self.label_host_port1 = QtWidgets.QLabel(self.groupBox_controller_config)
        self.label_host_port1.setGeometry(QtCore.QRect(50, 90, 91, 17))
        self.label_host_port1.setObjectName("label_host_port1")

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

        #when select list
        self.comboBox_host_port1.currentIndexChanged.connect(self.select_host_port)


        #------------------------------------------------------------------------------

        # checkBox_host_port2
        self.checkBox_host_port2 = QtWidgets.QCheckBox(self.groupBox_controller_config)
        self.checkBox_host_port2.setGeometry(QtCore.QRect(200, 130, 111, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBox_host_port2.setFont(font)
        self.checkBox_host_port2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkBox_host_port2.setChecked(False) if host_port2_i == 0 else self.checkBox_host_port2.setChecked(True)

        self.checkBox_host_port2.stateChanged.connect(self.enable_host_port2)
        self.checkBox_host_port2.setObjectName("checkBox_host_port2")


        #host port 2
        self.label_host_port2 = QtWidgets.QLabel(self.groupBox_controller_config)
        self.label_host_port2.setGeometry(QtCore.QRect(50, 160, 91, 17))
        self.label_host_port2.setEnabled(False) if host_port2_i == 0 else self.label_host_port2.setEnabled(True)
        self.label_host_port2.setObjectName("label_host_port2")
        
        self.comboBox_host_port2 = QtWidgets.QComboBox(self.groupBox_controller_config)
        self.comboBox_host_port2.setEnabled(False) if host_port2_i == 0 else self.comboBox_host_port2.setEnabled(True)
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

        #when select list
        self.comboBox_host_port2.currentIndexChanged.connect(self.select_host_port2)

        #-------------------------------------------------------------------------------
        #source type

        self.label_src_type = QtWidgets.QLabel(self.groupBox_controller_config)
        self.label_src_type.setGeometry(QtCore.QRect(50, 200, 91, 17))
        self.label_src_type.setObjectName("label_src_type")

        self.comboBox_video = QtWidgets.QComboBox(self.groupBox_controller_config)
        self.comboBox_video.setEnabled(True)
        self.comboBox_video.setGeometry(QtCore.QRect(200, 200, 311, 21))
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
        self.comboBox_video.addItem("")

        #when select list
        self.comboBox_video.currentIndexChanged.connect(self.select_source_type)
        

        #----------------------------------------------------------------------------------------
        # toll
        self.label_toll = QtWidgets.QLabel(self.groupBox_controller_config)
        self.label_toll.setGeometry(QtCore.QRect(50, 240, 91, 17))
        self.label_toll.setObjectName("label_toll")

        self.comboBox_toll = QtWidgets.QComboBox(self.groupBox_controller_config)
        self.comboBox_toll.setEnabled(True)
        self.comboBox_toll.setGeometry(QtCore.QRect(200, 240, 311, 21))
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

        #when select list
        self.comboBox_toll.currentIndexChanged.connect(self.select_toll)

        #---------------------------------------------------------------------------------------




        # =================================================================
        # |                                                               |
        # |                       Start Tab Camera                        |
        # |                                                               |
        # =================================================================


        #---------------------------------------------------------------------------------------

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/controller.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_controller, icon, "")
        self.tab_camera = QtWidgets.QWidget()
        self.tab_camera.setObjectName("tab_camera")
        self.tabWidget_camera_tab = QtWidgets.QTabWidget(self.tab_camera)
        self.tabWidget_camera_tab.setGeometry(QtCore.QRect(-10, 0, 661, 551))
        self.tabWidget_camera_tab.setObjectName("tabWidget_camera_tab")

        #----------------------------------------------------------------------------------------
        
        # tab cam 1

        self.tab_cam1 = QtWidgets.QWidget()
        self.tab_cam1.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tab_cam1.setObjectName("tab_cam1")
        self.groupBox_anpr_config_cam1 = QtWidgets.QGroupBox(self.tab_cam1)
        self.groupBox_anpr_config_cam1.setGeometry(QtCore.QRect(20, 20, 611, 431))
        self.groupBox_anpr_config_cam1.setObjectName("groupBox_anpr_config_cam1")

        #anpr button
        self.label_ANPR_cam1 = QtWidgets.QLabel(self.groupBox_anpr_config_cam1)
        self.label_ANPR_cam1.setGeometry(QtCore.QRect(50, 40, 51, 17))
        self.label_ANPR_cam1.setObjectName("label_ANPR_cam1")
        self.radioButton_on_anpr_cam1 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam1)
        self.radioButton_on_anpr_cam1.setGeometry(QtCore.QRect(180, 40, 51, 23))
        self.radioButton_on_anpr_cam1.setChecked(True)
        self.radioButton_on_anpr_cam1.setObjectName("radioButton_on_anpr_cam1")
        self.radioButton_off_anpr_cam1 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam1)
        self.radioButton_off_anpr_cam1.setGeometry(QtCore.QRect(240, 40, 61, 23))
        self.radioButton_off_anpr_cam1.setObjectName("radioButton_off_anpr_cam1")
        self.buttonGroup_anpr_cam1 = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup_anpr_cam1.addButton(self.radioButton_on_anpr_cam1)
        self.buttonGroup_anpr_cam1.addButton(self.radioButton_off_anpr_cam1)
        self.buttonGroup_anpr_cam1.setObjectName("buttonGroup_anpr_cam1")

        #vavc button
        self.label_VAVC_cam1 = QtWidgets.QLabel(self.groupBox_anpr_config_cam1)
        self.label_VAVC_cam1.setGeometry(QtCore.QRect(50, 80, 51, 17))
        self.label_VAVC_cam1.setObjectName("label_VAVC_cam1")
        self.radioButton_on_vavc_cam1 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam1)
        self.radioButton_on_vavc_cam1.setGeometry(QtCore.QRect(180, 80, 51, 23))
        self.radioButton_on_vavc_cam1.setEnabled(False)
        self.radioButton_on_vavc_cam1.setObjectName("radioButton_on_vavc_cam1")
        self.radioButton_off_vavc_cam1 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam1)
        self.radioButton_off_vavc_cam1.setGeometry(QtCore.QRect(240, 80, 61, 23))
        self.radioButton_off_vavc_cam1.setChecked(True)
        self.radioButton_off_vavc_cam1.setObjectName("radioButton_off_vavc_cam1")
        self.buttonGroup_vavc_cam1 = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup_vavc_cam1.setObjectName("buttonGroup_vavc_cam1")
        self.buttonGroup_vavc_cam1.addButton(self.radioButton_off_vavc_cam1)
        self.buttonGroup_vavc_cam1.addButton(self.radioButton_on_vavc_cam1)

        #mode
        self.label_mode_cam1 = QtWidgets.QLabel(self.groupBox_anpr_config_cam1)
        self.label_mode_cam1.setGeometry(QtCore.QRect(50, 120, 91, 17))
        self.label_mode_cam1.setObjectName("label_mode_cam1")
        self.comboBox_mode_cam1 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam1)
        self.comboBox_mode_cam1.setEnabled(True)
        self.comboBox_mode_cam1.setGeometry(QtCore.QRect(180, 120, 311, 21))
        self.comboBox_mode_cam1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_mode_cam1.setMouseTracking(True)
        self.comboBox_mode_cam1.setWhatsThis("")
        self.comboBox_mode_cam1.setAutoFillBackground(False)
        self.comboBox_mode_cam1.setEditable(False)
        self.comboBox_mode_cam1.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_mode_cam1.setMinimumContentsLength(5)
        self.comboBox_mode_cam1.setObjectName("comboBox_mode_cam1")
        self.comboBox_mode_cam1.addItem("")
        self.comboBox_mode_cam1.addItem("")
        self.comboBox_mode_cam1.addItem("")
        #when select list
        self.comboBox_mode_cam1.currentIndexChanged.connect(self.select_mode0)

        

        

        #lane type
        self.label_lane_type_cam1 = QtWidgets.QLabel(self.groupBox_anpr_config_cam1)
        self.label_lane_type_cam1.setGeometry(QtCore.QRect(50, 160, 91, 17))
        self.label_lane_type_cam1.setObjectName("label_lane_type_cam1")
        self.comboBox_lane_type_cam1 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam1)
        self.comboBox_lane_type_cam1.setEnabled(True)
        self.comboBox_lane_type_cam1.setGeometry(QtCore.QRect(180, 160, 311, 21))
        self.comboBox_lane_type_cam1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_lane_type_cam1.setMouseTracking(True)
        self.comboBox_lane_type_cam1.setWhatsThis("")
        self.comboBox_lane_type_cam1.setAutoFillBackground(False)
        self.comboBox_lane_type_cam1.setEditable(False)
        self.comboBox_lane_type_cam1.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_lane_type_cam1.setMinimumContentsLength(5)
        self.comboBox_lane_type_cam1.setObjectName("comboBox_lane_type_cam1")
        self.comboBox_lane_type_cam1.addItem("")
        self.comboBox_lane_type_cam1.addItem("")
        self.comboBox_lane_type_cam1.addItem("")
        self.comboBox_lane_type_cam1.addItem("")
        #when select list
        self.comboBox_lane_type_cam1.currentIndexChanged.connect(self.select_lane_type0)

        #Plaza ID
        self.label_plaza_id_cam1 = QtWidgets.QLabel(self.groupBox_anpr_config_cam1)
        self.label_plaza_id_cam1.setGeometry(QtCore.QRect(50, 200, 67, 17))
        self.label_plaza_id_cam1.setObjectName("label_plaza_id_cam1")
        self.comboBox_plaza_id_cam1 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam1)
        self.comboBox_plaza_id_cam1.setEnabled(True)
        self.comboBox_plaza_id_cam1.setGeometry(QtCore.QRect(180, 200, 311, 21))
        self.comboBox_plaza_id_cam1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_plaza_id_cam1.setMouseTracking(True)
        self.comboBox_plaza_id_cam1.setWhatsThis("")
        self.comboBox_plaza_id_cam1.setAutoFillBackground(False)
        self.comboBox_plaza_id_cam1.setEditable(False)
        self.comboBox_plaza_id_cam1.setMaxVisibleItems(10)
        self.comboBox_plaza_id_cam1.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_plaza_id_cam1.setMinimumContentsLength(5)
        self.comboBox_plaza_id_cam1.setFrame(True)
        self.comboBox_plaza_id_cam1.setObjectName("comboBox_plaza_id_cam1")
        self.comboBox_plaza_id_cam1.addItem("")
        self.comboBox_plaza_id_cam1.addItem("")
        self.comboBox_plaza_id_cam1.addItem("")
        self.comboBox_plaza_id_cam1.addItem("")
        self.comboBox_plaza_id_cam1.addItem("")
        self.comboBox_plaza_id_cam1.addItem("")
        self.comboBox_plaza_id_cam1.addItem("")
        self.comboBox_plaza_id_cam1.addItem("")
        self.comboBox_plaza_id_cam1.addItem("")
        self.comboBox_plaza_id_cam1.addItem("")
        self.comboBox_plaza_id_cam1.addItem("")
        self.comboBox_plaza_id_cam1.addItem("")
        #when select list
        self.comboBox_plaza_id_cam1.currentIndexChanged.connect(self.select_plaza_ID0)



        #Lane ID
        self.label_lane_id_cam1 = QtWidgets.QLabel(self.groupBox_anpr_config_cam1)
        self.label_lane_id_cam1.setGeometry(QtCore.QRect(50, 250, 67, 17))
        self.label_lane_id_cam1.setObjectName("label_lane_id_cam1")
        self.lineEdit_lane_id_cam1 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam1)
        self.lineEdit_lane_id_cam1.setGeometry(QtCore.QRect(180, 240, 380, 31))
        self.lineEdit_lane_id_cam1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_lane_id_cam1.setDragEnabled(False)
        self.lineEdit_lane_id_cam1.setObjectName("lineEdit_lane_id_cam1")
        self.lineEdit_lane_id_cam1.setText(lane_ID0)

        setting_changed_list[37] = lane_ID0
        self.lineEdit_lane_id_cam1.textChanged.connect(self.lane_ID0)

        #rtsp camera
        self.label_rtsp_cam1 = QtWidgets.QLabel(self.groupBox_anpr_config_cam1)
        self.label_rtsp_cam1.setGeometry(QtCore.QRect(50, 300, 81, 17))
        self.label_rtsp_cam1.setObjectName("label_rtsp_cam1")
        self.lineEdit_rtsp_cam1 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam1)
        self.lineEdit_rtsp_cam1.setGeometry(QtCore.QRect(180, 290, 380, 31))
        self.lineEdit_rtsp_cam1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_rtsp_cam1.setDragEnabled(False)
        self.lineEdit_rtsp_cam1.setObjectName("lineEdit_rtsp_cam1")
        self.lineEdit_rtsp_cam1.setText(input_src0)
        
        setting_changed_list[21] = input_src0
        self.lineEdit_rtsp_cam1.textChanged.connect(self.rtsp0)
 
        self.label_1_milesight_16 = QtWidgets.QLabel(self.groupBox_anpr_config_cam1)
        self.label_1_milesight_16.setGeometry(QtCore.QRect(50, 370, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_1_milesight_16.setFont(font)
        self.label_1_milesight_16.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_1_milesight_16.setObjectName("label_1_milesight_16")
        self.label_komoto_16 = QtWidgets.QLabel(self.groupBox_anpr_config_cam1)
        self.label_komoto_16.setGeometry(QtCore.QRect(50, 390, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_komoto_16.setFont(font)
        self.label_komoto_16.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_komoto_16.setObjectName("label_komoto_16")
        self.label_eg_16 = QtWidgets.QLabel(self.groupBox_anpr_config_cam1)
        self.label_eg_16.setGeometry(QtCore.QRect(50, 350, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_eg_16.setFont(font)
        self.label_eg_16.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_eg_16.setObjectName("label_eg_16")
        self.tabWidget_camera_tab.addTab(self.tab_cam1, "")

        #-------------------------------------------------------------------------------------
        #tab cam 2
        
        self.tab_cam2 = QtWidgets.QWidget()
        self.tab_cam2.setObjectName("tab_cam2")
        self.groupBox_anpr_config_cam2 = QtWidgets.QGroupBox(self.tab_cam2)
        self.groupBox_anpr_config_cam2.setGeometry(QtCore.QRect(20, 20, 611, 431))
        self.groupBox_anpr_config_cam2.setObjectName("groupBox_anpr_config_cam2")

        #anpr button
        self.label_ANPR_cam2 = QtWidgets.QLabel(self.groupBox_anpr_config_cam2)
        self.label_ANPR_cam2.setGeometry(QtCore.QRect(50, 40, 51, 17))
        self.label_ANPR_cam2.setObjectName("label_ANPR_cam2")
        self.buttonGroup_anpr_cam2 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_anpr_cam2 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam2)
        self.radioButton_on_anpr_cam2.setGeometry(QtCore.QRect(180, 40, 51, 23))
        self.radioButton_on_anpr_cam2.setChecked(True)
        self.radioButton_on_anpr_cam2.setObjectName("radioButton_on_anpr_cam2")
        self.buttonGroup_anpr_cam2.addButton(self.radioButton_on_anpr_cam2)
        self.radioButton_off_anpr_cam2 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam2)
        self.radioButton_off_anpr_cam2.setGeometry(QtCore.QRect(240, 40, 61, 23))
        self.radioButton_off_anpr_cam2.setObjectName("radioButton_off_anpr_cam2")
        self.buttonGroup_anpr_cam2.setObjectName("buttonGroup_anpr_cam2")
        self.buttonGroup_anpr_cam2.addButton(self.radioButton_off_anpr_cam2)

        #vavc button
        self.label_VAVC_cam2 = QtWidgets.QLabel(self.groupBox_anpr_config_cam2)
        self.label_VAVC_cam2.setGeometry(QtCore.QRect(50, 80, 51, 17))
        self.label_VAVC_cam2.setObjectName("label_VAVC_cam2")
        self.buttonGroup_vavc_cam2 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_vavc_cam2 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam2)
        self.radioButton_on_vavc_cam2.setGeometry(QtCore.QRect(180, 80, 51, 23))
        self.radioButton_on_vavc_cam2.setEnabled(False)
        self.radioButton_on_vavc_cam2.setObjectName("radioButton_on_vavc_cam2")
        self.buttonGroup_vavc_cam2.addButton(self.radioButton_on_vavc_cam2)
        self.radioButton_off_vavc_cam2 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam2)
        self.radioButton_off_vavc_cam2.setGeometry(QtCore.QRect(240, 80, 61, 23))
        self.radioButton_off_vavc_cam2.setChecked(True)
        self.radioButton_off_vavc_cam2.setObjectName("radioButton_off_vavc_cam2")
        self.buttonGroup_vavc_cam2.setObjectName("buttonGroup_vavc_cam2")
        self.buttonGroup_vavc_cam2.addButton(self.radioButton_off_vavc_cam2)

        #mode
        self.label_mode_cam2 = QtWidgets.QLabel(self.groupBox_anpr_config_cam2)
        self.label_mode_cam2.setGeometry(QtCore.QRect(50, 120, 91, 17))
        self.label_mode_cam2.setObjectName("label_mode_cam2")
        self.comboBox_mode_cam2 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam2)
        self.comboBox_mode_cam2.setEnabled(True)
        self.comboBox_mode_cam2.setGeometry(QtCore.QRect(180, 120, 311, 21))
        self.comboBox_mode_cam2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_mode_cam2.setMouseTracking(True)
        self.comboBox_mode_cam2.setWhatsThis("")
        self.comboBox_mode_cam2.setAutoFillBackground(False)
        self.comboBox_mode_cam2.setEditable(False)
        self.comboBox_mode_cam2.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_mode_cam2.setMinimumContentsLength(5)
        self.comboBox_mode_cam2.setObjectName("comboBox_mode_cam2")
        self.comboBox_mode_cam2.addItem("")
        self.comboBox_mode_cam2.addItem("")
        self.comboBox_mode_cam2.addItem("")
        #when select list
        self.comboBox_mode_cam2.currentIndexChanged.connect(self.select_mode1)


        #lane type
        self.label_lane_type_cam2 = QtWidgets.QLabel(self.groupBox_anpr_config_cam2)
        self.label_lane_type_cam2.setGeometry(QtCore.QRect(50, 160, 91, 17))
        self.label_lane_type_cam2.setObjectName("label_lane_type_cam2")
        self.comboBox_lane_type_cam2 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam2)
        self.comboBox_lane_type_cam2.setEnabled(True)
        self.comboBox_lane_type_cam2.setGeometry(QtCore.QRect(180, 160, 311, 21))
        self.comboBox_lane_type_cam2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_lane_type_cam2.setMouseTracking(True)
        self.comboBox_lane_type_cam2.setWhatsThis("")
        self.comboBox_lane_type_cam2.setAutoFillBackground(False)
        self.comboBox_lane_type_cam2.setEditable(False)
        self.comboBox_lane_type_cam2.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_lane_type_cam2.setMinimumContentsLength(5)
        self.comboBox_lane_type_cam2.setObjectName("comboBox_lane_type_cam2")
        self.comboBox_lane_type_cam2.addItem("")
        self.comboBox_lane_type_cam2.addItem("")
        self.comboBox_lane_type_cam2.addItem("")
        self.comboBox_lane_type_cam2.addItem("")
        #when select list
        self.comboBox_lane_type_cam2.currentIndexChanged.connect(self.select_lane_type1)
        

        #Plaza ID
        self.label_plaza_id_cam2 = QtWidgets.QLabel(self.groupBox_anpr_config_cam2)
        self.label_plaza_id_cam2.setGeometry(QtCore.QRect(50, 200, 67, 17))
        self.label_plaza_id_cam2.setObjectName("label_plaza_id_cam2")
        self.comboBox_plaza_id_cam2 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam2)
        self.comboBox_plaza_id_cam2.setEnabled(True)
        self.comboBox_plaza_id_cam2.setGeometry(QtCore.QRect(180, 200, 311, 21))
        self.comboBox_plaza_id_cam2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_plaza_id_cam2.setMouseTracking(True)
        self.comboBox_plaza_id_cam2.setWhatsThis("")
        self.comboBox_plaza_id_cam2.setAutoFillBackground(False)
        self.comboBox_plaza_id_cam2.setEditable(False)
        self.comboBox_plaza_id_cam2.setMaxVisibleItems(10)
        self.comboBox_plaza_id_cam2.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_plaza_id_cam2.setMinimumContentsLength(5)
        self.comboBox_plaza_id_cam2.setFrame(True)
        self.comboBox_plaza_id_cam2.setObjectName("comboBox_plaza_id_cam2")
        self.comboBox_plaza_id_cam2.addItem("")
        self.comboBox_plaza_id_cam2.addItem("")
        self.comboBox_plaza_id_cam2.addItem("")
        self.comboBox_plaza_id_cam2.addItem("")
        self.comboBox_plaza_id_cam2.addItem("")
        self.comboBox_plaza_id_cam2.addItem("")
        self.comboBox_plaza_id_cam2.addItem("")
        self.comboBox_plaza_id_cam2.addItem("")
        self.comboBox_plaza_id_cam2.addItem("")
        self.comboBox_plaza_id_cam2.addItem("")
        self.comboBox_plaza_id_cam2.addItem("")
        self.comboBox_plaza_id_cam2.addItem("")
        #when select list
        self.comboBox_plaza_id_cam2.currentIndexChanged.connect(self.select_plaza_ID1)

        #Lane ID
        self.label_lane_id_cam2 = QtWidgets.QLabel(self.groupBox_anpr_config_cam2)
        self.label_lane_id_cam2.setGeometry(QtCore.QRect(50, 250, 67, 17))
        self.label_lane_id_cam2.setObjectName("label_lane_id_cam2")
        self.lineEdit_lane_id_cam2 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam2)
        self.lineEdit_lane_id_cam2.setGeometry(QtCore.QRect(180, 240, 380, 31))
        self.lineEdit_lane_id_cam2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_lane_id_cam2.setDragEnabled(False)
        self.lineEdit_lane_id_cam2.setObjectName("lineEdit_lane_id_cam2")
        self.lineEdit_lane_id_cam2.setText(lane_ID1)

        setting_changed_list[38] = lane_ID1
        self.lineEdit_lane_id_cam2.textChanged.connect(self.lane_ID1)

        #rtsp camera
        self.label_rtsp_cam2 = QtWidgets.QLabel(self.groupBox_anpr_config_cam2)
        self.label_rtsp_cam2.setGeometry(QtCore.QRect(50, 300, 81, 17))
        self.label_rtsp_cam2.setObjectName("label_rtsp_cam2")
        self.lineEdit_rtsp_cam2 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam2)
        self.lineEdit_rtsp_cam2.setGeometry(QtCore.QRect(180, 290, 380, 31))
        self.lineEdit_rtsp_cam2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_rtsp_cam2.setDragEnabled(False)
        self.lineEdit_rtsp_cam2.setObjectName("lineEdit_rtsp_cam2")
        self.lineEdit_rtsp_cam2.setText(input_src1)
        self.lineEdit_rtsp_cam2.textChanged.connect(self.rtsp1)
        
        setting_changed_list[22] = input_src1
        self.lineEdit_rtsp_cam2.textChanged.connect(self.rtsp1)
        

        self.label_1_milesight_17 = QtWidgets.QLabel(self.groupBox_anpr_config_cam2)
        self.label_1_milesight_17.setGeometry(QtCore.QRect(50, 370, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_1_milesight_17.setFont(font)
        self.label_1_milesight_17.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_1_milesight_17.setObjectName("label_1_milesight_17")
        self.label_komoto_17 = QtWidgets.QLabel(self.groupBox_anpr_config_cam2)
        self.label_komoto_17.setGeometry(QtCore.QRect(50, 390, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_komoto_17.setFont(font)
        self.label_komoto_17.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_komoto_17.setObjectName("label_komoto_17")

        self.label_eg_17 = QtWidgets.QLabel(self.groupBox_anpr_config_cam2)
        self.label_eg_17.setGeometry(QtCore.QRect(50, 350, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_eg_17.setFont(font)
        self.label_eg_17.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_eg_17.setObjectName("label_eg_17")

        self.frame_cam2 = QtWidgets.QFrame(self.tab_cam2)
        self.frame_cam2.setGeometry(QtCore.QRect(-1, -11, 651, 521))
        self.frame_cam2.setAutoFillBackground(True)
        self.frame_cam2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_cam2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_cam2.setObjectName("frame_cam2")
        self.frame_cam2.raise_()
        self.groupBox_anpr_config_cam2.raise_()
        self.tabWidget_camera_tab.addTab(self.tab_cam2, "")

        #---------------------------------------------------------------------------------------------
        # tab cam 3
        self.tab_cam3 = QtWidgets.QWidget()
        self.tab_cam3.setObjectName("tab_cam3")
        self.groupBox_anpr_config_cam3 = QtWidgets.QGroupBox(self.tab_cam3)
        self.groupBox_anpr_config_cam3.setGeometry(QtCore.QRect(20, 20, 611, 431))
        self.groupBox_anpr_config_cam3.setObjectName("groupBox_anpr_config_cam3")

        #anpr button
        self.label_ANPR_cam3 = QtWidgets.QLabel(self.groupBox_anpr_config_cam3)
        self.label_ANPR_cam3.setGeometry(QtCore.QRect(50, 40, 51, 17))
        self.label_ANPR_cam3.setObjectName("label_ANPR_cam3")
        self.buttonGroup_anpr_cam3 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_anpr_cam3 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam3)
        self.radioButton_on_anpr_cam3.setGeometry(QtCore.QRect(180, 40, 51, 23))
        self.radioButton_on_anpr_cam3.setChecked(True)
        self.radioButton_on_anpr_cam3.setObjectName("radioButton_on_anpr_cam3")
        self.buttonGroup_anpr_cam3.addButton(self.radioButton_on_anpr_cam3)
        self.radioButton_off_anpr_cam3 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam3)
        self.radioButton_off_anpr_cam3.setGeometry(QtCore.QRect(240, 40, 61, 23))
        self.radioButton_off_anpr_cam3.setObjectName("radioButton_off_anpr_cam3")
        self.buttonGroup_anpr_cam3.setObjectName("buttonGroup_anpr_cam3")
        self.buttonGroup_anpr_cam3.addButton(self.radioButton_off_anpr_cam3)

        #vavc button
        self.label_VAVC_cam3 = QtWidgets.QLabel(self.groupBox_anpr_config_cam3)
        self.label_VAVC_cam3.setGeometry(QtCore.QRect(50, 80, 51, 17))
        self.label_VAVC_cam3.setObjectName("label_VAVC_cam3")
        self.buttonGroup_vavc_cam3 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_vavc_cam3 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam3)
        self.radioButton_on_vavc_cam3.setGeometry(QtCore.QRect(180, 80, 51, 23))
        self.radioButton_on_vavc_cam3.setEnabled(False)
        self.radioButton_on_vavc_cam3.setObjectName("radioButton_on_vavc_cam3")
        self.buttonGroup_vavc_cam3.addButton(self.radioButton_on_vavc_cam3)
        self.radioButton_off_vavc_cam3 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam3)
        self.radioButton_off_vavc_cam3.setGeometry(QtCore.QRect(240, 80, 61, 23))
        self.radioButton_off_vavc_cam3.setChecked(True)
        self.radioButton_off_vavc_cam3.setObjectName("radioButton_off_vavc_cam3")
        self.buttonGroup_vavc_cam3.setObjectName("buttonGroup_vavc_cam3")
        self.buttonGroup_vavc_cam3.addButton(self.radioButton_off_vavc_cam3)

        #mode
        self.label_mode_cam3 = QtWidgets.QLabel(self.groupBox_anpr_config_cam3)
        self.label_mode_cam3.setGeometry(QtCore.QRect(50, 120, 91, 17))
        self.label_mode_cam3.setObjectName("label_mode_cam3")
        self.comboBox_mode_cam3 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam3)
        self.comboBox_mode_cam3.setEnabled(True)
        self.comboBox_mode_cam3.setGeometry(QtCore.QRect(180, 120, 311, 21))
        self.comboBox_mode_cam3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_mode_cam3.setMouseTracking(True)
        self.comboBox_mode_cam3.setWhatsThis("")
        self.comboBox_mode_cam3.setAutoFillBackground(False)
        self.comboBox_mode_cam3.setEditable(False)
        self.comboBox_mode_cam3.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_mode_cam3.setMinimumContentsLength(5)
        self.comboBox_mode_cam3.setObjectName("comboBox_mode_cam3")
        self.comboBox_mode_cam3.addItem("")
        self.comboBox_mode_cam3.addItem("")
        self.comboBox_mode_cam3.addItem("")
        #when select list
        self.comboBox_mode_cam3.currentIndexChanged.connect(self.select_mode2)

        #lane type
        self.label_lane_type_cam3 = QtWidgets.QLabel(self.groupBox_anpr_config_cam3)
        self.label_lane_type_cam3.setGeometry(QtCore.QRect(50, 160, 91, 17))
        self.label_lane_type_cam3.setObjectName("label_lane_type_cam3")
        self.comboBox_lane_type_cam3 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam3)
        self.comboBox_lane_type_cam3.setEnabled(True)
        self.comboBox_lane_type_cam3.setGeometry(QtCore.QRect(180, 160, 311, 21))
        self.comboBox_lane_type_cam3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_lane_type_cam3.setMouseTracking(True)
        self.comboBox_lane_type_cam3.setWhatsThis("")
        self.comboBox_lane_type_cam3.setAutoFillBackground(False)
        self.comboBox_lane_type_cam3.setEditable(False)
        self.comboBox_lane_type_cam3.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_lane_type_cam3.setMinimumContentsLength(5)
        self.comboBox_lane_type_cam3.setObjectName("comboBox_lane_type_cam3")
        self.comboBox_lane_type_cam3.addItem("")
        self.comboBox_lane_type_cam3.addItem("")
        self.comboBox_lane_type_cam3.addItem("")
        self.comboBox_lane_type_cam3.addItem("")
        #when select list
        self.comboBox_lane_type_cam3.currentIndexChanged.connect(self.select_lane_type2)

        #Plaza ID
        self.label_plaza_id_cam3 = QtWidgets.QLabel(self.groupBox_anpr_config_cam3)
        self.label_plaza_id_cam3.setGeometry(QtCore.QRect(50, 200, 67, 17))
        self.label_plaza_id_cam3.setObjectName("label_plaza_id_cam3")
        self.comboBox_plaza_id_cam3 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam3)
        self.comboBox_plaza_id_cam3.setEnabled(True)
        self.comboBox_plaza_id_cam3.setGeometry(QtCore.QRect(180, 200, 311, 21))
        self.comboBox_plaza_id_cam3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_plaza_id_cam3.setMouseTracking(True)
        self.comboBox_plaza_id_cam3.setWhatsThis("")
        self.comboBox_plaza_id_cam3.setAutoFillBackground(False)
        self.comboBox_plaza_id_cam3.setEditable(False)
        self.comboBox_plaza_id_cam3.setMaxVisibleItems(10)
        self.comboBox_plaza_id_cam3.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_plaza_id_cam3.setMinimumContentsLength(5)
        self.comboBox_plaza_id_cam3.setFrame(True)
        self.comboBox_plaza_id_cam3.setObjectName("comboBox_plaza_id_cam3")
        self.comboBox_plaza_id_cam3.addItem("")
        self.comboBox_plaza_id_cam3.addItem("")
        self.comboBox_plaza_id_cam3.addItem("")
        self.comboBox_plaza_id_cam3.addItem("")
        self.comboBox_plaza_id_cam3.addItem("")
        self.comboBox_plaza_id_cam3.addItem("")
        self.comboBox_plaza_id_cam3.addItem("")
        self.comboBox_plaza_id_cam3.addItem("")
        self.comboBox_plaza_id_cam3.addItem("")
        self.comboBox_plaza_id_cam3.addItem("")
        self.comboBox_plaza_id_cam3.addItem("")
        self.comboBox_plaza_id_cam3.addItem("")
        #when select list
        self.comboBox_plaza_id_cam3.currentIndexChanged.connect(self.select_plaza_ID2)

        #Lane ID
        self.label_lane_id_cam3 = QtWidgets.QLabel(self.groupBox_anpr_config_cam3)
        self.label_lane_id_cam3.setGeometry(QtCore.QRect(50, 250, 67, 17))
        self.label_lane_id_cam3.setObjectName("label_lane_id_cam3")
        self.lineEdit_lane_id_cam3 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam3)
        self.lineEdit_lane_id_cam3.setGeometry(QtCore.QRect(180, 240, 380, 31))
        self.lineEdit_lane_id_cam3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_lane_id_cam3.setDragEnabled(False)
        self.lineEdit_lane_id_cam3.setObjectName("lineEdit_lane_id_cam3")
        self.lineEdit_lane_id_cam3.setText(lane_ID2)

        setting_changed_list[39] = lane_ID2
        self.lineEdit_lane_id_cam3.textChanged.connect(self.lane_ID2)

        #rtsp camera
        self.label_rtsp_cam3 = QtWidgets.QLabel(self.groupBox_anpr_config_cam3)
        self.label_rtsp_cam3.setGeometry(QtCore.QRect(50, 300, 81, 17))
        self.label_rtsp_cam3.setObjectName("label_rtsp_cam3")
        self.lineEdit_rtsp_cam3 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam3)
        self.lineEdit_rtsp_cam3.setGeometry(QtCore.QRect(180, 290, 380, 31))
        self.lineEdit_rtsp_cam3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_rtsp_cam3.setDragEnabled(False)
        self.lineEdit_rtsp_cam3.setObjectName("lineEdit_rtsp_cam3")
        self.lineEdit_rtsp_cam3.setText(input_src2)
        self.lineEdit_rtsp_cam3.textChanged.connect(self.rtsp2)
        
        setting_changed_list[23] = input_src2
        self.lineEdit_rtsp_cam3.textChanged.connect(self.rtsp2)

        self.label_1_milesight_18 = QtWidgets.QLabel(self.groupBox_anpr_config_cam3)
        self.label_1_milesight_18.setGeometry(QtCore.QRect(50, 370, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_1_milesight_18.setFont(font)
        self.label_1_milesight_18.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_1_milesight_18.setObjectName("label_1_milesight_18")
        self.label_komoto_18 = QtWidgets.QLabel(self.groupBox_anpr_config_cam3)
        self.label_komoto_18.setGeometry(QtCore.QRect(50, 390, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_komoto_18.setFont(font)
        self.label_komoto_18.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_komoto_18.setObjectName("label_komoto_18")

        self.label_eg_18 = QtWidgets.QLabel(self.groupBox_anpr_config_cam3)
        self.label_eg_18.setGeometry(QtCore.QRect(50, 350, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_eg_18.setFont(font)
        self.label_eg_18.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_eg_18.setObjectName("label_eg_18")
        self.tabWidget_camera_tab.addTab(self.tab_cam3, "")



        #---------------------------------------------------------------------------------------------
        # tab cam 4
        self.tab_cam4 = QtWidgets.QWidget()
        self.tab_cam4.setObjectName("tab_cam4")
        self.groupBox_anpr_config_cam4 = QtWidgets.QGroupBox(self.tab_cam4)
        self.groupBox_anpr_config_cam4.setGeometry(QtCore.QRect(20, 20, 611, 431))
        self.groupBox_anpr_config_cam4.setObjectName("groupBox_anpr_config_cam4")
        
        #anpr button
        self.label_ANPR_cam4 = QtWidgets.QLabel(self.groupBox_anpr_config_cam4)
        self.label_ANPR_cam4.setGeometry(QtCore.QRect(50, 40, 51, 17))
        self.label_ANPR_cam4.setObjectName("label_ANPR_cam4")
        self.buttonGroup_anpr_cam4 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_anpr_cam4 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam4)
        self.radioButton_on_anpr_cam4.setGeometry(QtCore.QRect(180, 40, 51, 23))
        self.radioButton_on_anpr_cam4.setChecked(True)
        self.radioButton_on_anpr_cam4.setObjectName("radioButton_on_anpr_cam4")
        self.radioButton_off_anpr_cam4 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam4)
        self.radioButton_off_anpr_cam4.setGeometry(QtCore.QRect(240, 40, 61, 23))
        self.radioButton_off_anpr_cam4.setObjectName("radioButton_off_anpr_cam4")
        self.buttonGroup_anpr_cam4.setObjectName("buttonGroup_anpr_cam4")
        self.buttonGroup_anpr_cam4.addButton(self.radioButton_off_anpr_cam4)
        self.buttonGroup_anpr_cam4.addButton(self.radioButton_on_anpr_cam4)
        
        #vavc button
        self.label_VAVC_cam4 = QtWidgets.QLabel(self.groupBox_anpr_config_cam4)
        self.label_VAVC_cam4.setGeometry(QtCore.QRect(50, 80, 51, 17))
        self.label_VAVC_cam4.setObjectName("label_VAVC_cam4")
        self.buttonGroup_vavc_cam4 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_vavc_cam4 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam4)
        self.radioButton_on_vavc_cam4.setGeometry(QtCore.QRect(180, 80, 51, 23))
        self.radioButton_on_vavc_cam4.setEnabled(False)
        self.radioButton_on_vavc_cam4.setObjectName("radioButton_on_vavc_cam4")
        self.buttonGroup_vavc_cam4.addButton(self.radioButton_on_vavc_cam4)
        self.radioButton_off_vavc_cam4 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam4)
        self.radioButton_off_vavc_cam4.setGeometry(QtCore.QRect(240, 80, 61, 23))
        self.radioButton_off_vavc_cam4.setChecked(True)
        self.radioButton_off_vavc_cam4.setObjectName("radioButton_off_vavc_cam4")
        self.buttonGroup_vavc_cam4.setObjectName("buttonGroup_vavc_cam4")
        self.buttonGroup_vavc_cam4.addButton(self.radioButton_off_vavc_cam4)
        
        #mode
        self.label_mode_cam4 = QtWidgets.QLabel(self.groupBox_anpr_config_cam4)
        self.label_mode_cam4.setGeometry(QtCore.QRect(50, 120, 91, 17))
        self.label_mode_cam4.setObjectName("label_mode_cam4")
        self.comboBox_mode_cam4 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam4)
        self.comboBox_mode_cam4.setEnabled(True)
        self.comboBox_mode_cam4.setGeometry(QtCore.QRect(180, 120, 311, 21))
        self.comboBox_mode_cam4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_mode_cam4.setMouseTracking(True)
        self.comboBox_mode_cam4.setWhatsThis("")
        self.comboBox_mode_cam4.setAutoFillBackground(False)
        self.comboBox_mode_cam4.setEditable(False)
        self.comboBox_mode_cam4.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_mode_cam4.setMinimumContentsLength(5)
        self.comboBox_mode_cam4.setObjectName("comboBox_mode_cam4")
        self.comboBox_mode_cam4.addItem("")
        self.comboBox_mode_cam4.addItem("")
        self.comboBox_mode_cam4.addItem("")
        #when select list
        self.comboBox_mode_cam4.currentIndexChanged.connect(self.select_mode3)     
        
        #lane type
        self.label_lane_type_cam4 = QtWidgets.QLabel(self.groupBox_anpr_config_cam4)
        self.label_lane_type_cam4.setGeometry(QtCore.QRect(50, 160, 91, 17))
        self.label_lane_type_cam4.setObjectName("label_lane_type_cam4")
        self.comboBox_lane_type_cam4 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam4)
        self.comboBox_lane_type_cam4.setEnabled(True)
        self.comboBox_lane_type_cam4.setGeometry(QtCore.QRect(180, 160, 311, 21))
        self.comboBox_lane_type_cam4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_lane_type_cam4.setMouseTracking(True)
        self.comboBox_lane_type_cam4.setWhatsThis("")
        self.comboBox_lane_type_cam4.setAutoFillBackground(False)
        self.comboBox_lane_type_cam4.setEditable(False)
        self.comboBox_lane_type_cam4.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_lane_type_cam4.setMinimumContentsLength(5)
        self.comboBox_lane_type_cam4.setObjectName("comboBox_lane_type_cam4")
        self.comboBox_lane_type_cam4.addItem("")
        self.comboBox_lane_type_cam4.addItem("")
        self.comboBox_lane_type_cam4.addItem("")
        self.comboBox_lane_type_cam4.addItem("")
        #when select list
        self.comboBox_lane_type_cam4.currentIndexChanged.connect(self.select_lane_type3)
        
        #Plaza ID
        self.label_plaza_id_cam4 = QtWidgets.QLabel(self.groupBox_anpr_config_cam4)
        self.label_plaza_id_cam4.setGeometry(QtCore.QRect(50, 200, 67, 17))
        self.label_plaza_id_cam4.setObjectName("label_plaza_id_cam4")
        self.comboBox_plaza_id_cam4 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam4)
        self.comboBox_plaza_id_cam4.setEnabled(True)
        self.comboBox_plaza_id_cam4.setGeometry(QtCore.QRect(180, 200, 311, 21))
        self.comboBox_plaza_id_cam4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_plaza_id_cam4.setMouseTracking(True)
        self.comboBox_plaza_id_cam4.setWhatsThis("")
        self.comboBox_plaza_id_cam4.setAutoFillBackground(False)
        self.comboBox_plaza_id_cam4.setEditable(False)
        self.comboBox_plaza_id_cam4.setMaxVisibleItems(10)
        self.comboBox_plaza_id_cam4.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_plaza_id_cam4.setMinimumContentsLength(5)
        self.comboBox_plaza_id_cam4.setFrame(True)
        self.comboBox_plaza_id_cam4.setObjectName("comboBox_plaza_id_cam4")
        self.comboBox_plaza_id_cam4.addItem("")
        self.comboBox_plaza_id_cam4.addItem("")
        self.comboBox_plaza_id_cam4.addItem("")
        self.comboBox_plaza_id_cam4.addItem("")
        self.comboBox_plaza_id_cam4.addItem("")
        self.comboBox_plaza_id_cam4.addItem("")
        self.comboBox_plaza_id_cam4.addItem("")
        self.comboBox_plaza_id_cam4.addItem("")
        self.comboBox_plaza_id_cam4.addItem("")
        self.comboBox_plaza_id_cam4.addItem("")
        self.comboBox_plaza_id_cam4.addItem("")
        self.comboBox_plaza_id_cam4.addItem("")
        #when select list
        self.comboBox_plaza_id_cam4.currentIndexChanged.connect(self.select_plaza_ID3)
        
        #Lane ID
        self.label_lane_id_cam4 = QtWidgets.QLabel(self.groupBox_anpr_config_cam4)
        self.label_lane_id_cam4.setGeometry(QtCore.QRect(50, 250, 67, 17))
        self.label_lane_id_cam4.setObjectName("label_lane_id_cam4")
        self.lineEdit_lane_id_cam4 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam4)
        self.lineEdit_lane_id_cam4.setGeometry(QtCore.QRect(180, 240, 380, 31))
        self.lineEdit_lane_id_cam4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_lane_id_cam4.setDragEnabled(False)
        self.lineEdit_lane_id_cam4.setObjectName("lineEdit_lane_id_cam4")
        self.lineEdit_lane_id_cam4.setText(lane_ID3)

        setting_changed_list[40] = lane_ID3
        self.lineEdit_lane_id_cam4.textChanged.connect(self.lane_ID3)
        
        #rtsp camera
        self.label_rtsp_cam4 = QtWidgets.QLabel(self.groupBox_anpr_config_cam4)
        self.label_rtsp_cam4.setGeometry(QtCore.QRect(50, 300, 81, 17))
        self.label_rtsp_cam4.setObjectName("label_rtsp_cam4")
        self.lineEdit_rtsp_cam4 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam4)
        self.lineEdit_rtsp_cam4.setGeometry(QtCore.QRect(180, 290, 380, 31))
        self.lineEdit_rtsp_cam4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_rtsp_cam4.setDragEnabled(False)
        self.lineEdit_rtsp_cam4.setObjectName("lineEdit_rtsp_cam4")
        self.lineEdit_rtsp_cam4.setText(input_src3)
        self.lineEdit_rtsp_cam4.textChanged.connect(self.rtsp3)
        
        setting_changed_list[24] = input_src3
        self.lineEdit_rtsp_cam4.textChanged.connect(self.rtsp4)
        
        
        self.label_1_milesight_20 = QtWidgets.QLabel(self.groupBox_anpr_config_cam4)
        self.label_1_milesight_20.setGeometry(QtCore.QRect(50, 370, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_1_milesight_20.setFont(font)
        self.label_1_milesight_20.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_1_milesight_20.setObjectName("label_1_milesight_20")
        self.label_komoto_20 = QtWidgets.QLabel(self.groupBox_anpr_config_cam4)
        self.label_komoto_20.setGeometry(QtCore.QRect(50, 390, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_komoto_20.setFont(font)
        self.label_komoto_20.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_komoto_20.setObjectName("label_komoto_20")

        self.label_eg_20 = QtWidgets.QLabel(self.groupBox_anpr_config_cam4)
        self.label_eg_20.setGeometry(QtCore.QRect(50, 350, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_eg_20.setFont(font)
        self.label_eg_20.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_eg_20.setObjectName("label_eg_20")

        self.frame_cam4 = QtWidgets.QFrame(self.tab_cam4)
        self.frame_cam4.setGeometry(QtCore.QRect(-10, -10, 651, 521))
        self.frame_cam4.setAutoFillBackground(True)
        self.frame_cam4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_cam4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_cam4.setObjectName("frame_cam4")
        self.frame_cam4.raise_()
        self.groupBox_anpr_config_cam4.raise_()
        self.tabWidget_camera_tab.addTab(self.tab_cam4, "")     

        #-----------------------------------------------------------------------------------------
        
        # tab cam 5
        self.tab_cam5 = QtWidgets.QWidget()
        self.tab_cam5.setObjectName("tab_cam5")
        self.groupBox_anpr_config_cam5 = QtWidgets.QGroupBox(self.tab_cam5)
        self.groupBox_anpr_config_cam5.setGeometry(QtCore.QRect(20, 20, 611, 431))
        self.groupBox_anpr_config_cam5.setObjectName("groupBox_anpr_config_cam5")

        #anpr button
        self.label_ANPR_cam5 = QtWidgets.QLabel(self.groupBox_anpr_config_cam5)
        self.label_ANPR_cam5.setGeometry(QtCore.QRect(50, 40, 51, 17))
        self.label_ANPR_cam5.setObjectName("label_ANPR_cam5")
        self.buttonGroup_anpr_cam5 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_anpr_cam5 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam5)
        self.radioButton_on_anpr_cam5.setGeometry(QtCore.QRect(180, 40, 51, 23))
        self.radioButton_on_anpr_cam5.setChecked(True)
        self.radioButton_on_anpr_cam5.setObjectName("radioButton_on_anpr_cam5")
        self.buttonGroup_anpr_cam5.addButton(self.radioButton_on_anpr_cam5)
        self.radioButton_off_anpr_cam5 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam5)
        self.radioButton_off_anpr_cam5.setGeometry(QtCore.QRect(240, 40, 61, 23))
        self.radioButton_off_anpr_cam5.setObjectName("radioButton_off_anpr_cam5")
        self.buttonGroup_anpr_cam5.setObjectName("buttonGroup_anpr_cam5")
        self.buttonGroup_anpr_cam5.addButton(self.radioButton_off_anpr_cam5)

        #vavc button
        self.label_VAVC_cam5 = QtWidgets.QLabel(self.groupBox_anpr_config_cam5)
        self.label_VAVC_cam5.setGeometry(QtCore.QRect(50, 80, 51, 17))
        self.label_VAVC_cam5.setObjectName("label_VAVC_cam5")
        self.buttonGroup_vavc_cam5 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_vavc_cam5 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam5)
        self.radioButton_on_vavc_cam5.setGeometry(QtCore.QRect(180, 80, 51, 23))
        self.radioButton_on_vavc_cam5.setEnabled(False)
        self.radioButton_on_vavc_cam5.setObjectName("radioButton_on_vavc_cam5")
        self.buttonGroup_vavc_cam5.addButton(self.radioButton_on_vavc_cam5)
        self.radioButton_off_vavc_cam5 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam5)
        self.radioButton_off_vavc_cam5.setGeometry(QtCore.QRect(240, 80, 61, 23))
        self.radioButton_off_vavc_cam5.setChecked(True)
        self.radioButton_off_vavc_cam5.setObjectName("radioButton_off_vavc_cam5")
        self.buttonGroup_vavc_cam5.setObjectName("buttonGroup_vavc_cam5")
        self.buttonGroup_vavc_cam5.addButton(self.radioButton_off_vavc_cam5)

        #mode
        self.label_mode_cam5 = QtWidgets.QLabel(self.groupBox_anpr_config_cam5)
        self.label_mode_cam5.setGeometry(QtCore.QRect(50, 120, 91, 17))
        self.label_mode_cam5.setObjectName("label_mode_cam5")
        self.comboBox_mode_cam5 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam5)
        self.comboBox_mode_cam5.setEnabled(True)
        self.comboBox_mode_cam5.setGeometry(QtCore.QRect(180, 120, 311, 21))
        self.comboBox_mode_cam5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_mode_cam5.setMouseTracking(True)
        self.comboBox_mode_cam5.setWhatsThis("")
        self.comboBox_mode_cam5.setAutoFillBackground(False)
        self.comboBox_mode_cam5.setEditable(False)
        self.comboBox_mode_cam5.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_mode_cam5.setMinimumContentsLength(5)
        self.comboBox_mode_cam5.setObjectName("comboBox_mode_cam5")
        self.comboBox_mode_cam5.addItem("")
        self.comboBox_mode_cam5.addItem("")
        self.comboBox_mode_cam5.addItem("")
        #when select list
        self.comboBox_mode_cam5.currentIndexChanged.connect(self.select_mode4)

        #lane type
        self.label_lane_type_cam5 = QtWidgets.QLabel(self.groupBox_anpr_config_cam5)
        self.label_lane_type_cam5.setGeometry(QtCore.QRect(50, 160, 91, 17))
        self.label_lane_type_cam5.setObjectName("label_lane_type_cam5")
        self.comboBox_lane_type_cam5 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam5)
        self.comboBox_lane_type_cam5.setEnabled(True)
        self.comboBox_lane_type_cam5.setGeometry(QtCore.QRect(180, 160, 311, 21))
        self.comboBox_lane_type_cam5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_lane_type_cam5.setMouseTracking(True)
        self.comboBox_lane_type_cam5.setWhatsThis("")
        self.comboBox_lane_type_cam5.setAutoFillBackground(False)
        self.comboBox_lane_type_cam5.setEditable(False)
        self.comboBox_lane_type_cam5.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_lane_type_cam5.setMinimumContentsLength(5)
        self.comboBox_lane_type_cam5.setObjectName("comboBox_lane_type_cam5")
        self.comboBox_lane_type_cam5.addItem("")
        self.comboBox_lane_type_cam5.addItem("")
        self.comboBox_lane_type_cam5.addItem("")
        self.comboBox_lane_type_cam5.addItem("")
        #when select list
        self.comboBox_lane_type_cam5.currentIndexChanged.connect(self.select_lane_type4)

        #Plaza ID
        self.label_plaza_id_cam5 = QtWidgets.QLabel(self.groupBox_anpr_config_cam5)
        self.label_plaza_id_cam5.setGeometry(QtCore.QRect(50, 200, 67, 17))
        self.label_plaza_id_cam5.setObjectName("label_plaza_id_cam5")
        self.comboBox_plaza_id_cam5 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam5)
        self.comboBox_plaza_id_cam5.setEnabled(True)
        self.comboBox_plaza_id_cam5.setGeometry(QtCore.QRect(180, 200, 311, 21))
        self.comboBox_plaza_id_cam5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_plaza_id_cam5.setMouseTracking(True)
        self.comboBox_plaza_id_cam5.setWhatsThis("")
        self.comboBox_plaza_id_cam5.setAutoFillBackground(False)
        self.comboBox_plaza_id_cam5.setEditable(False)
        self.comboBox_plaza_id_cam5.setMaxVisibleItems(10)
        self.comboBox_plaza_id_cam5.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_plaza_id_cam5.setMinimumContentsLength(5)
        self.comboBox_plaza_id_cam5.setFrame(True)
        self.comboBox_plaza_id_cam5.setObjectName("comboBox_plaza_id_cam5")
        self.comboBox_plaza_id_cam5.addItem("")
        self.comboBox_plaza_id_cam5.addItem("")
        self.comboBox_plaza_id_cam5.addItem("")
        self.comboBox_plaza_id_cam5.addItem("")
        self.comboBox_plaza_id_cam5.addItem("")
        self.comboBox_plaza_id_cam5.addItem("")
        self.comboBox_plaza_id_cam5.addItem("")
        self.comboBox_plaza_id_cam5.addItem("")
        self.comboBox_plaza_id_cam5.addItem("")
        self.comboBox_plaza_id_cam5.addItem("")
        self.comboBox_plaza_id_cam5.addItem("")
        self.comboBox_plaza_id_cam5.addItem("")
        #when select list
        self.comboBox_plaza_id_cam5.currentIndexChanged.connect(self.select_plaza_ID4)

        #Lane ID
        self.label_lane_id_cam5 = QtWidgets.QLabel(self.groupBox_anpr_config_cam5)
        self.label_lane_id_cam5.setGeometry(QtCore.QRect(50, 250, 67, 17))
        self.label_lane_id_cam5.setObjectName("label_lane_id_cam5")
        self.lineEdit_lane_id_cam5 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam5)
        self.lineEdit_lane_id_cam5.setGeometry(QtCore.QRect(180, 240, 380, 31))
        self.lineEdit_lane_id_cam5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_lane_id_cam5.setDragEnabled(False)
        self.lineEdit_lane_id_cam5.setObjectName("lineEdit_lane_id_cam5")
        self.lineEdit_lane_id_cam5.setText(lane_ID4)

        setting_changed_list[41] = lane_ID4
        self.lineEdit_lane_id_cam5.textChanged.connect(self.lane_ID4)

        #rtsp camera
        self.label_rtsp_cam5 = QtWidgets.QLabel(self.groupBox_anpr_config_cam5)
        self.label_rtsp_cam5.setGeometry(QtCore.QRect(50, 300, 81, 17))
        self.label_rtsp_cam5.setObjectName("label_rtsp_cam5")
        self.lineEdit_rtsp_cam5 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam5)
        self.lineEdit_rtsp_cam5.setGeometry(QtCore.QRect(180, 290, 380, 31))
        self.lineEdit_rtsp_cam5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_rtsp_cam5.setDragEnabled(False)
        self.lineEdit_rtsp_cam5.setObjectName("lineEdit_rtsp_cam5")
        self.lineEdit_rtsp_cam5.setText(input_src4)
        self.lineEdit_rtsp_cam5.textChanged.connect(self.rtsp4)
        
        setting_changed_list[25] = input_src4
        self.lineEdit_rtsp_cam5.textChanged.connect(self.rtsp4)


        self.label_1_milesight_21 = QtWidgets.QLabel(self.groupBox_anpr_config_cam5)
        self.label_1_milesight_21.setGeometry(QtCore.QRect(50, 370, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_1_milesight_21.setFont(font)
        self.label_1_milesight_21.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_1_milesight_21.setObjectName("label_1_milesight_21")
        self.label_komoto_21 = QtWidgets.QLabel(self.groupBox_anpr_config_cam5)
        self.label_komoto_21.setGeometry(QtCore.QRect(50, 390, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_komoto_21.setFont(font)
        self.label_komoto_21.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_komoto_21.setObjectName("label_komoto_21")

        self.label_eg_21 = QtWidgets.QLabel(self.groupBox_anpr_config_cam5)
        self.label_eg_21.setGeometry(QtCore.QRect(50, 350, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_eg_21.setFont(font)
        self.label_eg_21.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_eg_21.setObjectName("label_eg_21")
        self.tabWidget_camera_tab.addTab(self.tab_cam5, "")


        #-----------------------------------------------------------------------
        
        # tab cam 6
        self.tab_cam6 = QtWidgets.QWidget()
        self.tab_cam6.setObjectName("tab_cam6")
        self.groupBox_anpr_config_cam6 = QtWidgets.QGroupBox(self.tab_cam6)
        self.groupBox_anpr_config_cam6.setGeometry(QtCore.QRect(20, 20, 611, 431))
        self.groupBox_anpr_config_cam6.setObjectName("groupBox_anpr_config_cam6")

        #anpr button
        self.label_ANPR_cam6 = QtWidgets.QLabel(self.groupBox_anpr_config_cam6)
        self.label_ANPR_cam6.setGeometry(QtCore.QRect(50, 40, 51, 17))
        self.label_ANPR_cam6.setObjectName("label_ANPR_cam6")
        self.buttonGroup_anpr_cam6 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_anpr_cam6 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam6)
        self.radioButton_on_anpr_cam6.setGeometry(QtCore.QRect(180, 40, 51, 23))
        self.radioButton_on_anpr_cam6.setChecked(True)
        self.radioButton_on_anpr_cam6.setObjectName("radioButton_on_anpr_cam6")
        self.buttonGroup_anpr_cam6.addButton(self.radioButton_on_anpr_cam6)
        self.radioButton_off_anpr_cam6 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam6)
        self.radioButton_off_anpr_cam6.setGeometry(QtCore.QRect(240, 40, 61, 23))
        self.radioButton_off_anpr_cam6.setObjectName("radioButton_off_anpr_cam6")
        self.buttonGroup_anpr_cam6.setObjectName("buttonGroup_anpr_cam6")
        self.buttonGroup_anpr_cam6.addButton(self.radioButton_off_anpr_cam6)

        #vavc button
        self.label_VAVC_cam6 = QtWidgets.QLabel(self.groupBox_anpr_config_cam6)
        self.label_VAVC_cam6.setGeometry(QtCore.QRect(50, 80, 51, 17))
        self.label_VAVC_cam6.setObjectName("label_VAVC_cam6")
        self.buttonGroup_vavc_cam6 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_vavc_cam6 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam6)
        self.radioButton_on_vavc_cam6.setGeometry(QtCore.QRect(180, 80, 51, 23))
        self.radioButton_on_vavc_cam6.setEnabled(False)
        self.radioButton_on_vavc_cam6.setObjectName("radioButton_on_vavc_cam6")
        self.buttonGroup_vavc_cam6.addButton(self.radioButton_on_vavc_cam6)
        self.radioButton_off_vavc_cam6 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam6)
        self.radioButton_off_vavc_cam6.setGeometry(QtCore.QRect(240, 80, 61, 23))
        self.radioButton_off_vavc_cam6.setChecked(True)
        self.radioButton_off_vavc_cam6.setObjectName("radioButton_off_vavc_cam6")
        self.buttonGroup_vavc_cam6.setObjectName("buttonGroup_vavc_cam6")
        self.buttonGroup_vavc_cam6.addButton(self.radioButton_off_vavc_cam6)

        #mode
        self.label_mode_cam6 = QtWidgets.QLabel(self.groupBox_anpr_config_cam6)
        self.label_mode_cam6.setGeometry(QtCore.QRect(50, 120, 91, 17))
        self.label_mode_cam6.setObjectName("label_mode_cam6")
        self.comboBox_mode_cam6 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam6)
        self.comboBox_mode_cam6.setEnabled(True)
        self.comboBox_mode_cam6.setGeometry(QtCore.QRect(180, 120, 311, 21))
        self.comboBox_mode_cam6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_mode_cam6.setMouseTracking(True)
        self.comboBox_mode_cam6.setWhatsThis("")
        self.comboBox_mode_cam6.setAutoFillBackground(False)
        self.comboBox_mode_cam6.setEditable(False)
        self.comboBox_mode_cam6.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_mode_cam6.setMinimumContentsLength(5)
        self.comboBox_mode_cam6.setObjectName("comboBox_mode_cam6")
        self.comboBox_mode_cam6.addItem("")
        self.comboBox_mode_cam6.addItem("")
        self.comboBox_mode_cam6.addItem("")
        #when select list
        self.comboBox_mode_cam6.currentIndexChanged.connect(self.select_mode5)

        #lane type
        self.label_lane_type_cam6 = QtWidgets.QLabel(self.groupBox_anpr_config_cam6)
        self.label_lane_type_cam6.setGeometry(QtCore.QRect(50, 160, 91, 17))
        self.label_lane_type_cam6.setObjectName("label_lane_type_cam6")
        self.comboBox_lane_type_cam6 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam6)
        self.comboBox_lane_type_cam6.setEnabled(True)
        self.comboBox_lane_type_cam6.setGeometry(QtCore.QRect(180, 160, 311, 21))
        self.comboBox_lane_type_cam6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_lane_type_cam6.setMouseTracking(True)
        self.comboBox_lane_type_cam6.setWhatsThis("")
        self.comboBox_lane_type_cam6.setAutoFillBackground(False)
        self.comboBox_lane_type_cam6.setEditable(False)
        self.comboBox_lane_type_cam6.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_lane_type_cam6.setMinimumContentsLength(5)
        self.comboBox_lane_type_cam6.setObjectName("comboBox_lane_type_cam6")
        self.comboBox_lane_type_cam6.addItem("")
        self.comboBox_lane_type_cam6.addItem("")
        self.comboBox_lane_type_cam6.addItem("")
        self.comboBox_lane_type_cam6.addItem("")
        #when select list
        self.comboBox_lane_type_cam6.currentIndexChanged.connect(self.select_lane_type5)

        #Plaza ID
        self.label_plaza_id_cam6 = QtWidgets.QLabel(self.groupBox_anpr_config_cam6)
        self.label_plaza_id_cam6.setGeometry(QtCore.QRect(50, 200, 67, 17))
        self.label_plaza_id_cam6.setObjectName("label_plaza_id_cam6")
        self.comboBox_plaza_id_cam6 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam6)
        self.comboBox_plaza_id_cam6.setEnabled(True)
        self.comboBox_plaza_id_cam6.setGeometry(QtCore.QRect(180, 200, 311, 21))
        self.comboBox_plaza_id_cam6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_plaza_id_cam6.setMouseTracking(True)
        self.comboBox_plaza_id_cam6.setWhatsThis("")
        self.comboBox_plaza_id_cam6.setAutoFillBackground(False)
        self.comboBox_plaza_id_cam6.setEditable(False)
        self.comboBox_plaza_id_cam6.setMaxVisibleItems(10)
        self.comboBox_plaza_id_cam6.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_plaza_id_cam6.setMinimumContentsLength(5)
        self.comboBox_plaza_id_cam6.setFrame(True)
        self.comboBox_plaza_id_cam6.setObjectName("comboBox_plaza_id_cam6")
        self.comboBox_plaza_id_cam6.addItem("")
        self.comboBox_plaza_id_cam6.addItem("")
        self.comboBox_plaza_id_cam6.addItem("")
        self.comboBox_plaza_id_cam6.addItem("")
        self.comboBox_plaza_id_cam6.addItem("")
        self.comboBox_plaza_id_cam6.addItem("")
        self.comboBox_plaza_id_cam6.addItem("")
        self.comboBox_plaza_id_cam6.addItem("")
        self.comboBox_plaza_id_cam6.addItem("")
        self.comboBox_plaza_id_cam6.addItem("")
        self.comboBox_plaza_id_cam6.addItem("")
        self.comboBox_plaza_id_cam6.addItem("")
        #when select list
        self.comboBox_plaza_id_cam6.currentIndexChanged.connect(self.select_plaza_ID5)

        #Lane ID
        self.label_lane_id_cam6 = QtWidgets.QLabel(self.groupBox_anpr_config_cam6)
        self.label_lane_id_cam6.setGeometry(QtCore.QRect(50, 250, 67, 17))
        self.label_lane_id_cam6.setObjectName("label_lane_id_cam6")
        self.lineEdit_lane_id_cam6 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam6)
        self.lineEdit_lane_id_cam6.setGeometry(QtCore.QRect(180, 240, 380, 31))
        self.lineEdit_lane_id_cam6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_lane_id_cam6.setDragEnabled(False)
        self.lineEdit_lane_id_cam6.setObjectName("lineEdit_lane_id_cam6")
        self.lineEdit_lane_id_cam6.setText(lane_ID5)

        setting_changed_list[42] = lane_ID5
        self.lineEdit_lane_id_cam6.textChanged.connect(self.lane_ID5)

        #rtsp camera
        self.label_rtsp_cam6 = QtWidgets.QLabel(self.groupBox_anpr_config_cam6)
        self.label_rtsp_cam6.setGeometry(QtCore.QRect(50, 300, 81, 17))
        self.label_rtsp_cam6.setObjectName("label_rtsp_cam6")
        self.lineEdit_rtsp_cam6 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam6)
        self.lineEdit_rtsp_cam6.setGeometry(QtCore.QRect(180, 290, 380, 31))
        self.lineEdit_rtsp_cam6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_rtsp_cam6.setDragEnabled(False)
        self.lineEdit_rtsp_cam6.setObjectName("lineEdit_rtsp_cam6")
        self.lineEdit_rtsp_cam6.setText(input_src5)
        self.lineEdit_rtsp_cam6.textChanged.connect(self.rtsp5)
        
        setting_changed_list[26] = input_src5
        self.lineEdit_rtsp_cam6.textChanged.connect(self.rtsp5)


        self.label_1_milesight_22 = QtWidgets.QLabel(self.groupBox_anpr_config_cam6)
        self.label_1_milesight_22.setGeometry(QtCore.QRect(50, 370, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_1_milesight_22.setFont(font)
        self.label_1_milesight_22.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_1_milesight_22.setObjectName("label_1_milesight_22")
        self.label_komoto_22 = QtWidgets.QLabel(self.groupBox_anpr_config_cam6)
        self.label_komoto_22.setGeometry(QtCore.QRect(50, 390, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_komoto_22.setFont(font)
        self.label_komoto_22.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_komoto_22.setObjectName("label_komoto_22")

        self.label_eg_22 = QtWidgets.QLabel(self.groupBox_anpr_config_cam6)
        self.label_eg_22.setGeometry(QtCore.QRect(50, 350, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_eg_22.setFont(font)
        self.label_eg_22.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_eg_22.setObjectName("label_eg_22")
        self.frame = QtWidgets.QFrame(self.tab_cam6)

        #--------------------------------------------------------------------
        # tab cam 7
        self.tab_cam7 = QtWidgets.QWidget()
        self.tab_cam7.setObjectName("tab_cam7")
        self.groupBox_anpr_config_cam7 = QtWidgets.QGroupBox(self.tab_cam7)
        self.groupBox_anpr_config_cam7.setGeometry(QtCore.QRect(20, 20, 611, 431))
        self.groupBox_anpr_config_cam7.setObjectName("groupBox_anpr_config_cam7")
        
        #anpr button
        self.label_ANPR_cam7 = QtWidgets.QLabel(self.groupBox_anpr_config_cam7)
        self.label_ANPR_cam7.setGeometry(QtCore.QRect(50, 40, 51, 17))
        self.label_ANPR_cam7.setObjectName("label_ANPR_cam7")
        self.buttonGroup_anpr_cam7 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_anpr_cam7 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam7)
        self.radioButton_on_anpr_cam7.setGeometry(QtCore.QRect(180, 40, 51, 23))
        self.radioButton_on_anpr_cam7.setChecked(True)
        self.radioButton_on_anpr_cam7.setObjectName("radioButton_on_anpr_cam7")
        self.buttonGroup_anpr_cam7.addButton(self.radioButton_on_anpr_cam7)
        self.radioButton_off_anpr_cam7 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam7)
        self.radioButton_off_anpr_cam7.setGeometry(QtCore.QRect(240, 40, 61, 23))
        self.radioButton_off_anpr_cam7.setObjectName("radioButton_off_anpr_cam7")
        self.buttonGroup_anpr_cam7.setObjectName("buttonGroup_anpr_cam7")
        self.buttonGroup_anpr_cam7.addButton(self.radioButton_off_anpr_cam7)
        
        #vavc button
        self.label_VAVC_cam7 = QtWidgets.QLabel(self.groupBox_anpr_config_cam7)
        self.label_VAVC_cam7.setGeometry(QtCore.QRect(50, 80, 51, 17))
        self.label_VAVC_cam7.setObjectName("label_VAVC_cam7")
        self.buttonGroup_vavc_cam7 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_vavc_cam7 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam7)
        self.radioButton_on_vavc_cam7.setGeometry(QtCore.QRect(180, 80, 51, 23))
        self.radioButton_on_vavc_cam7.setEnabled(False)
        self.radioButton_on_vavc_cam7.setObjectName("radioButton_on_vavc_cam7")
        self.buttonGroup_vavc_cam7.addButton(self.radioButton_on_vavc_cam7)
        self.radioButton_off_vavc_cam7 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam7)
        self.radioButton_off_vavc_cam7.setGeometry(QtCore.QRect(240, 80, 61, 23))
        self.radioButton_off_vavc_cam7.setChecked(True)
        self.radioButton_off_vavc_cam7.setObjectName("radioButton_off_vavc_cam7")
        self.buttonGroup_vavc_cam7.setObjectName("buttonGroup_vavc_cam7")
        self.buttonGroup_vavc_cam7.addButton(self.radioButton_off_vavc_cam7)
        
        #mode
        self.label_mode_cam7 = QtWidgets.QLabel(self.groupBox_anpr_config_cam7)
        self.label_mode_cam7.setGeometry(QtCore.QRect(50, 120, 91, 17))
        self.label_mode_cam7.setObjectName("label_mode_cam7")
        self.comboBox_mode_cam7 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam7)
        self.comboBox_mode_cam7.setEnabled(True)
        self.comboBox_mode_cam7.setGeometry(QtCore.QRect(180, 120, 311, 21))
        self.comboBox_mode_cam7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_mode_cam7.setMouseTracking(True)
        self.comboBox_mode_cam7.setWhatsThis("")
        self.comboBox_mode_cam7.setAutoFillBackground(False)
        self.comboBox_mode_cam7.setEditable(False)
        self.comboBox_mode_cam7.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_mode_cam7.setMinimumContentsLength(5)
        self.comboBox_mode_cam7.setObjectName("comboBox_mode_cam7")
        self.comboBox_mode_cam7.addItem("")
        self.comboBox_mode_cam7.addItem("")
        self.comboBox_mode_cam7.addItem("")
        #when select list
        self.comboBox_mode_cam7.currentIndexChanged.connect(self.select_mode6)
        
        #lane type
        self.label_lane_type_cam7 = QtWidgets.QLabel(self.groupBox_anpr_config_cam7)
        self.label_lane_type_cam7.setGeometry(QtCore.QRect(50, 160, 91, 17))
        self.label_lane_type_cam7.setObjectName("label_lane_type_cam7")
        self.comboBox_lane_type_cam7 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam7)
        self.comboBox_lane_type_cam7.setEnabled(True)
        self.comboBox_lane_type_cam7.setGeometry(QtCore.QRect(180, 160, 311, 21))
        self.comboBox_lane_type_cam7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_lane_type_cam7.setMouseTracking(True)
        self.comboBox_lane_type_cam7.setWhatsThis("")
        self.comboBox_lane_type_cam7.setAutoFillBackground(False)
        self.comboBox_lane_type_cam7.setEditable(False)
        self.comboBox_lane_type_cam7.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_lane_type_cam7.setMinimumContentsLength(5)
        self.comboBox_lane_type_cam7.setObjectName("comboBox_lane_type_cam7")
        self.comboBox_lane_type_cam7.addItem("")
        self.comboBox_lane_type_cam7.addItem("")
        self.comboBox_lane_type_cam7.addItem("")
        self.comboBox_lane_type_cam7.addItem("")
        #when select list
        self.comboBox_lane_type_cam7.currentIndexChanged.connect(self.select_lane_type6)
        
        #Plaza ID
        self.label_plaza_id_cam7 = QtWidgets.QLabel(self.groupBox_anpr_config_cam7)
        self.label_plaza_id_cam7.setGeometry(QtCore.QRect(50, 200, 67, 17))
        self.label_plaza_id_cam7.setObjectName("label_plaza_id_cam7")
        self.comboBox_plaza_id_cam7 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam7)
        self.comboBox_plaza_id_cam7.setEnabled(True)
        self.comboBox_plaza_id_cam7.setGeometry(QtCore.QRect(180, 200, 311, 21))
        self.comboBox_plaza_id_cam7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_plaza_id_cam7.setMouseTracking(True)
        self.comboBox_plaza_id_cam7.setWhatsThis("")
        self.comboBox_plaza_id_cam7.setAutoFillBackground(False)
        self.comboBox_plaza_id_cam7.setEditable(False)
        self.comboBox_plaza_id_cam7.setMaxVisibleItems(10)
        self.comboBox_plaza_id_cam7.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_plaza_id_cam7.setMinimumContentsLength(5)
        self.comboBox_plaza_id_cam7.setFrame(True)
        self.comboBox_plaza_id_cam7.setObjectName("comboBox_plaza_id_cam7")
        self.comboBox_plaza_id_cam7.addItem("")
        self.comboBox_plaza_id_cam7.addItem("")
        self.comboBox_plaza_id_cam7.addItem("")
        self.comboBox_plaza_id_cam7.addItem("")
        self.comboBox_plaza_id_cam7.addItem("")
        self.comboBox_plaza_id_cam7.addItem("")
        self.comboBox_plaza_id_cam7.addItem("")
        self.comboBox_plaza_id_cam7.addItem("")
        self.comboBox_plaza_id_cam7.addItem("")
        self.comboBox_plaza_id_cam7.addItem("")
        self.comboBox_plaza_id_cam7.addItem("")
        self.comboBox_plaza_id_cam7.addItem("")
        #when select list
        self.comboBox_plaza_id_cam7.currentIndexChanged.connect(self.select_plaza_ID6)
        
        #Lane ID
        self.label_lane_id_cam7 = QtWidgets.QLabel(self.groupBox_anpr_config_cam7)
        self.label_lane_id_cam7.setGeometry(QtCore.QRect(50, 250, 67, 17))
        self.label_lane_id_cam7.setObjectName("label_lane_id_cam7")
        self.lineEdit_lane_id_cam7 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam7)
        self.lineEdit_lane_id_cam7.setGeometry(QtCore.QRect(180, 240, 380, 31))
        self.lineEdit_lane_id_cam7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_lane_id_cam7.setDragEnabled(False)
        self.lineEdit_lane_id_cam7.setObjectName("lineEdit_lane_id_cam7")
        self.lineEdit_lane_id_cam7.setText(lane_ID6)

        setting_changed_list[43] = lane_ID6
        self.lineEdit_lane_id_cam7.textChanged.connect(self.lane_ID6)
        
        #rtsp camera
        self.label_rtsp_cam7 = QtWidgets.QLabel(self.groupBox_anpr_config_cam7)
        self.label_rtsp_cam7.setGeometry(QtCore.QRect(50, 300, 81, 17))
        self.label_rtsp_cam7.setObjectName("label_rtsp_cam7")
        self.lineEdit_rtsp_cam7 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam7)
        self.lineEdit_rtsp_cam7.setGeometry(QtCore.QRect(180, 290, 380, 31))
        self.lineEdit_rtsp_cam7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_rtsp_cam7.setDragEnabled(False)
        self.lineEdit_rtsp_cam7.setObjectName("lineEdit_rtsp_cam7")
        self.lineEdit_rtsp_cam7.setText(input_src6)
        self.lineEdit_rtsp_cam7.textChanged.connect(self.rtsp6)
        
        setting_changed_list[27] = input_src6
        self.lineEdit_rtsp_cam7.textChanged.connect(self.rtsp6)
        
        self.frame.setGeometry(QtCore.QRect(0, -10, 651, 531))
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.raise_()
        self.groupBox_anpr_config_cam6.raise_()
        self.tabWidget_camera_tab.addTab(self.tab_cam6, "")

        self.label_1_milesight_23 = QtWidgets.QLabel(self.groupBox_anpr_config_cam7)
        self.label_1_milesight_23.setGeometry(QtCore.QRect(50, 370, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_1_milesight_23.setFont(font)
        self.label_1_milesight_23.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_1_milesight_23.setObjectName("label_1_milesight_23")
        self.label_komoto_23 = QtWidgets.QLabel(self.groupBox_anpr_config_cam7)
        self.label_komoto_23.setGeometry(QtCore.QRect(50, 390, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_komoto_23.setFont(font)
        self.label_komoto_23.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_komoto_23.setObjectName("label_komoto_23")        
        self.label_eg_23 = QtWidgets.QLabel(self.groupBox_anpr_config_cam7)
        self.label_eg_23.setGeometry(QtCore.QRect(50, 350, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_eg_23.setFont(font)
        self.label_eg_23.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_eg_23.setObjectName("label_eg_23")
        self.tabWidget_camera_tab.addTab(self.tab_cam7, "")
                                                                                                                                                                       
        #------------------------------------------------------------------------
        # tab cam 8
        self.tab_cam8 = QtWidgets.QWidget()
        self.tab_cam8.setObjectName("tab_cam8")
        self.groupBox_anpr_config_cam8 = QtWidgets.QGroupBox(self.tab_cam8)
        self.groupBox_anpr_config_cam8.setGeometry(QtCore.QRect(20, 20, 611, 431))
        self.groupBox_anpr_config_cam8.setObjectName("groupBox_anpr_config_cam8")       
        
        #anpr button
        self.label_ANPR_cam8 = QtWidgets.QLabel(self.groupBox_anpr_config_cam8)
        self.label_ANPR_cam8.setGeometry(QtCore.QRect(50, 40, 51, 17))
        self.label_ANPR_cam8.setObjectName("label_ANPR_cam8")
        self.buttonGroup_anpr_cam8 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_anpr_cam8 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam8)
        self.radioButton_on_anpr_cam8.setGeometry(QtCore.QRect(180, 40, 51, 23))
        self.radioButton_on_anpr_cam8.setChecked(True)
        self.radioButton_on_anpr_cam8.setObjectName("radioButton_on_anpr_cam8")
        self.buttonGroup_anpr_cam8.addButton(self.radioButton_on_anpr_cam8)
        self.radioButton_off_anpr_cam8 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam8)
        self.radioButton_off_anpr_cam8.setGeometry(QtCore.QRect(240, 40, 61, 23))
        self.radioButton_off_anpr_cam8.setObjectName("radioButton_off_anpr_cam8")
        self.buttonGroup_anpr_cam8.setObjectName("buttonGroup_anpr_cam8")
        self.buttonGroup_anpr_cam8.addButton(self.radioButton_off_anpr_cam8)
        
        #vavc button
        self.label_VAVC_cam8 = QtWidgets.QLabel(self.groupBox_anpr_config_cam8)
        self.label_VAVC_cam8.setGeometry(QtCore.QRect(50, 80, 51, 17))
        self.label_VAVC_cam8.setObjectName("label_VAVC_cam8")
        self.buttonGroup_vavc_cam8 = QtWidgets.QButtonGroup(MainWindow)
        self.radioButton_on_vavc_cam8 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam8)
        self.radioButton_on_vavc_cam8.setGeometry(QtCore.QRect(180, 80, 51, 23))
        self.radioButton_on_vavc_cam8.setEnabled(False)
        self.radioButton_on_vavc_cam8.setObjectName("radioButton_on_vavc_cam8")
        self.buttonGroup_vavc_cam8.addButton(self.radioButton_on_vavc_cam8)
        self.radioButton_off_vavc_cam8 = QtWidgets.QRadioButton(self.groupBox_anpr_config_cam8)
        self.radioButton_off_vavc_cam8.setGeometry(QtCore.QRect(240, 80, 61, 23))
        self.radioButton_off_vavc_cam8.setChecked(True)
        self.radioButton_off_vavc_cam8.setObjectName("radioButton_off_vavc_cam8")
        self.buttonGroup_vavc_cam8.setObjectName("buttonGroup_vavc_cam8")
        self.buttonGroup_vavc_cam8.addButton(self.radioButton_off_vavc_cam8)
        
        #mode
        self.label_mode_cam8 = QtWidgets.QLabel(self.groupBox_anpr_config_cam8)
        self.label_mode_cam8.setGeometry(QtCore.QRect(50, 120, 91, 17))
        self.label_mode_cam8.setObjectName("label_mode_cam8")
        self.comboBox_mode_cam8 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam8)
        self.comboBox_mode_cam8.setEnabled(True)
        self.comboBox_mode_cam8.setGeometry(QtCore.QRect(180, 120, 311, 21))
        self.comboBox_mode_cam8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_mode_cam8.setMouseTracking(True)
        self.comboBox_mode_cam8.setWhatsThis("")
        self.comboBox_mode_cam8.setAutoFillBackground(False)
        self.comboBox_mode_cam8.setEditable(False)
        self.comboBox_mode_cam8.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_mode_cam8.setMinimumContentsLength(5)
        self.comboBox_mode_cam8.setObjectName("comboBox_mode_cam8")
        self.comboBox_mode_cam8.addItem("")
        self.comboBox_mode_cam8.addItem("")
        self.comboBox_mode_cam8.addItem("")
        #when select list
        self.comboBox_mode_cam8.currentIndexChanged.connect(self.select_mode7)
        
        #lane type
        self.label_lane_type_cam8 = QtWidgets.QLabel(self.groupBox_anpr_config_cam8)
        self.label_lane_type_cam8.setGeometry(QtCore.QRect(50, 160, 91, 17))
        self.label_lane_type_cam8.setObjectName("label_lane_type_cam8")
        self.comboBox_lane_type_cam8 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam8)
        self.comboBox_lane_type_cam8.setEnabled(True)
        self.comboBox_lane_type_cam8.setGeometry(QtCore.QRect(180, 160, 311, 21))
        self.comboBox_lane_type_cam8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_lane_type_cam8.setMouseTracking(True)
        self.comboBox_lane_type_cam8.setWhatsThis("")
        self.comboBox_lane_type_cam8.setAutoFillBackground(False)
        self.comboBox_lane_type_cam8.setEditable(False)
        self.comboBox_lane_type_cam8.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_lane_type_cam8.setMinimumContentsLength(5)
        self.comboBox_lane_type_cam8.setObjectName("comboBox_lane_type_cam8")
        self.comboBox_lane_type_cam8.addItem("")
        self.comboBox_lane_type_cam8.addItem("")
        self.comboBox_lane_type_cam8.addItem("")
        self.comboBox_lane_type_cam8.addItem("")
        #when select list
        self.comboBox_lane_type_cam8.currentIndexChanged.connect(self.select_lane_type7)  
        
        #Plaza ID
        self.label_plaza_id_cam8 = QtWidgets.QLabel(self.groupBox_anpr_config_cam8)
        self.label_plaza_id_cam8.setGeometry(QtCore.QRect(50, 200, 67, 17))
        self.label_plaza_id_cam8.setObjectName("label_plaza_id_cam8")
        self.comboBox_plaza_id_cam8 = QtWidgets.QComboBox(self.groupBox_anpr_config_cam8)
        self.comboBox_plaza_id_cam8.setEnabled(True)
        self.comboBox_plaza_id_cam8.setGeometry(QtCore.QRect(180, 200, 311, 21))
        self.comboBox_plaza_id_cam8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_plaza_id_cam8.setMouseTracking(True)
        self.comboBox_plaza_id_cam8.setWhatsThis("")
        self.comboBox_plaza_id_cam8.setAutoFillBackground(False)
        self.comboBox_plaza_id_cam8.setEditable(False)
        self.comboBox_plaza_id_cam8.setMaxVisibleItems(10)
        self.comboBox_plaza_id_cam8.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_plaza_id_cam8.setMinimumContentsLength(5)
        self.comboBox_plaza_id_cam8.setFrame(True)
        self.comboBox_plaza_id_cam8.setObjectName("comboBox_plaza_id_cam8")
        self.comboBox_plaza_id_cam8.addItem("")
        self.comboBox_plaza_id_cam8.addItem("")
        self.comboBox_plaza_id_cam8.addItem("")
        self.comboBox_plaza_id_cam8.addItem("")
        self.comboBox_plaza_id_cam8.addItem("")
        self.comboBox_plaza_id_cam8.addItem("")
        self.comboBox_plaza_id_cam8.addItem("")
        self.comboBox_plaza_id_cam8.addItem("")
        self.comboBox_plaza_id_cam8.addItem("")
        self.comboBox_plaza_id_cam8.addItem("")
        self.comboBox_plaza_id_cam8.addItem("")
        self.comboBox_plaza_id_cam8.addItem("")
        #when select list
        self.comboBox_plaza_id_cam8.currentIndexChanged.connect(self.select_plaza_ID7)
        
        #Lane ID
        self.label_lane_id_cam8 = QtWidgets.QLabel(self.groupBox_anpr_config_cam8)
        self.label_lane_id_cam8.setGeometry(QtCore.QRect(50, 250, 67, 17))
        self.label_lane_id_cam8.setObjectName("label_lane_id_cam8")
        self.lineEdit_lane_id_cam8 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam8)
        self.lineEdit_lane_id_cam8.setGeometry(QtCore.QRect(180, 240, 380, 31))
        self.lineEdit_lane_id_cam8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_lane_id_cam8.setDragEnabled(False)
        self.lineEdit_lane_id_cam8.setObjectName("lineEdit_lane_id_cam8")
        self.lineEdit_lane_id_cam8.setText(lane_ID7)

        setting_changed_list[44] = lane_ID7
        self.lineEdit_lane_id_cam8.textChanged.connect(self.lane_ID7)
        
        #rtsp camera
        self.label_rtsp_cam8 = QtWidgets.QLabel(self.groupBox_anpr_config_cam8)
        self.label_rtsp_cam8.setGeometry(QtCore.QRect(50, 300, 81, 17))
        self.label_rtsp_cam8.setObjectName("label_rtsp_cam8")
        self.lineEdit_rtsp_cam8 = QtWidgets.QLineEdit(self.groupBox_anpr_config_cam8)
        self.lineEdit_rtsp_cam8.setGeometry(QtCore.QRect(180, 290, 380, 31))
        self.lineEdit_rtsp_cam8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_rtsp_cam8.setDragEnabled(False)
        self.lineEdit_rtsp_cam8.setObjectName("lineEdit_rtsp_cam8")
        self.lineEdit_rtsp_cam8.setText(input_src7)
        self.lineEdit_rtsp_cam8.textChanged.connect(self.rtsp7)
        
        setting_changed_list[28] = input_src7
        self.lineEdit_rtsp_cam8.textChanged.connect(self.rtsp7)


        self.label_1_milesight_24 = QtWidgets.QLabel(self.groupBox_anpr_config_cam8)
        self.label_1_milesight_24.setGeometry(QtCore.QRect(50, 370, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_1_milesight_24.setFont(font)
        self.label_1_milesight_24.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_1_milesight_24.setObjectName("label_1_milesight_24")
        self.label_komoto_24 = QtWidgets.QLabel(self.groupBox_anpr_config_cam8)
        self.label_komoto_24.setGeometry(QtCore.QRect(50, 390, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_komoto_24.setFont(font)
        self.label_komoto_24.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_komoto_24.setObjectName("label_komoto_24")



        self.label_eg_24 = QtWidgets.QLabel(self.groupBox_anpr_config_cam8)
        self.label_eg_24.setGeometry(QtCore.QRect(50, 350, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_eg_24.setFont(font)
        self.label_eg_24.setStyleSheet("QLabel{\n"
        "color:rgb(186, 189, 182)\n"
        "}")
        self.label_eg_24.setObjectName("label_eg_24")



        #----------------------------------------------------------------------
        self.frame_2 = QtWidgets.QFrame(self.tab_cam8)
        self.frame_2.setGeometry(QtCore.QRect(-10, -10, 651, 531))
        self.frame_2.setAutoFillBackground(True)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.raise_()
        self.groupBox_anpr_config_cam8.raise_()
        self.tabWidget_camera_tab.addTab(self.tab_cam8, "")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/camera.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_camera, icon1, "")
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


        #-------------------------------------------------------------------
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
        icon2.addPixmap(QtGui.QPixmap("icon/floppy-disk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_save.setIcon(icon2)
        self.pushButton_save.setObjectName("pushButton_save")
        self.pushButton_save.clicked.connect(self.pushbutton_save_)
        MainWindow.setCentralWidget(self.centralwidget)


        #---------------------------------------------------------------------
        #current value show at gui
        
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.comboBox_controllerIP.setCurrentIndex(host_IP_i)
        self.comboBox_host_port1.setCurrentIndex(host_port_i)
        self.comboBox_host_port2.setCurrentIndex(host_port2_i)
        self.comboBox_video.setCurrentIndex(src_type_i)
        self.comboBox_toll.setCurrentIndex(toll_i)
        self.tabWidget_camera_tab.setCurrentIndex(0)
        self.comboBox_plaza_id_cam1.setCurrentIndex(plaza_ID0_i)
        self.comboBox_lane_type_cam1.setCurrentIndex(lane_type0_i)
        self.comboBox_mode_cam1.setCurrentIndex(src_mode0_i)
        self.comboBox_plaza_id_cam2.setCurrentIndex(plaza_ID1_i)
        self.comboBox_lane_type_cam2.setCurrentIndex(lane_type1_i)
        self.comboBox_mode_cam2.setCurrentIndex(src_mode1_i)
        self.comboBox_plaza_id_cam3.setCurrentIndex(plaza_ID2_i)
        self.comboBox_lane_type_cam3.setCurrentIndex(lane_type2_i)
        self.comboBox_mode_cam3.setCurrentIndex(src_mode2_i)
        self.comboBox_plaza_id_cam4.setCurrentIndex(plaza_ID3_i)
        self.comboBox_lane_type_cam4.setCurrentIndex(lane_type3_i)
        self.comboBox_mode_cam4.setCurrentIndex(src_mode3_i)
        self.comboBox_plaza_id_cam5.setCurrentIndex(plaza_ID4_i)
        self.comboBox_lane_type_cam5.setCurrentIndex(lane_type4_i)
        self.comboBox_mode_cam5.setCurrentIndex(src_mode4_i)
        self.comboBox_plaza_id_cam6.setCurrentIndex(plaza_ID5_i)
        self.comboBox_lane_type_cam6.setCurrentIndex(lane_type5_i)
        self.comboBox_mode_cam6.setCurrentIndex(src_mode5_i)
        self.comboBox_plaza_id_cam7.setCurrentIndex(plaza_ID6_i)
        self.comboBox_lane_type_cam7.setCurrentIndex(lane_type6_i)
        self.comboBox_mode_cam7.setCurrentIndex(src_mode6_i)
        self.comboBox_plaza_id_cam8.setCurrentIndex(plaza_ID7_i)
        self.comboBox_lane_type_cam8.setCurrentIndex(lane_type7_i)
        self.comboBox_mode_cam8.setCurrentIndex(src_mode7_i)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    # all parameter value at gui
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ANPR Setting"))
        self.groupBox_controller_config.setTitle(_translate("MainWindow", "Controller configuration  "))
        self.label_host_port1.setText(_translate("MainWindow", "Host Port 1"))
        self.comboBox_controllerIP.setCurrentText(_translate("MainWindow", "-- Select IP --"))
        self.comboBox_controllerIP.setItemText(0, _translate("MainWindow", "-- Select IP -- "))
        self.comboBox_controllerIP.setItemText(1, _translate("MainWindow", "10.20.3.15 - Gombak"))
        self.comboBox_controllerIP.setItemText(2, _translate("MainWindow", "10.20.4.15 - Bentong"))
        self.comboBox_controllerIP.setItemText(3, _translate("MainWindow", "10.20.5.5 - Karak 1"))
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
        self.comboBox_controllerIP.setItemText(14, _translate("MainWindow", "local"))
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
        self.comboBox_video.setCurrentText(_translate("MainWindow", "Video"))
        self.comboBox_video.setItemText(0, _translate("MainWindow", "-- Select Source --"))
        self.comboBox_video.setItemText(1, _translate("MainWindow", "Video"))
        self.comboBox_video.setItemText(2, _translate("MainWindow", "Image"))
        self.label_src_type.setText(_translate("MainWindow", "Source type"))
        self.label_toll.setText(_translate("MainWindow", "Toll"))
        self.comboBox_toll.setCurrentText(_translate("MainWindow", "-- Select Toll --"))
        self.comboBox_toll.setItemText(0, _translate("MainWindow", "-- Select Toll --"))
        self.comboBox_toll.setItemText(1, _translate("MainWindow", "KLK"))
        self.comboBox_toll.setItemText(2, _translate("MainWindow", "LPT 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_controller), _translate("MainWindow", "  Controller"))

         #---------------------------------------------------------------------------------------


        # =================================================================
        # |                                                               |
        # |                       Start Tab Camera                        |
        # |                                                               |
        # =================================================================


        #---------------------------------------------------------------------------------------



        self.groupBox_anpr_config_cam1.setTitle(_translate("MainWindow", "Camera 1 "))
        self.label_plaza_id_cam1.setText(_translate("MainWindow", "Plaza ID"))
        self.comboBox_plaza_id_cam1.setCurrentText(_translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam1.setItemText(0, _translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam1.setItemText(1, _translate("MainWindow", "101 - Gombak"))
        self.comboBox_plaza_id_cam1.setItemText(2, _translate("MainWindow", "100 - Bentong"))
        self.comboBox_plaza_id_cam1.setItemText(3, _translate("MainWindow", "801 - Karak"))
        self.comboBox_plaza_id_cam1.setItemText(4, _translate("MainWindow", "802 - Lanchang"))
        self.comboBox_plaza_id_cam1.setItemText(5, _translate("MainWindow", "803 - Temerloh"))
        self.comboBox_plaza_id_cam1.setItemText(6, _translate("MainWindow", "804 - Chenor"))
        self.comboBox_plaza_id_cam1.setItemText(7, _translate("MainWindow", "805 - Maran"))
        self.comboBox_plaza_id_cam1.setItemText(8, _translate("MainWindow", "806 - Srijaya"))
        self.comboBox_plaza_id_cam1.setItemText(9, _translate("MainWindow", "807 - Gambang"))
        self.comboBox_plaza_id_cam1.setItemText(10, _translate("MainWindow", "808 - Kuantan"))
        self.comboBox_plaza_id_cam1.setItemText(11, _translate("MainWindow", "809 - Jabor"))
        self.label_lane_type_cam1.setText(_translate("MainWindow", "Lane type"))
        self.label_mode_cam1.setText(_translate("MainWindow", "Mode"))
        self.comboBox_lane_type_cam1.setCurrentText(_translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam1.setItemText(0, _translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam1.setItemText(1, _translate("MainWindow", "Offline"))
        self.comboBox_lane_type_cam1.setItemText(2, _translate("MainWindow", "Quatriz"))
        self.comboBox_lane_type_cam1.setItemText(3, _translate("MainWindow", "Teras"))
        self.comboBox_mode_cam1.setCurrentText(_translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam1.setItemText(0, _translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam1.setItemText(1, _translate("MainWindow", "Online"))
        self.comboBox_mode_cam1.setItemText(2, _translate("MainWindow", "Offline"))
        self.label_1_milesight_16.setText(_translate("MainWindow", "1. Milesight : rtsp://admin:Milesight12345@10.20.12.31:554/main"))
        self.label_komoto_16.setText(_translate("MainWindow", "2. Komoto   : rtsp://root:Komoto@172.18.117.115/cam0_0"))
        self.label_lane_id_cam1.setText(_translate("MainWindow", "Lane ID"))
        self.label_rtsp_cam1.setText(_translate("MainWindow", "Camera 1"))
        self.lineEdit_lane_id_cam1.setPlaceholderText(_translate("MainWindow", "e.g. M01, K02, T03"))
        self.label_eg_16.setText(_translate("MainWindow", "*Note : "))
        self.lineEdit_rtsp_cam1.setPlaceholderText(_translate("MainWindow", "rtsp://"))
        self.radioButton_off_vavc_cam1.setText(_translate("MainWindow", "OFF"))
        self.radioButton_off_anpr_cam1.setText(_translate("MainWindow", "OFF"))
        self.label_ANPR_cam1.setText(_translate("MainWindow", "ANPR"))
        self.radioButton_on_vavc_cam1.setText(_translate("MainWindow", "ON"))
        self.label_VAVC_cam1.setText(_translate("MainWindow", "VAVC"))
        self.radioButton_on_anpr_cam1.setText(_translate("MainWindow", "ON"))
        self.tabWidget_camera_tab.setTabText(self.tabWidget_camera_tab.indexOf(self.tab_cam1), _translate("MainWindow", "Cam 1"))
        self.groupBox_anpr_config_cam2.setTitle(_translate("MainWindow", "Camera 2"))
        self.label_plaza_id_cam2.setText(_translate("MainWindow", "Plaza ID"))
        self.comboBox_plaza_id_cam2.setCurrentText(_translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam2.setItemText(0, _translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam2.setItemText(1, _translate("MainWindow", "101 - Gombak"))
        self.comboBox_plaza_id_cam2.setItemText(2, _translate("MainWindow", "100 - Bentong"))
        self.comboBox_plaza_id_cam2.setItemText(3, _translate("MainWindow", "801 - Karak"))
        self.comboBox_plaza_id_cam2.setItemText(4, _translate("MainWindow", "802 - Lanchang"))
        self.comboBox_plaza_id_cam2.setItemText(5, _translate("MainWindow", "803 - Temerloh"))
        self.comboBox_plaza_id_cam2.setItemText(6, _translate("MainWindow", "804 - Chenor"))
        self.comboBox_plaza_id_cam2.setItemText(7, _translate("MainWindow", "805 - Maran"))
        self.comboBox_plaza_id_cam2.setItemText(8, _translate("MainWindow", "806 - Srijaya"))
        self.comboBox_plaza_id_cam2.setItemText(9, _translate("MainWindow", "807 - Gambang"))
        self.comboBox_plaza_id_cam2.setItemText(10, _translate("MainWindow", "808 - Kuantan"))
        self.comboBox_plaza_id_cam2.setItemText(11, _translate("MainWindow", "809 - Jabor"))
        self.label_lane_type_cam2.setText(_translate("MainWindow", "Lane type"))
        self.label_mode_cam2.setText(_translate("MainWindow", "Mode"))
        self.comboBox_lane_type_cam2.setCurrentText(_translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam2.setItemText(0, _translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam2.setItemText(1, _translate("MainWindow", "Offline"))
        self.comboBox_lane_type_cam2.setItemText(2, _translate("MainWindow", "Quatriz"))
        self.comboBox_lane_type_cam2.setItemText(3, _translate("MainWindow", "Teras"))
        self.comboBox_mode_cam2.setCurrentText(_translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam2.setItemText(0, _translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam2.setItemText(1, _translate("MainWindow", "Online"))
        self.comboBox_mode_cam2.setItemText(2, _translate("MainWindow", "Offline"))
        self.label_1_milesight_17.setText(_translate("MainWindow", "1. Milesight : rtsp://admin:Milesight12345@10.20.12.31:554/main"))
        self.label_komoto_17.setText(_translate("MainWindow", "2. Komoto   : rtsp://root:Komoto@172.18.117.115/cam0_0"))
        self.label_lane_id_cam2.setText(_translate("MainWindow", "Lane ID"))
        self.label_rtsp_cam2.setText(_translate("MainWindow", "Camera 2"))
        self.lineEdit_lane_id_cam2.setPlaceholderText(_translate("MainWindow", "e.g. M01, K02, T03"))
        self.label_eg_17.setText(_translate("MainWindow", "*Note : "))
        self.lineEdit_rtsp_cam2.setPlaceholderText(_translate("MainWindow", "rtsp://"))
        self.radioButton_off_vavc_cam2.setText(_translate("MainWindow", "OFF"))
        self.radioButton_off_anpr_cam2.setText(_translate("MainWindow", "OFF"))
        self.label_ANPR_cam2.setText(_translate("MainWindow", "ANPR"))
        self.radioButton_on_vavc_cam2.setText(_translate("MainWindow", "ON"))
        self.label_VAVC_cam2.setText(_translate("MainWindow", "VAVC"))
        self.radioButton_on_anpr_cam2.setText(_translate("MainWindow", "ON"))
        self.tabWidget_camera_tab.setTabText(self.tabWidget_camera_tab.indexOf(self.tab_cam2), _translate("MainWindow", "Cam 2"))
        self.groupBox_anpr_config_cam3.setTitle(_translate("MainWindow", "Camera 3"))
        self.label_plaza_id_cam3.setText(_translate("MainWindow", "Plaza ID"))
        self.comboBox_plaza_id_cam3.setCurrentText(_translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam3.setItemText(0, _translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam3.setItemText(1, _translate("MainWindow", "101 - Gombak"))
        self.comboBox_plaza_id_cam3.setItemText(2, _translate("MainWindow", "100 - Bentong"))
        self.comboBox_plaza_id_cam3.setItemText(3, _translate("MainWindow", "801 - Karak"))
        self.comboBox_plaza_id_cam3.setItemText(4, _translate("MainWindow", "802 - Lanchang"))
        self.comboBox_plaza_id_cam3.setItemText(5, _translate("MainWindow", "803 - Temerloh"))
        self.comboBox_plaza_id_cam3.setItemText(6, _translate("MainWindow", "804 - Chenor"))
        self.comboBox_plaza_id_cam3.setItemText(7, _translate("MainWindow", "805 - Maran"))
        self.comboBox_plaza_id_cam3.setItemText(8, _translate("MainWindow", "806 - Srijaya"))
        self.comboBox_plaza_id_cam3.setItemText(9, _translate("MainWindow", "807 - Gambang"))
        self.comboBox_plaza_id_cam3.setItemText(10, _translate("MainWindow", "808 - Kuantan"))
        self.comboBox_plaza_id_cam3.setItemText(11, _translate("MainWindow", "809 - Jabor"))
        self.label_lane_type_cam3.setText(_translate("MainWindow", "Lane type"))
        self.label_mode_cam3.setText(_translate("MainWindow", "Mode"))
        self.comboBox_lane_type_cam3.setCurrentText(_translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam3.setItemText(0, _translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam3.setItemText(1, _translate("MainWindow", "Offline"))
        self.comboBox_lane_type_cam3.setItemText(2, _translate("MainWindow", "Quatriz"))
        self.comboBox_lane_type_cam3.setItemText(3, _translate("MainWindow", "Teras"))
        self.comboBox_mode_cam3.setCurrentText(_translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam3.setItemText(0, _translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam3.setItemText(1, _translate("MainWindow", "Online"))
        self.comboBox_mode_cam3.setItemText(2, _translate("MainWindow", "Offline"))
        self.label_1_milesight_18.setText(_translate("MainWindow", "1. Milesight : rtsp://admin:Milesight12345@10.20.12.31:554/main"))
        self.label_komoto_18.setText(_translate("MainWindow", "2. Komoto   : rtsp://root:Komoto@172.18.117.115/cam0_0"))
        self.label_lane_id_cam3.setText(_translate("MainWindow", "Lane ID"))
        self.label_rtsp_cam3.setText(_translate("MainWindow", "Camera 1"))
        self.lineEdit_lane_id_cam3.setPlaceholderText(_translate("MainWindow", "e.g. M01, K02, T03"))
        self.label_eg_18.setText(_translate("MainWindow", "*Note : "))
        self.lineEdit_rtsp_cam3.setPlaceholderText(_translate("MainWindow", "rtsp://"))
        self.radioButton_off_vavc_cam3.setText(_translate("MainWindow", "OFF"))
        self.radioButton_off_anpr_cam3.setText(_translate("MainWindow", "OFF"))
        self.label_ANPR_cam3.setText(_translate("MainWindow", "ANPR"))
        self.radioButton_on_vavc_cam3.setText(_translate("MainWindow", "ON"))
        self.label_VAVC_cam3.setText(_translate("MainWindow", "VAVC"))
        self.radioButton_on_anpr_cam3.setText(_translate("MainWindow", "ON"))
        self.tabWidget_camera_tab.setTabText(self.tabWidget_camera_tab.indexOf(self.tab_cam3), _translate("MainWindow", "Cam 3"))
        self.groupBox_anpr_config_cam4.setTitle(_translate("MainWindow", "Camera 4"))
        self.label_plaza_id_cam4.setText(_translate("MainWindow", "Plaza ID"))
        self.comboBox_plaza_id_cam4.setCurrentText(_translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam4.setItemText(0, _translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam4.setItemText(1, _translate("MainWindow", "101 - Gombak"))
        self.comboBox_plaza_id_cam4.setItemText(2, _translate("MainWindow", "100 - Bentong"))
        self.comboBox_plaza_id_cam4.setItemText(3, _translate("MainWindow", "801 - Karak"))
        self.comboBox_plaza_id_cam4.setItemText(4, _translate("MainWindow", "802 - Lanchang"))
        self.comboBox_plaza_id_cam4.setItemText(5, _translate("MainWindow", "803 - Temerloh"))
        self.comboBox_plaza_id_cam4.setItemText(6, _translate("MainWindow", "804 - Chenor"))
        self.comboBox_plaza_id_cam4.setItemText(7, _translate("MainWindow", "805 - Maran"))
        self.comboBox_plaza_id_cam4.setItemText(8, _translate("MainWindow", "806 - Srijaya"))
        self.comboBox_plaza_id_cam4.setItemText(9, _translate("MainWindow", "807 - Gambang"))
        self.comboBox_plaza_id_cam4.setItemText(10, _translate("MainWindow", "808 - Kuantan"))
        self.comboBox_plaza_id_cam4.setItemText(11, _translate("MainWindow", "809 - Jabor"))
        self.label_lane_type_cam4.setText(_translate("MainWindow", "Lane type"))
        self.label_mode_cam4.setText(_translate("MainWindow", "Mode"))
        self.comboBox_lane_type_cam4.setCurrentText(_translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam4.setItemText(0, _translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam4.setItemText(1, _translate("MainWindow", "Offline"))
        self.comboBox_lane_type_cam4.setItemText(2, _translate("MainWindow", "Quatriz"))
        self.comboBox_lane_type_cam4.setItemText(3, _translate("MainWindow", "Teras"))
        self.comboBox_mode_cam4.setCurrentText(_translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam4.setItemText(0, _translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam4.setItemText(1, _translate("MainWindow", "Online"))
        self.comboBox_mode_cam4.setItemText(2, _translate("MainWindow", "Offline"))
        self.label_1_milesight_20.setText(_translate("MainWindow", "1. Milesight : rtsp://admin:Milesight12345@10.20.12.31:554/main"))
        self.label_komoto_20.setText(_translate("MainWindow", "2. Komoto   : rtsp://root:Komoto@172.18.117.115/cam0_0"))
        self.label_lane_id_cam4.setText(_translate("MainWindow", "Lane ID"))
        self.label_rtsp_cam4.setText(_translate("MainWindow", "Camera 4"))
        self.lineEdit_lane_id_cam4.setPlaceholderText(_translate("MainWindow", "e.g. M01, K02, T03"))
        self.label_eg_20.setText(_translate("MainWindow", "*Note : "))
        self.lineEdit_rtsp_cam4.setPlaceholderText(_translate("MainWindow", "rtsp://"))
        self.radioButton_off_vavc_cam4.setText(_translate("MainWindow", "OFF"))
        self.radioButton_off_anpr_cam4.setText(_translate("MainWindow", "OFF"))
        self.label_ANPR_cam4.setText(_translate("MainWindow", "ANPR"))
        self.radioButton_on_vavc_cam4.setText(_translate("MainWindow", "ON"))
        self.label_VAVC_cam4.setText(_translate("MainWindow", "VAVC"))
        self.radioButton_on_anpr_cam4.setText(_translate("MainWindow", "ON"))
        self.tabWidget_camera_tab.setTabText(self.tabWidget_camera_tab.indexOf(self.tab_cam4), _translate("MainWindow", "Cam 4"))
        self.groupBox_anpr_config_cam5.setTitle(_translate("MainWindow", "Camera 5"))
        self.label_plaza_id_cam5.setText(_translate("MainWindow", "Plaza ID"))
        self.comboBox_plaza_id_cam5.setCurrentText(_translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam5.setItemText(0, _translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam5.setItemText(1, _translate("MainWindow", "101 - Gombak"))
        self.comboBox_plaza_id_cam5.setItemText(2, _translate("MainWindow", "100 - Bentong"))
        self.comboBox_plaza_id_cam5.setItemText(3, _translate("MainWindow", "801 - Karak"))
        self.comboBox_plaza_id_cam5.setItemText(4, _translate("MainWindow", "802 - Lanchang"))
        self.comboBox_plaza_id_cam5.setItemText(5, _translate("MainWindow", "803 - Temerloh"))
        self.comboBox_plaza_id_cam5.setItemText(6, _translate("MainWindow", "804 - Chenor"))
        self.comboBox_plaza_id_cam5.setItemText(7, _translate("MainWindow", "805 - Maran"))
        self.comboBox_plaza_id_cam5.setItemText(8, _translate("MainWindow", "806 - Srijaya"))
        self.comboBox_plaza_id_cam5.setItemText(9, _translate("MainWindow", "807 - Gambang"))
        self.comboBox_plaza_id_cam5.setItemText(10, _translate("MainWindow", "808 - Kuantan"))
        self.comboBox_plaza_id_cam5.setItemText(11, _translate("MainWindow", "809 - Jabor"))
        self.label_lane_type_cam5.setText(_translate("MainWindow", "Lane type"))
        self.label_mode_cam5.setText(_translate("MainWindow", "Mode"))
        self.comboBox_lane_type_cam5.setCurrentText(_translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam5.setItemText(0, _translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam5.setItemText(1, _translate("MainWindow", "Offline"))
        self.comboBox_lane_type_cam5.setItemText(2, _translate("MainWindow", "Quatriz"))
        self.comboBox_lane_type_cam5.setItemText(3, _translate("MainWindow", "Teras"))
        self.comboBox_mode_cam5.setCurrentText(_translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam5.setItemText(0, _translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam5.setItemText(1, _translate("MainWindow", "Online"))
        self.comboBox_mode_cam5.setItemText(2, _translate("MainWindow", "Offline"))
        self.label_1_milesight_21.setText(_translate("MainWindow", "1. Milesight : rtsp://admin:Milesight12345@10.20.12.31:554/main"))
        self.label_komoto_21.setText(_translate("MainWindow", "2. Komoto   : rtsp://root:Komoto@172.18.117.115/cam0_0"))
        self.label_lane_id_cam5.setText(_translate("MainWindow", "Lane ID"))
        self.label_rtsp_cam5.setText(_translate("MainWindow", "Camera 5"))
        self.lineEdit_lane_id_cam5.setPlaceholderText(_translate("MainWindow", "e.g. M01, K02, T03"))
        self.label_eg_21.setText(_translate("MainWindow", "*Note : "))
        self.lineEdit_rtsp_cam5.setPlaceholderText(_translate("MainWindow", "rtsp://"))
        self.radioButton_off_vavc_cam5.setText(_translate("MainWindow", "OFF"))
        self.radioButton_off_anpr_cam5.setText(_translate("MainWindow", "OFF"))
        self.label_ANPR_cam5.setText(_translate("MainWindow", "ANPR"))
        self.radioButton_on_vavc_cam5.setText(_translate("MainWindow", "ON"))
        self.label_VAVC_cam5.setText(_translate("MainWindow", "VAVC"))
        self.radioButton_on_anpr_cam5.setText(_translate("MainWindow", "ON"))
        self.tabWidget_camera_tab.setTabText(self.tabWidget_camera_tab.indexOf(self.tab_cam5), _translate("MainWindow", "Cam 5"))
        self.groupBox_anpr_config_cam6.setTitle(_translate("MainWindow", "Camera 6"))
        self.label_plaza_id_cam6.setText(_translate("MainWindow", "Plaza ID"))
        self.comboBox_plaza_id_cam6.setCurrentText(_translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam6.setItemText(0, _translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam6.setItemText(1, _translate("MainWindow", "101 - Gombak"))
        self.comboBox_plaza_id_cam6.setItemText(2, _translate("MainWindow", "100 - Bentong"))
        self.comboBox_plaza_id_cam6.setItemText(3, _translate("MainWindow", "801 - Karak"))
        self.comboBox_plaza_id_cam6.setItemText(4, _translate("MainWindow", "802 - Lanchang"))
        self.comboBox_plaza_id_cam6.setItemText(5, _translate("MainWindow", "803 - Temerloh"))
        self.comboBox_plaza_id_cam6.setItemText(6, _translate("MainWindow", "804 - Chenor"))
        self.comboBox_plaza_id_cam6.setItemText(7, _translate("MainWindow", "805 - Maran"))
        self.comboBox_plaza_id_cam6.setItemText(8, _translate("MainWindow", "806 - Srijaya"))
        self.comboBox_plaza_id_cam6.setItemText(9, _translate("MainWindow", "807 - Gambang"))
        self.comboBox_plaza_id_cam6.setItemText(10, _translate("MainWindow", "808 - Kuantan"))
        self.comboBox_plaza_id_cam6.setItemText(11, _translate("MainWindow", "809 - Jabor"))
        self.label_lane_type_cam6.setText(_translate("MainWindow", "Lane type"))
        self.label_mode_cam6.setText(_translate("MainWindow", "Mode"))
        self.comboBox_lane_type_cam6.setCurrentText(_translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam6.setItemText(0, _translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam6.setItemText(1, _translate("MainWindow", "Offline"))
        self.comboBox_lane_type_cam6.setItemText(2, _translate("MainWindow", "Quatriz"))
        self.comboBox_lane_type_cam6.setItemText(3, _translate("MainWindow", "Teras"))
        self.comboBox_mode_cam6.setCurrentText(_translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam6.setItemText(0, _translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam6.setItemText(1, _translate("MainWindow", "Online"))
        self.comboBox_mode_cam6.setItemText(2, _translate("MainWindow", "Offline"))
        self.label_1_milesight_22.setText(_translate("MainWindow", "1. Milesight : rtsp://admin:Milesight12345@10.20.12.31:554/main"))
        self.label_komoto_22.setText(_translate("MainWindow", "2. Komoto   : rtsp://root:Komoto@172.18.117.115/cam0_0"))
        self.label_lane_id_cam6.setText(_translate("MainWindow", "Lane ID"))
        self.label_rtsp_cam6.setText(_translate("MainWindow", "Camera 6"))
        self.lineEdit_lane_id_cam6.setPlaceholderText(_translate("MainWindow", "e.g. M01, K02, T03"))
        self.label_eg_22.setText(_translate("MainWindow", "*Note : "))
        self.lineEdit_rtsp_cam6.setPlaceholderText(_translate("MainWindow", "rtsp://"))
        self.radioButton_off_vavc_cam6.setText(_translate("MainWindow", "OFF"))
        self.radioButton_off_anpr_cam6.setText(_translate("MainWindow", "OFF"))
        self.label_ANPR_cam6.setText(_translate("MainWindow", "ANPR"))
        self.radioButton_on_vavc_cam6.setText(_translate("MainWindow", "ON"))
        self.label_VAVC_cam6.setText(_translate("MainWindow", "VAVC"))
        self.radioButton_on_anpr_cam6.setText(_translate("MainWindow", "ON"))
        self.tabWidget_camera_tab.setTabText(self.tabWidget_camera_tab.indexOf(self.tab_cam6), _translate("MainWindow", "Cam 6"))
        self.groupBox_anpr_config_cam7.setTitle(_translate("MainWindow", "Camera 7"))
        self.label_plaza_id_cam7.setText(_translate("MainWindow", "Plaza ID"))
        self.comboBox_plaza_id_cam7.setCurrentText(_translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam7.setItemText(0, _translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam7.setItemText(1, _translate("MainWindow", "101 - Gombak"))
        self.comboBox_plaza_id_cam7.setItemText(2, _translate("MainWindow", "100 - Bentong"))
        self.comboBox_plaza_id_cam7.setItemText(3, _translate("MainWindow", "801 - Karak"))
        self.comboBox_plaza_id_cam7.setItemText(4, _translate("MainWindow", "802 - Lanchang"))
        self.comboBox_plaza_id_cam7.setItemText(5, _translate("MainWindow", "803 - Temerloh"))
        self.comboBox_plaza_id_cam7.setItemText(6, _translate("MainWindow", "804 - Chenor"))
        self.comboBox_plaza_id_cam7.setItemText(7, _translate("MainWindow", "805 - Maran"))
        self.comboBox_plaza_id_cam7.setItemText(8, _translate("MainWindow", "806 - Srijaya"))
        self.comboBox_plaza_id_cam7.setItemText(9, _translate("MainWindow", "807 - Gambang"))
        self.comboBox_plaza_id_cam7.setItemText(10, _translate("MainWindow", "808 - Kuantan"))
        self.comboBox_plaza_id_cam7.setItemText(11, _translate("MainWindow", "809 - Jabor"))
        self.label_lane_type_cam7.setText(_translate("MainWindow", "Lane type"))
        self.label_mode_cam7.setText(_translate("MainWindow", "Mode"))
        self.comboBox_lane_type_cam7.setCurrentText(_translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam7.setItemText(0, _translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam7.setItemText(1, _translate("MainWindow", "Offline"))
        self.comboBox_lane_type_cam7.setItemText(2, _translate("MainWindow", "Quatriz"))
        self.comboBox_lane_type_cam7.setItemText(3, _translate("MainWindow", "Teras"))
        self.comboBox_mode_cam7.setCurrentText(_translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam7.setItemText(0, _translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam7.setItemText(1, _translate("MainWindow", "Online"))
        self.comboBox_mode_cam7.setItemText(2, _translate("MainWindow", "Offline"))
        self.label_1_milesight_23.setText(_translate("MainWindow", "1. Milesight : rtsp://admin:Milesight12345@10.20.12.31:554/main"))
        self.label_komoto_23.setText(_translate("MainWindow", "2. Komoto   : rtsp://root:Komoto@172.18.117.115/cam0_0"))
        self.label_lane_id_cam7.setText(_translate("MainWindow", "Lane ID"))
        self.label_rtsp_cam7.setText(_translate("MainWindow", "Camera 7"))
        self.lineEdit_lane_id_cam7.setPlaceholderText(_translate("MainWindow", "e.g. M01, K02, T03"))
        self.label_eg_23.setText(_translate("MainWindow", "*Note : "))
        self.lineEdit_rtsp_cam7.setPlaceholderText(_translate("MainWindow", "rtsp://"))
        self.radioButton_off_vavc_cam7.setText(_translate("MainWindow", "OFF"))
        self.radioButton_off_anpr_cam7.setText(_translate("MainWindow", "OFF"))
        self.label_ANPR_cam7.setText(_translate("MainWindow", "ANPR"))
        self.radioButton_on_vavc_cam7.setText(_translate("MainWindow", "ON"))
        self.label_VAVC_cam7.setText(_translate("MainWindow", "VAVC"))
        self.radioButton_on_anpr_cam7.setText(_translate("MainWindow", "ON"))
        self.tabWidget_camera_tab.setTabText(self.tabWidget_camera_tab.indexOf(self.tab_cam7), _translate("MainWindow", "Cam 7"))
        self.groupBox_anpr_config_cam8.setTitle(_translate("MainWindow", "Camera 8"))
        self.label_plaza_id_cam8.setText(_translate("MainWindow", "Plaza ID"))
        self.comboBox_plaza_id_cam8.setCurrentText(_translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam8.setItemText(0, _translate("MainWindow", "-- Select Plaza ID--"))
        self.comboBox_plaza_id_cam8.setItemText(1, _translate("MainWindow", "101 - Gombak"))
        self.comboBox_plaza_id_cam8.setItemText(2, _translate("MainWindow", "100 - Bentong"))
        self.comboBox_plaza_id_cam8.setItemText(3, _translate("MainWindow", "801 - Karak"))
        self.comboBox_plaza_id_cam8.setItemText(4, _translate("MainWindow", "802 - Lanchang"))
        self.comboBox_plaza_id_cam8.setItemText(5, _translate("MainWindow", "803 - Temerloh"))
        self.comboBox_plaza_id_cam8.setItemText(6, _translate("MainWindow", "804 - Chenor"))
        self.comboBox_plaza_id_cam8.setItemText(7, _translate("MainWindow", "805 - Maran"))
        self.comboBox_plaza_id_cam8.setItemText(8, _translate("MainWindow", "806 - Srijaya"))
        self.comboBox_plaza_id_cam8.setItemText(9, _translate("MainWindow", "807 - Gambang"))
        self.comboBox_plaza_id_cam8.setItemText(10, _translate("MainWindow", "808 - Kuantan"))
        self.comboBox_plaza_id_cam8.setItemText(11, _translate("MainWindow", "809 - Jabor"))
        self.label_lane_type_cam8.setText(_translate("MainWindow", "Lane type"))
        self.label_mode_cam8.setText(_translate("MainWindow", "Mode"))
        self.comboBox_lane_type_cam8.setCurrentText(_translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam8.setItemText(0, _translate("MainWindow", "-- Select Lane --"))
        self.comboBox_lane_type_cam8.setItemText(1, _translate("MainWindow", "Offline"))
        self.comboBox_lane_type_cam8.setItemText(2, _translate("MainWindow", "Quatriz"))
        self.comboBox_lane_type_cam8.setItemText(3, _translate("MainWindow", "Teras"))
        self.comboBox_mode_cam8.setCurrentText(_translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam8.setItemText(0, _translate("MainWindow", "-- Select Mode --"))
        self.comboBox_mode_cam8.setItemText(1, _translate("MainWindow", "Online"))
        self.comboBox_mode_cam8.setItemText(2, _translate("MainWindow", "Offline"))
        self.label_1_milesight_24.setText(_translate("MainWindow", "1. Milesight : rtsp://admin:Milesight12345@10.20.12.31:554/main"))
        self.label_komoto_24.setText(_translate("MainWindow", "2. Komoto   : rtsp://root:Komoto@172.18.117.115/cam0_0"))
        self.label_lane_id_cam8.setText(_translate("MainWindow", "Lane ID"))
        self.label_rtsp_cam8.setText(_translate("MainWindow", "Camera 8"))
        self.lineEdit_lane_id_cam8.setPlaceholderText(_translate("MainWindow", "e.g. M01, K02, T03"))
        self.label_eg_24.setText(_translate("MainWindow", "*Note : "))
        self.lineEdit_rtsp_cam8.setPlaceholderText(_translate("MainWindow", "rtsp://"))
        self.radioButton_off_vavc_cam8.setText(_translate("MainWindow", "OFF"))
        self.radioButton_off_anpr_cam8.setText(_translate("MainWindow", "OFF"))
        self.label_ANPR_cam8.setText(_translate("MainWindow", "ANPR"))
        self.radioButton_on_vavc_cam8.setText(_translate("MainWindow", "ON"))
        self.label_VAVC_cam8.setText(_translate("MainWindow", "VAVC"))
        self.radioButton_on_anpr_cam8.setText(_translate("MainWindow", "ON"))
        self.tabWidget_camera_tab.setTabText(self.tabWidget_camera_tab.indexOf(self.tab_cam8), _translate("MainWindow", "Cam 8"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_camera), _translate("MainWindow", "Camera"))
        self.label_ANPR_setting_page.setText(_translate("MainWindow", "ANPR Setting Page"))
        self.pushButton_save.setText(_translate("MainWindow", "  Save"))


        # ==============  END OF FRONT-END   ==================================



    def enable_host_port2(self, state):                

        if state == QtCore.Qt.Checked:
                # print('check')
                self.label_host_port2.setEnabled(True)
                self.comboBox_host_port2.setEnabled(True)
        else:
                # print('uncheck')
                self.label_host_port2.setEnabled(False)
                self.comboBox_host_port2.setEnabled(False)
    
    def select_controller_IP(self, controller_IP_i):
        print("current index ", controller_IP_i, "select ", self.comboBox_controllerIP.currentText())
        
        #controller ip list
        if controller_IP_i == 0 : host_IP_changed = ""
        if controller_IP_i == 1 : host_IP_changed = "10.20.3.15"
        if controller_IP_i == 2 : host_IP_changed = "10.20.4.15"
        if controller_IP_i == 3 : host_IP_changed = "10.20.5.5"
        if controller_IP_i == 4 : host_IP_changed = "10.20.5.6"
        if controller_IP_i == 5 : host_IP_changed = "10.20.6.5"
        if controller_IP_i == 6 : host_IP_changed = "10.20.7.5"
        if controller_IP_i == 7 : host_IP_changed = "10.20.8.5"
        if controller_IP_i == 8 : host_IP_changed = "10.20.9.5"
        if controller_IP_i == 9 : host_IP_changed = "10.20.10.5"
        if controller_IP_i == 10: host_IP_changed = "10.20.11.5"
        if controller_IP_i == 11: host_IP_changed = "10.20.12.5"
        if controller_IP_i == 12: host_IP_changed = "10.20.13.5"
        if controller_IP_i == 13: host_IP_changed = "10.20.13.6"
        if controller_IP_i == 14: host_IP_changed = "local"

        print("host_IP : ", host_IP_changed)
        setting_changed_list[0] = host_IP_changed

    def select_host_port(self, host_port_i):
        print("current index ", host_port_i, "select ", self.comboBox_host_port1.currentText())

        # port list
        if host_port_i == 0 : host_port = ""
        if host_port_i == 1 : host_port = "1000" 
        if host_port_i == 2 : host_port = "2000" 
        if host_port_i == 3 : host_port = "3000" 
        if host_port_i == 4 : host_port = "4000" 
        if host_port_i == 5 : host_port = "5000" 
        if host_port_i == 6 : host_port = "6000" 
        if host_port_i == 7 : host_port = "7000" 
        if host_port_i == 8 : host_port = "8000" 
        if host_port_i == 9 : host_port = "9000" 

        print("host_port : ", host_port)
        setting_changed_list[1] = host_port

    def select_host_port2(self, host_port2_i):
        print("current index ", host_port2_i, "select ", self.comboBox_host_port2.currentText())

        # port list
        if host_port2_i == 0 : host_port2 = ""
        if host_port2_i == 1 : host_port2 = "1000" 
        if host_port2_i == 2 : host_port2 = "2000" 
        if host_port2_i == 3 : host_port2 = "3000" 
        if host_port2_i == 4 : host_port2 = "4000" 
        if host_port2_i == 5 : host_port2 = "5000" 
        if host_port2_i == 6 : host_port2 = "6000" 
        if host_port2_i == 7 : host_port2 = "7000" 
        if host_port2_i == 8 : host_port2 = "8000" 
        if host_port2_i == 9 : host_port2 = "9000" 

        print("host_port2 : ", host_port2)
        setting_changed_list[2] = host_port2

    def select_source_type(self, src_type_i):
        # type list
        if src_type_i == 0 : src_type = ""
        if src_type_i == 1 : src_type = "video"
        if src_type_i == 2 : src_type = "image"

        print("src_type : ", src_type)
        setting_changed_list[3] = src_type

    def select_toll(self, toll_i):
        #toll list
        if toll_i == 0 : toll = ""
        if toll_i == 1 : toll = "KLK"
        if toll_i == 2 : toll = "LPT"

        print("src_type : ", toll)
        setting_changed_list[4] = toll








    #-----------------------------------------------------------------------------------
    # cam1 

    def select_mode0(self, src_mode0_i):

        if src_mode0_i == 0 : src_mode0 = ""
        if src_mode0_i == 1 : src_mode0 = "plaza_toll"
        if src_mode0_i == 2 : src_mode0 = "offline"
        print("src_mode0 : ", src_mode0)
        setting_changed_list[5] = src_mode0
        

    def select_lane_type0(self, lane_type0_i):
        if lane_type0_i == 0 : lane_type0 = ""
        if lane_type0_i == 1 : lane_type0 = "offline"
        if lane_type0_i == 2 : lane_type0 = "QUATRIZ"
        if lane_type0_i == 3 : lane_type0 = "TERAS"
        print("lane_type0 : ", lane_type0)
        setting_changed_list[13] = lane_type0

    def rtsp0(self, rtsp1_edited):
        # print(rtsp1_edited)
        if input_src0 is not None:
            setting_changed_list[21] = input_src0
        if setting_changed_list[21] != rtsp1_edited:
            setting_changed_list[21] = rtsp1_edited

    def select_plaza_ID0(self, plaza_ID0_i):
        if plaza_ID0_i == 0 : plaza_ID0 = 000
        if plaza_ID0_i == 1 : plaza_ID0 = 101
        if plaza_ID0_i == 2 : plaza_ID0 = 100
        if plaza_ID0_i == 3 : plaza_ID0 = 801
        if plaza_ID0_i == 4 : plaza_ID0 = 802
        if plaza_ID0_i == 5 : plaza_ID0 = 803
        if plaza_ID0_i == 6 : plaza_ID0 = 804
        if plaza_ID0_i == 7 : plaza_ID0 = 805
        if plaza_ID0_i == 8 : plaza_ID0 = 806
        if plaza_ID0_i == 9 : plaza_ID0 = 807
        if plaza_ID0_i == 10 : plaza_ID0 = 808
        if plaza_ID0_i == 11 : plaza_ID0 = 809

        print("plaza_ID0 : ", plaza_ID0)
        setting_changed_list[29] = plaza_ID0

    
    def lane_ID0(self, lane_ID0_edited):
        if lane_ID0 is not None:
            setting_changed_list[37] = lane_ID0
        if setting_changed_list[37] != lane_ID0_edited:
            setting_changed_list[37] = lane_ID0_edited
        






    #cam 2
    def select_mode1(self, src_mode1_i):
        
        if src_mode1_i == 0 : src_mode1 = ""
        if src_mode1_i == 1 : src_mode1 = "plaza_toll"
        if src_mode1_i == 2 : src_mode1 = "offline"
        print("src_mode1 : ", src_mode1)
        setting_changed_list[6] = src_mode1

    def select_lane_type1(self, lane_type1_i):
        if lane_type1_i == 0 : lane_type1 = ""
        if lane_type1_i == 1 : lane_type1 = "offline"
        if lane_type1_i == 2 : lane_type1 = "QUATRIZ"
        if lane_type1_i == 3 : lane_type1 = "TERAS"
        print("lane_type1 : ", lane_type1)
        setting_changed_list[14] = lane_type1

    def rtsp1(self, rtsp2_edited):
        if input_src1 is not None:
            setting_changed_list[22] = input_src1
        if setting_changed_list[22] != rtsp2_edited:
            setting_changed_list[22] = rtsp2_edited

    def select_plaza_ID1(self, plaza_ID1_i):
        if plaza_ID1_i == 0 : plaza_ID1 = 000
        if plaza_ID1_i == 1 : plaza_ID1 = 101
        if plaza_ID1_i == 2 : plaza_ID1 = 100
        if plaza_ID1_i == 3 : plaza_ID1 = 801
        if plaza_ID1_i == 4 : plaza_ID1 = 802
        if plaza_ID1_i == 5 : plaza_ID1 = 803
        if plaza_ID1_i == 6 : plaza_ID1 = 804
        if plaza_ID1_i == 7 : plaza_ID1 = 805
        if plaza_ID1_i == 8 : plaza_ID1 = 806
        if plaza_ID1_i == 9 : plaza_ID1 = 807
        if plaza_ID1_i == 10 : plaza_ID1 = 808
        if plaza_ID1_i == 11 : plaza_ID1 = 809

        print("plaza_ID1 : ", plaza_ID1)
        setting_changed_list[30] = plaza_ID1

    def lane_ID1(self, lane_ID1_edited):
        if lane_ID1 is not None:
            setting_changed_list[38] = lane_ID1
        if setting_changed_list[38] != lane_ID1_edited:
            setting_changed_list[38] = lane_ID1_edited
        










    #cam 3
    def select_mode2(self, src_mode2_i):
        
        if src_mode2_i == 0 : src_mode2 = ""
        if src_mode2_i == 1 : src_mode2 = "plaza_toll"
        if src_mode2_i == 2 : src_mode2 = "offline"
        print("src_mode2 : ", src_mode2)
        setting_changed_list[7] = src_mode2

    def select_lane_type2(self, lane_type2_i):
        if lane_type2_i == 0 : lane_type2 = ""
        if lane_type2_i == 1 : lane_type2 = "offline"
        if lane_type2_i == 2 : lane_type2 = "QUATRIZ"
        if lane_type2_i == 3 : lane_type2 = "TERAS"
        print("lane_type2 : ", lane_type2)
        setting_changed_list[15] = lane_type2

    def rtsp2(self, rtsp3_edited):
        if input_src2 is not None:
            setting_changed_list[23] = input_src2
        if setting_changed_list[23] != rtsp3_edited:
            setting_changed_list[23] = rtsp3_edited

    def select_plaza_ID2(self, plaza_ID2_i):
        if plaza_ID2_i == 0 : plaza_ID2 = 000
        if plaza_ID2_i == 1 : plaza_ID2 = 101
        if plaza_ID2_i == 2 : plaza_ID2 = 100
        if plaza_ID2_i == 3 : plaza_ID2 = 801
        if plaza_ID2_i == 4 : plaza_ID2 = 802
        if plaza_ID2_i == 5 : plaza_ID2 = 803
        if plaza_ID2_i == 6 : plaza_ID2 = 804
        if plaza_ID2_i == 7 : plaza_ID2 = 805
        if plaza_ID2_i == 8 : plaza_ID2 = 806
        if plaza_ID2_i == 9 : plaza_ID2 = 807
        if plaza_ID2_i == 10 : plaza_ID2 = 808
        if plaza_ID2_i == 11 : plaza_ID2 = 809

        print("plaza_ID2 : ", plaza_ID2)
        setting_changed_list[31] = plaza_ID2


    def lane_ID2(self, lane_ID2_edited):
        if lane_ID2 is not None:
            setting_changed_list[39] = lane_ID2
        if setting_changed_list[39] != lane_ID2_edited:
            setting_changed_list[39] = lane_ID2_edited








    # cam4
    def select_mode3(self, src_mode3_i):

        if src_mode3_i == 0 : src_mode3 = ""
        if src_mode3_i == 1 : src_mode3 = "plaza_toll"
        if src_mode3_i == 2 : src_mode3 = "offline"
        print("src_mode3 : ", src_mode3)
        setting_changed_list[8] = src_mode3

    def select_lane_type3(self, lane_type3_i):
        if lane_type3_i == 0 : lane_type3 = ""
        if lane_type3_i == 1 : lane_type3 = "offline"
        if lane_type3_i == 2 : lane_type3 = "QUATRIZ"
        if lane_type3_i == 3 : lane_type3 = "TERAS"
        print("lane_type3 : ", lane_type3)
        setting_changed_list[16] = lane_type3

    def rtsp3(self, rtsp4_edited):
        if input_src3 is not None:
            setting_changed_list[24] = input_src3
        if setting_changed_list[24] != rtsp4_edited:
            setting_changed_list[24] = rtsp4_edited

    def select_plaza_ID3(self, plaza_ID3_i):
        if plaza_ID3_i == 0 : plaza_ID3 = 000
        if plaza_ID3_i == 1 : plaza_ID3 = 101
        if plaza_ID3_i == 2 : plaza_ID3 = 100
        if plaza_ID3_i == 3 : plaza_ID3 = 801
        if plaza_ID3_i == 4 : plaza_ID3 = 802
        if plaza_ID3_i == 5 : plaza_ID3 = 803
        if plaza_ID3_i == 6 : plaza_ID3 = 804
        if plaza_ID3_i == 7 : plaza_ID3 = 805
        if plaza_ID3_i == 8 : plaza_ID3 = 806
        if plaza_ID3_i == 9 : plaza_ID3 = 807
        if plaza_ID3_i == 10 : plaza_ID3 = 808
        if plaza_ID3_i == 11 : plaza_ID3 = 809

        print("plaza_ID3 : ", plaza_ID3)
        setting_changed_list[32] = plaza_ID3

    
    def lane_ID3(self, lane_ID3_edited):
        if lane_ID3 is not None:
            setting_changed_list[40] = lane_ID3
        if setting_changed_list[40] != lane_ID3_edited:
            setting_changed_list[40] = lane_ID3_edited






    #cam5
        
    def select_mode4(self, src_mode4_i):

        if src_mode4_i == 0 : src_mode4 = ""
        if src_mode4_i == 1 : src_mode4 = "plaza_toll"
        if src_mode4_i == 2 : src_mode4 = "offline"
        print("src_mode4 : ", src_mode4)
        setting_changed_list[9] = src_mode4

    def select_lane_type4(self, lane_type4_i):
        if lane_type4_i == 0 : lane_type4 = ""
        if lane_type4_i == 1 : lane_type4 = "offline"
        if lane_type4_i == 2 : lane_type4 = "QUATRIZ"
        if lane_type4_i == 3 : lane_type4 = "TERAS"
        print("lane_type4 : ", lane_type4)
        setting_changed_list[17] = lane_type4

    def rtsp4(self, rtsp5_edited):
        if input_src4 is not None:
            setting_changed_list[25] = input_src4
        if setting_changed_list[25] != rtsp5_edited:
            setting_changed_list[25] = rtsp5_edited

    def select_plaza_ID4(self, plaza_ID4_i):
        if plaza_ID4_i == 0 : plaza_ID4 = 000
        if plaza_ID4_i == 1 : plaza_ID4 = 101
        if plaza_ID4_i == 2 : plaza_ID4 = 100
        if plaza_ID4_i == 3 : plaza_ID4 = 801
        if plaza_ID4_i == 4 : plaza_ID4 = 802
        if plaza_ID4_i == 5 : plaza_ID4 = 803
        if plaza_ID4_i == 6 : plaza_ID4 = 804
        if plaza_ID4_i == 7 : plaza_ID4 = 805
        if plaza_ID4_i == 8 : plaza_ID4 = 806
        if plaza_ID4_i == 9 : plaza_ID4 = 807
        if plaza_ID4_i == 10 : plaza_ID4 = 808
        if plaza_ID4_i == 11 : plaza_ID4 = 809

        print("plaza_ID4 : ", plaza_ID4)
        setting_changed_list[33] = plaza_ID4

    def lane_ID4(self, lane_ID4_edited):
        if lane_ID4 is not None:
            setting_changed_list[41] = lane_ID4
        if setting_changed_list[41] != lane_ID4_edited:
            setting_changed_list[41] = lane_ID4_edited



    #cam 6
    def select_mode5(self, src_mode5_i):

        if src_mode5_i == 0 : src_mode5 = ""
        if src_mode5_i == 1 : src_mode5 = "plaza_toll"
        if src_mode5_i == 2 : src_mode5 = "offline"
        print("src_mode5 : ", src_mode5)
        setting_changed_list[10] = src_mode5

    def select_lane_type5(self, lane_type5_i):
        if lane_type5_i == 0 : lane_type5 = ""
        if lane_type5_i == 1 : lane_type5 = "offline"
        if lane_type5_i == 2 : lane_type5 = "QUATRIZ"
        if lane_type5_i == 3 : lane_type5 = "TERAS"
        print("lane_type5 : ", lane_type5)
        setting_changed_list[18] = lane_type5

    def rtsp5(self, rtsp6_edited):
        if input_src4 is not None:
            setting_changed_list[26] = input_src4
        if setting_changed_list[26] != rtsp6_edited:
            setting_changed_list[26] = rtsp6_edited

    def select_plaza_ID5(self, plaza_ID5_i):
        if plaza_ID5_i == 0 : plaza_ID5 = 000
        if plaza_ID5_i == 1 : plaza_ID5 = 101
        if plaza_ID5_i == 2 : plaza_ID5 = 100
        if plaza_ID5_i == 3 : plaza_ID5 = 801
        if plaza_ID5_i == 4 : plaza_ID5 = 802
        if plaza_ID5_i == 5 : plaza_ID5 = 803
        if plaza_ID5_i == 6 : plaza_ID5 = 804
        if plaza_ID5_i == 7 : plaza_ID5 = 805
        if plaza_ID5_i == 8 : plaza_ID5 = 806
        if plaza_ID5_i == 9 : plaza_ID5 = 807
        if plaza_ID5_i == 10 : plaza_ID5 = 808
        if plaza_ID5_i == 11 : plaza_ID5 = 809

        print("plaza_ID5 : ", plaza_ID5)
        setting_changed_list[34] = plaza_ID5

    def lane_ID5(self, lane_ID5_edited):
        if lane_ID5 is not None:
            setting_changed_list[42] = lane_ID5
        if setting_changed_list[42] != lane_ID5_edited:
            setting_changed_list[42] = lane_ID5_edited




    #cam 7
    def select_mode6(self, src_mode6_i):

        if src_mode6_i == 0 : src_mode6 = ""
        if src_mode6_i == 1 : src_mode6 = "plaza_toll"
        if src_mode6_i == 2 : src_mode6 = "offline"
        print("src_mode6 : ", src_mode6)
        setting_changed_list[11] = src_mode6

    def select_lane_type6(self, lane_type6_i):
        if lane_type6_i == 0 : lane_type6 = ""
        if lane_type6_i == 1 : lane_type6 = "offline"
        if lane_type6_i == 2 : lane_type6 = "QUATRIZ"
        if lane_type6_i == 3 : lane_type6 = "TERAS"
        print("lane_type6 : ", lane_type6)
        setting_changed_list[19] = lane_type6

    def rtsp6(self, rtsp7_edited):
        if input_src5 is not None:
            setting_changed_list[27] = input_src5
        if setting_changed_list[27] != rtsp7_edited:
            setting_changed_list[27] = rtsp7_edited


    def select_plaza_ID6(self, plaza_ID6_i):
        if plaza_ID6_i == 0 : plaza_ID6 = 000
        if plaza_ID6_i == 1 : plaza_ID6 = 101
        if plaza_ID6_i == 2 : plaza_ID6 = 100
        if plaza_ID6_i == 3 : plaza_ID6 = 801
        if plaza_ID6_i == 4 : plaza_ID6 = 802
        if plaza_ID6_i == 5 : plaza_ID6 = 803
        if plaza_ID6_i == 6 : plaza_ID6 = 804
        if plaza_ID6_i == 7 : plaza_ID6 = 805
        if plaza_ID6_i == 8 : plaza_ID6 = 806
        if plaza_ID6_i == 9 : plaza_ID6 = 807
        if plaza_ID6_i == 10 : plaza_ID6 = 808
        if plaza_ID6_i == 11 : plaza_ID6 = 809

        print("plaza_ID6 : ", plaza_ID6)
        setting_changed_list[35] = plaza_ID6

    def lane_ID6(self, lane_ID6_edited):
        if lane_ID6 is not None:
            setting_changed_list[43] = lane_ID6
        if setting_changed_list[43] != lane_ID6_edited:
            setting_changed_list[43] = lane_ID6_edited




    
    def select_mode7(self, src_mode7_i):
        #cam 8
        if src_mode7_i == 0 : src_mode7 = ""
        if src_mode7_i == 1 : src_mode7 = "plaza_toll"
        if src_mode7_i == 2 : src_mode7 = "offline"
        print("src_mode7 : ", src_mode7)
        setting_changed_list[12] = src_mode7

    def select_lane_type7(self, lane_type7_i):
        if lane_type7_i == 0 : lane_type7 = ""
        if lane_type7_i == 1 : lane_type7 = "offline"
        if lane_type7_i == 2 : lane_type7 = "QUATRIZ"
        if lane_type7_i == 3 : lane_type7 = "TERAS"
        print("lane_type7 : ", lane_type7)
        setting_changed_list[20] = lane_type7

    def rtsp7(self, rtsp8_edited):
        if input_src6 is not None:
            setting_changed_list[28] = input_src6
        if setting_changed_list[28] != rtsp8_edited:
            setting_changed_list[28] = rtsp8_edited

    def select_plaza_ID7(self, plaza_ID7_i):
        if plaza_ID7_i == 0 : plaza_ID7 = 000
        if plaza_ID7_i == 1 : plaza_ID7 = 101
        if plaza_ID7_i == 2 : plaza_ID7 = 100
        if plaza_ID7_i == 3 : plaza_ID7 = 801
        if plaza_ID7_i == 4 : plaza_ID7 = 802
        if plaza_ID7_i == 5 : plaza_ID7 = 803
        if plaza_ID7_i == 6 : plaza_ID7 = 804
        if plaza_ID7_i == 7 : plaza_ID7 = 805
        if plaza_ID7_i == 8 : plaza_ID7 = 806
        if plaza_ID7_i == 9 : plaza_ID7 = 807
        if plaza_ID7_i == 10 : plaza_ID7 = 808
        if plaza_ID7_i == 11 : plaza_ID7 = 809

        setting_changed_list[36] = plaza_ID7

    def lane_ID7(self, lane_ID7_edited):
        if lane_ID7 is not None:
            setting_changed_list[44] = lane_ID7
            print("UPPER CASE : ", setting_changed_list[44])
        if setting_changed_list[44] != lane_ID7_edited:
            setting_changed_list[44] = lane_ID7_edited


    def pushbutton_save_(self):

        print(f"\nsetting_changed_list : {len(setting_changed_list)}\n",setting_changed_list)
        
        main_folder_path = os.path.dirname(os.getcwd())
        
        #update value based on changed value
        config = configparser.ConfigParser()
        if os.path.isfile(config_path):
            config.read(config_path)
        else:
            if os.path.isfile(setting_path):
                config.read(setting_path)
        
        
        config.set('host_setup', 'host_ip', str(setting_changed_list[0]))
        config.set('host_setup', 'host_port', str(setting_changed_list[1]))
        config.set('host_setup', 'host_port2', str(setting_changed_list[2]))
        config.set('src', 'input_type', str(setting_changed_list[3]))
        config.set('toll', 'toll_input', str(setting_changed_list[4]))

        config.set('src_mode','input_mode0', str(setting_changed_list[5]))
        config.set('src_mode','input_mode1', str(setting_changed_list[6]))
        config.set('src_mode','input_mode2', str(setting_changed_list[7]))
        config.set('src_mode','input_mode3', str(setting_changed_list[8]))
        config.set('src_mode','input_mode4', str(setting_changed_list[9]))
        config.set('src_mode','input_mode5', str(setting_changed_list[10]))
        config.set('src_mode','input_mode6', str(setting_changed_list[11]))
        config.set('src_mode','input_mode7', str(setting_changed_list[12]))

        config.set('lane_type','lane_type0', str(setting_changed_list[13]))
        config.set('lane_type','lane_type1', str(setting_changed_list[14]))
        config.set('lane_type','lane_type2', str(setting_changed_list[15]))
        config.set('lane_type','lane_type3', str(setting_changed_list[16]))
        config.set('lane_type','lane_type4', str(setting_changed_list[17]))
        config.set('lane_type','lane_type5', str(setting_changed_list[18]))
        config.set('lane_type','lane_type6', str(setting_changed_list[19]))
        config.set('lane_type','lane_type7', str(setting_changed_list[20]))

        #------------------------------------------------------------------
        #input source

        print("input_src0" ,input_src0)
        print("setting_changed_list[21] : ",setting_changed_list[21])


        config.set('src_input', 'input_src0', str(setting_changed_list[21]))
        config.set('src_input', 'input_src1', str(setting_changed_list[22]))
        config.set('src_input', 'input_src2', str(setting_changed_list[23]))
        config.set('src_input', 'input_src3', str(setting_changed_list[24]))
        config.set('src_input', 'input_src4', str(setting_changed_list[25]))
        config.set('src_input', 'input_src5', str(setting_changed_list[26]))
        config.set('src_input', 'input_src6', str(setting_changed_list[27]))
        config.set('src_input', 'input_src7', str(setting_changed_list[28]))

        #-------------------------------------------------------------------
        #source id
        config.set('src_id', 'input_id0', str(setting_changed_list[29]) + "." + str(setting_changed_list[37]).upper())
        config.set('src_id', 'input_id1', str(setting_changed_list[30]) + "." + str(setting_changed_list[38]).upper())
        config.set('src_id', 'input_id2', str(setting_changed_list[31]) + "." + str(setting_changed_list[39]).upper())
        config.set('src_id', 'input_id3', str(setting_changed_list[32]) + "." + str(setting_changed_list[40]).upper())
        config.set('src_id', 'input_id4', str(setting_changed_list[33]) + "." + str(setting_changed_list[41]).upper())
        config.set('src_id', 'input_id5', str(setting_changed_list[34]) + "." + str(setting_changed_list[42]).upper())
        config.set('src_id', 'input_id6', str(setting_changed_list[35]) + "." + str(setting_changed_list[43]).upper())
        config.set('src_id', 'input_id7', str(setting_changed_list[36]) + "." + str(setting_changed_list[44]).upper())



        with open(config_path, 'w') as file:
                config.write(file)



        # /home/delloyd/1.ANPR/LPT/2.main8v7-live_at_LPT/setting_gui/icon" 

        chime.success()
        os.system('notify-send -i /home/$USER/Tol_Master/setting_gui/icon/check.png "Setting saved." "Restart ANPR !!!"')


        
    
    
    
    
    
    
    
    
    
