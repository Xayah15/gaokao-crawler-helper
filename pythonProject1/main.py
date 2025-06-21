# -*- coding: utf-8 -*-
import json
import os
import random
import time
import pandas as pd
from PyQt6.QtCore import QThread, pyqtSignal, QUrl
from requests.exceptions import ProxyError, SSLError
import requests
from PyQt6.QtGui import QDesktopServices, QIcon
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6 import QtWidgets, QtCore, QtGui
import sys
import csv
from PyQt6.QtWidgets import QApplication, QStyleFactory
import vis_method
from ana_method import ana_window, find_files, ana_window_score
from sort_method import group_csv

url = 'https://api.zjzw.cn/web/api'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "close"
}
proxies = {
    "https": "http://111.177.63.86:8888",
}
# 当前为提升效率，未使用代理。若IP被封禁再使用。
# resp = requests.post(url=url, params=special_params, headers=headers, proxies=proxies)

class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        self.setupUi(self)
        self.setWindowIcon(QIcon('icon/VIP.png'))  # 设置程序图标
        self.tableWidget_3.setColumnWidth(5, 220)

        self.comboBox_pro_2.activated.connect(self.onProvinceActivated)  # 动态更新 根据省份提供不同的子选项

        self.pushButton_plan.clicked.connect(self.school_plan)
        self.pushButton_score.clicked.connect(self.special_score)
        self.pushButton_check.clicked.connect(self.check_net)
        self.pushButton_intro.clicked.connect(self.school_intro)
        self.pushButton_ana.clicked.connect(self.school_ana)
        self.pushButton_aspire.clicked.connect(self.aspire)

        self.textEdit_time.setReadOnly(True)


        self.statusBar().showMessage(' 当前可查询年份:2018-2024。所有数据来源于网络公开平台，仅供学习与参考。')


        self.action_vis.triggered.connect(self.vis)
        self.action_ana.triggered.connect(self.show_ana)
        self.action_ana_score.triggered.connect(self.show_ana_score)

        self.myth_plan = ThreadPlan()
        self.myth_plan.signal_csv.connect(self.net_plan)
        self.myth_plan.signal_time.connect(self.show_time)

        self.myth_score = ThreadScore()
        self.myth_score.signal_csv.connect(self.net_score)
        self.myth_score.signal_time.connect(self.show_time)

        self.myth_ana = ThreadAna()
        self.myth_ana.signal_csv.connect(self.get_ana)
        self.myth_ana.signal_time.connect(self.show_time)

        self.myth_check = ThreadChecknet()
        self.myth_check.signal_time.connect(self.net_check_show)

        self.myth_intro = ThreadIntro()
        self.myth_intro.signal_intro.connect(self.show_intro)
        self.myth_intro.signal_time.connect(self.show_time)

        self.myth_aspire = ThreadAspire()
        self.myth_aspire.signal_csv.connect(self.show_aspire)
        self.myth_aspire.signal_time.connect(self.show_time)

        QApplication.setStyle(QStyleFactory.create('Fusion'))

    # UISET
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(970, 670)
        MainWindow.setMinimumSize(QtCore.QSize(970, 650))
        MainWindow.setAcceptDrops(False)
        icon = QtGui.QIcon.fromTheme("address-book-new")
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("selection-color: rgb(83, 250, 250);")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_4.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_4.setMaximumSize(QtCore.QSize(16777215, 80))
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.textEdit_time = QtWidgets.QTextEdit(parent=self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_time.sizePolicy().hasHeightForWidth())
        self.textEdit_time.setSizePolicy(sizePolicy)
        self.textEdit_time.setMinimumSize(QtCore.QSize(335, 40))
        self.textEdit_time.setMaximumSize(QtCore.QSize(800, 65))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setStrikeOut(False)
        self.textEdit_time.setFont(font)
        self.textEdit_time.setReadOnly(True)
        self.textEdit_time.setObjectName("textEdit_time")
        self.gridLayout_4.addWidget(self.textEdit_time, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_4, 0, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_2.setEnabled(True)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 70))
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 74))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.lineEdit_sch = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.lineEdit_sch.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_sch.setObjectName("lineEdit_sch")
        self.gridLayout.addWidget(self.lineEdit_sch, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.lineEdit_year = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.lineEdit_year.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_year.setClearButtonEnabled(False)
        self.lineEdit_year.setObjectName("lineEdit_year")
        self.gridLayout.addWidget(self.lineEdit_year, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 4, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(parent=self.groupBox_2)
        self.comboBox.setMinimumSize(QtCore.QSize(70, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 1, 4, 1, 1)
        self.comboBox_pro = QtWidgets.QComboBox(parent=self.groupBox_2)
        self.comboBox_pro.setMinimumSize(QtCore.QSize(90, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_pro.setFont(font)
        self.comboBox_pro.setObjectName("comboBox_pro")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.comboBox_pro.addItem("")
        self.gridLayout.addWidget(self.comboBox_pro, 1, 1, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_2, 2, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 70))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_intro = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_intro.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.pushButton_intro.setFont(font)
        self.pushButton_intro.setObjectName("pushButton_intro")
        self.gridLayout_3.addWidget(self.pushButton_intro, 0, 2, 1, 1)
        self.pushButton_score = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_score.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.pushButton_score.setFont(font)
        self.pushButton_score.setStyleSheet("")
        self.pushButton_score.setObjectName("pushButton_score")
        self.gridLayout_3.addWidget(self.pushButton_score, 0, 0, 1, 1)
        self.pushButton_plan = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_plan.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.pushButton_plan.setFont(font)
        self.pushButton_plan.setObjectName("pushButton_plan")
        self.gridLayout_3.addWidget(self.pushButton_plan, 0, 1, 1, 1)
        self.pushButton_ana = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_ana.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.pushButton_ana.setFont(font)
        self.pushButton_ana.setObjectName("pushButton_ana")
        self.gridLayout_3.addWidget(self.pushButton_ana, 0, 3, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_3, 2, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 40))
        self.groupBox.setMaximumSize(QtCore.QSize(1200, 80))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_check = QtWidgets.QPushButton(parent=self.groupBox)
        self.pushButton_check.setMinimumSize(QtCore.QSize(0, 46))
        font = QtGui.QFont()
        font.setBold(False)
        self.pushButton_check.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icon/attachment.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_check.setIcon(icon)
        self.pushButton_check.setObjectName("pushButton_check")
        self.gridLayout_2.addWidget(self.pushButton_check, 0, 0, 1, 1)
        self.label_check = QtWidgets.QLabel(parent=self.groupBox)
        self.label_check.setObjectName("label_check")
        self.gridLayout_2.addWidget(self.label_check, 0, 1, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(950, 440))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.widget = QtWidgets.QWidget(parent=self.tab)
        self.widget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.widget.setObjectName("widget")
        self.gridLayout_5.addWidget(self.widget, 1, 1, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(parent=self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableWidget.setFont(font)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setUnderline(False)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.gridLayout_5.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.tableWidget_2 = QtWidgets.QTableWidget(parent=self.tab_2)
        self.tableWidget_2.setAutoFillBackground(False)
        self.tableWidget_2.setLineWidth(1)
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setUnderline(False)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        self.gridLayout_6.addWidget(self.tableWidget_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.tableWidget_4 = QtWidgets.QTableWidget(parent=self.tab_3)
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(0)
        self.tableWidget_4.setRowCount(12)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(11, item)
        self.gridLayout_8.addWidget(self.tableWidget_4, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.pushButton_aspire = QtWidgets.QPushButton(parent=self.tab_4)
        self.pushButton_aspire.setMinimumSize(QtCore.QSize(150, 27))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_aspire.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../icon/fabulous.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_aspire.setIcon(icon1)
        self.pushButton_aspire.setObjectName("pushButton_aspire")
        self.gridLayout_9.addWidget(self.pushButton_aspire, 1, 6, 1, 1)
        self.tableWidget_3 = QtWidgets.QTableWidget(parent=self.tab_4)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(8)
        self.tableWidget_3.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(7, item)
        self.gridLayout_9.addWidget(self.tableWidget_3, 2, 0, 1, 7)
        self.comboBox_pro_2 = QtWidgets.QComboBox(parent=self.tab_4)
        self.comboBox_pro_2.setMinimumSize(QtCore.QSize(100, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comboBox_pro_2.setFont(font)
        self.comboBox_pro_2.setObjectName("comboBox_pro_2")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.comboBox_pro_2.addItem("")
        self.gridLayout_9.addWidget(self.comboBox_pro_2, 1, 0, 1, 1)
        self.comboBox_subject = QtWidgets.QComboBox(parent=self.tab_4)
        self.comboBox_subject.setMinimumSize(QtCore.QSize(130, 25))
        self.comboBox_subject.setObjectName("comboBox_subject")
        self.comboBox_subject.addItem("")
        self.comboBox_subject.addItem("")
        self.gridLayout_9.addWidget(self.comboBox_subject, 1, 1, 1, 1)
        self.comboBox_batch = QtWidgets.QComboBox(parent=self.tab_4)
        self.comboBox_batch.setMinimumSize(QtCore.QSize(100, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comboBox_batch.setFont(font)
        self.comboBox_batch.setObjectName("comboBox_batch")
        self.comboBox_batch.addItem("")
        self.comboBox_batch.addItem("")
        self.comboBox_batch.addItem("")
        self.gridLayout_9.addWidget(self.comboBox_batch, 1, 5, 1, 1)
        self.lineEdit_sec = QtWidgets.QLineEdit(parent=self.tab_4)
        self.lineEdit_sec.setObjectName("lineEdit_sec")
        self.gridLayout_9.addWidget(self.lineEdit_sec, 1, 3, 1, 1)
        self.lineEdit_score = QtWidgets.QLineEdit(parent=self.tab_4)
        self.lineEdit_score.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEdit_score.setObjectName("lineEdit_score")
        self.gridLayout_9.addWidget(self.lineEdit_score, 1, 4, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.tab_4)
        self.label_5.setObjectName("label_5")
        self.gridLayout_9.addWidget(self.label_5, 0, 0, 1, 5)
        self.tabWidget.addTab(self.tab_4, "")
        self.gridLayout_7.addWidget(self.tabWidget, 3, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.action_ana = QtGui.QAction(parent=MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../icon/chart-bar.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_ana.setIcon(icon2)
        self.action_ana.setObjectName("action_ana")
        self.action_help = QtGui.QAction(parent=MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../icon/help.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_help.setIcon(icon3)
        self.action_help.setObjectName("action_help")
        self.action_ana_score = QtGui.QAction(parent=MainWindow)
        self.action_ana_score.setIcon(icon2)
        self.action_ana_score.setObjectName("action_ana_score")
        self.action_clear = QtGui.QAction(parent=MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../icon/refresh.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_clear.setIcon(icon4)
        self.action_clear.setObjectName("action_clear")
        self.action_vis = QtGui.QAction(parent=MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../icon/data-view.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_vis.setIcon(icon5)
        self.action_vis.setObjectName("action_vis")
        self.toolBar.addAction(self.action_vis)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_ana)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_ana_score)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_clear)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_help)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.action_clear.triggered.connect(self.tableWidget.clearContents) # type: ignore
        self.action_clear.triggered.connect(self.tableWidget_2.clearContents) # type: ignore
        self.action_clear.triggered.connect(self.lineEdit_sch.clear) # type: ignore
        self.pushButton_score.clicked.connect(self.tableWidget.setFocus) # type: ignore
        self.pushButton_plan.clicked.connect(self.tableWidget_2.setFocus) # type: ignore
        self.action_clear.triggered.connect(self.lineEdit_year.clear) # type: ignore
        self.action_clear.triggered.connect(self.textEdit_time.clear) # type: ignore
        self.action_clear.triggered.connect(self.tableWidget_3.clearContents) # type: ignore
        self.action_clear.triggered.connect(self.lineEdit_sec.clear) # type: ignore
        self.action_clear.triggered.connect(self.tableWidget_4.clearContents) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.lineEdit_sch, self.lineEdit_year)
        MainWindow.setTabOrder(self.lineEdit_year, self.comboBox)
        MainWindow.setTabOrder(self.comboBox, self.pushButton_plan)
        MainWindow.setTabOrder(self.pushButton_plan, self.pushButton_score)
        MainWindow.setTabOrder(self.pushButton_score, self.pushButton_check)
        MainWindow.setTabOrder(self.pushButton_check, self.tabWidget)
        MainWindow.setTabOrder(self.tabWidget, self.tableWidget)
        MainWindow.setTabOrder(self.tableWidget, self.textEdit_time)
        MainWindow.setTabOrder(self.textEdit_time, self.tableWidget_2)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "高考助手"))
        self.textEdit_time.setPlaceholderText(_translate("MainWindow", "此处为操作提示框，当前没有查询操作"))
        self.label_2.setText(_translate("MainWindow", "考生省份"))
        self.lineEdit_sch.setPlaceholderText(_translate("MainWindow", "输入完整学校名称"))
        self.label_4.setText(_translate("MainWindow", "年"))
        self.lineEdit_year.setPlaceholderText(_translate("MainWindow", "2018-2024"))
        self.label_3.setText(_translate("MainWindow", "类型"))
        self.label.setText(_translate("MainWindow", "学校名称"))
        self.comboBox.setItemText(0, _translate("MainWindow", "理科"))
        self.comboBox.setItemText(1, _translate("MainWindow", "文科"))
        self.comboBox.setItemText(2, _translate("MainWindow", "综合"))
        self.comboBox.setItemText(3, _translate("MainWindow", "物理类"))
        self.comboBox.setItemText(4, _translate("MainWindow", "历史类"))
        self.comboBox_pro.setItemText(0, _translate("MainWindow", "河南"))
        self.comboBox_pro.setItemText(1, _translate("MainWindow", "河北"))
        self.comboBox_pro.setItemText(2, _translate("MainWindow", "北京"))
        self.comboBox_pro.setItemText(3, _translate("MainWindow", "天津"))
        self.comboBox_pro.setItemText(4, _translate("MainWindow", "山东"))
        self.comboBox_pro.setItemText(5, _translate("MainWindow", "山西"))
        self.comboBox_pro.setItemText(6, _translate("MainWindow", "内蒙古"))
        self.comboBox_pro.setItemText(7, _translate("MainWindow", "辽宁"))
        self.comboBox_pro.setItemText(8, _translate("MainWindow", "吉林"))
        self.comboBox_pro.setItemText(9, _translate("MainWindow", "黑龙江"))
        self.comboBox_pro.setItemText(10, _translate("MainWindow", "上海"))
        self.comboBox_pro.setItemText(11, _translate("MainWindow", "江苏"))
        self.comboBox_pro.setItemText(12, _translate("MainWindow", "浙江"))
        self.comboBox_pro.setItemText(13, _translate("MainWindow", "安徽"))
        self.comboBox_pro.setItemText(14, _translate("MainWindow", "福建"))
        self.comboBox_pro.setItemText(15, _translate("MainWindow", "江西"))
        self.comboBox_pro.setItemText(16, _translate("MainWindow", "湖北"))
        self.comboBox_pro.setItemText(17, _translate("MainWindow", "湖南"))
        self.comboBox_pro.setItemText(18, _translate("MainWindow", "广东"))
        self.comboBox_pro.setItemText(19, _translate("MainWindow", "广西"))
        self.comboBox_pro.setItemText(20, _translate("MainWindow", "海南"))
        self.comboBox_pro.setItemText(21, _translate("MainWindow", "重庆"))
        self.comboBox_pro.setItemText(22, _translate("MainWindow", "四川"))
        self.comboBox_pro.setItemText(23, _translate("MainWindow", "贵州"))
        self.comboBox_pro.setItemText(24, _translate("MainWindow", "云南"))
        self.comboBox_pro.setItemText(25, _translate("MainWindow", "西藏"))
        self.comboBox_pro.setItemText(26, _translate("MainWindow", "陕西"))
        self.comboBox_pro.setItemText(27, _translate("MainWindow", "甘肃"))
        self.comboBox_pro.setItemText(28, _translate("MainWindow", "青海"))
        self.comboBox_pro.setItemText(29, _translate("MainWindow", "宁夏"))
        self.comboBox_pro.setItemText(30, _translate("MainWindow", "新疆"))
        self.pushButton_intro.setText(_translate("MainWindow", "查学校简介"))
        self.pushButton_score.setText(_translate("MainWindow", "查专业分数线"))
        self.pushButton_plan.setText(_translate("MainWindow", "查招生计划"))
        self.pushButton_ana.setText(_translate("MainWindow", "数据分析"))
        self.pushButton_check.setText(_translate("MainWindow", "检测网络状态"))
        self.label_check.setText(_translate("MainWindow", "使用前请检测网络状态，若网络异常，请1分钟后重试。"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "专业"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "平均分"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "最低分"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "最低位次"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "批次"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "专业分数线"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "专业"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "招生人数"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "学制"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "学费（年）"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "批次"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "招生计划"))
        item = self.tableWidget_4.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "学校名称"))
        item = self.tableWidget_4.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "地址"))
        item = self.tableWidget_4.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "网站"))
        item = self.tableWidget_4.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "电话"))
        item = self.tableWidget_4.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "邮箱"))
        item = self.tableWidget_4.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "归属"))
        item = self.tableWidget_4.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "校训"))
        item = self.tableWidget_4.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "类型"))
        item = self.tableWidget_4.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "占地面积"))
        item = self.tableWidget_4.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "软科排名"))
        item = self.tableWidget_4.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "校友会排名"))
        item = self.tableWidget_4.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "办学层次"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "学校简介"))
        self.pushButton_aspire.setText(_translate("MainWindow", "志愿推荐"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "学校名称"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "填报建议"))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "学校代码"))
        item = self.tableWidget_3.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "办学性质"))
        item = self.tableWidget_3.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "学校类型"))
        item = self.tableWidget_3.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "历年情况(分数、位次、招生人数)"))
        item = self.tableWidget_3.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "招生计划（人）"))
        item = self.tableWidget_3.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "招生专业"))
        self.comboBox_pro_2.setItemText(0, _translate("MainWindow", "河南"))
        self.comboBox_pro_2.setItemText(1, _translate("MainWindow", "河北"))
        self.comboBox_pro_2.setItemText(2, _translate("MainWindow", "北京"))
        self.comboBox_pro_2.setItemText(3, _translate("MainWindow", "天津"))
        self.comboBox_pro_2.setItemText(4, _translate("MainWindow", "山东"))
        self.comboBox_pro_2.setItemText(5, _translate("MainWindow", "山西"))
        self.comboBox_pro_2.setItemText(6, _translate("MainWindow", "内蒙古"))
        self.comboBox_pro_2.setItemText(7, _translate("MainWindow", "辽宁"))
        self.comboBox_pro_2.setItemText(8, _translate("MainWindow", "吉林"))
        self.comboBox_pro_2.setItemText(9, _translate("MainWindow", "黑龙江"))
        self.comboBox_pro_2.setItemText(10, _translate("MainWindow", "上海"))
        self.comboBox_pro_2.setItemText(11, _translate("MainWindow", "江苏"))
        self.comboBox_pro_2.setItemText(12, _translate("MainWindow", "浙江"))
        self.comboBox_pro_2.setItemText(13, _translate("MainWindow", "安徽"))
        self.comboBox_pro_2.setItemText(14, _translate("MainWindow", "福建"))
        self.comboBox_pro_2.setItemText(15, _translate("MainWindow", "江西"))
        self.comboBox_pro_2.setItemText(16, _translate("MainWindow", "湖北"))
        self.comboBox_pro_2.setItemText(17, _translate("MainWindow", "湖南"))
        self.comboBox_pro_2.setItemText(18, _translate("MainWindow", "广东"))
        self.comboBox_pro_2.setItemText(19, _translate("MainWindow", "广西"))
        self.comboBox_pro_2.setItemText(20, _translate("MainWindow", "海南"))
        self.comboBox_pro_2.setItemText(21, _translate("MainWindow", "重庆"))
        self.comboBox_pro_2.setItemText(22, _translate("MainWindow", "四川"))
        self.comboBox_pro_2.setItemText(23, _translate("MainWindow", "贵州"))
        self.comboBox_pro_2.setItemText(24, _translate("MainWindow", "云南"))
        self.comboBox_pro_2.setItemText(25, _translate("MainWindow", "西藏"))
        self.comboBox_pro_2.setItemText(26, _translate("MainWindow", "陕西"))
        self.comboBox_pro_2.setItemText(27, _translate("MainWindow", "甘肃"))
        self.comboBox_pro_2.setItemText(28, _translate("MainWindow", "青海"))
        self.comboBox_pro_2.setItemText(29, _translate("MainWindow", "宁夏"))
        self.comboBox_pro_2.setItemText(30, _translate("MainWindow", "新疆"))
        self.comboBox_subject.setItemText(0, _translate("MainWindow", "理科"))
        self.comboBox_subject.setItemText(1, _translate("MainWindow", "文科"))
        self.comboBox_batch.setItemText(0, _translate("MainWindow", "本科一批"))
        self.comboBox_batch.setItemText(1, _translate("MainWindow", "本科二批"))
        self.comboBox_batch.setItemText(2, _translate("MainWindow", "专科批"))
        self.lineEdit_sec.setPlaceholderText(_translate("MainWindow", "考生位次"))
        self.lineEdit_score.setPlaceholderText(_translate("MainWindow", "考生对应2023年分数"))
        self.label_5.setText(_translate("MainWindow", "河南考生只需要填写考生位次，无需填写对应2023年分数。其他省份只需填写对应2023年分数。"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "填报志愿"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_ana.setText(_translate("MainWindow", "数据分析（最低位次）"))
        self.action_ana.setToolTip(_translate("MainWindow", "统计最低位次变化情况（F2）"))
        self.action_ana.setShortcut(_translate("MainWindow", "F2"))
        self.action_help.setText(_translate("MainWindow", "帮助（ 暂未启用，有疑问请联系1277252513@qq.com ）"))
        self.action_help.setToolTip(_translate("MainWindow", "查看使用说明"))
        self.action_ana_score.setText(_translate("MainWindow", "数据分析（最低分）"))
        self.action_ana_score.setToolTip(_translate("MainWindow", "统计最低分变化情况（F3）"))
        self.action_ana_score.setShortcut(_translate("MainWindow", "F3"))
        self.action_clear.setText(_translate("MainWindow", "刷新"))
        self.action_clear.setToolTip(_translate("MainWindow", "刷新页面（F5）"))
        self.action_clear.setShortcut(_translate("MainWindow", "F5"))
        self.action_vis.setText(_translate("MainWindow", "专业分数线统计"))
        self.action_vis.setToolTip(_translate("MainWindow", "专业分数线可视化（F1）"))
        self.action_vis.setShortcut(_translate("MainWindow", "F1"))





    # 动态更新 根据省份展示下位选项
    def onProvinceActivated(self, province):
        province = self.comboBox_pro_2.currentText()
        self.comboBox_subject.clear()
        self.comboBox_batch.clear()

        if province == "河南":
            self.comboBox_subject.addItem("理科")
            self.comboBox_subject.addItem("文科")
            self.comboBox_batch.addItem("本科一批")
            self.comboBox_batch.addItem("本科二批")
            self.comboBox_batch.addItem("专科批")
        elif province == "山东":
            self.comboBox_subject.addItem("物理,化学,生物")
            self.comboBox_subject.addItem("物理,化学,政治")
            self.comboBox_subject.addItem("物理,化学,历史")
            self.comboBox_subject.addItem("物理,化学,地理")
            self.comboBox_subject.addItem("物理,生物,政治")
            self.comboBox_subject.addItem("物理,生物,历史")
            self.comboBox_subject.addItem("物理,生物,地理")
            self.comboBox_subject.addItem("物理,政治,历史")
            self.comboBox_subject.addItem("物理,政治,地理")
            self.comboBox_subject.addItem("物理,历史,地理")
            self.comboBox_subject.addItem("化学,生物,政治")
            self.comboBox_subject.addItem("化学,生物,历史")
            self.comboBox_subject.addItem("化学,生物,地理")
            self.comboBox_subject.addItem("化学,政治,历史")
            self.comboBox_subject.addItem("化学,政治,地理")
            self.comboBox_subject.addItem("化学,历史,地理")
            self.comboBox_subject.addItem("生物,政治,历史")
            self.comboBox_subject.addItem("生物,政治,地理")
            self.comboBox_subject.addItem("生物,历史,地理")
            self.comboBox_subject.addItem("政治,历史,地理")
            self.comboBox_batch.addItem("普通类一段")
            self.comboBox_batch.addItem("普通类二段")
        elif province == "北京":
            self.comboBox_subject.addItem("物理,化学,生物")
            self.comboBox_subject.addItem("物理,化学,政治")
            self.comboBox_subject.addItem("物理,化学,历史")
            self.comboBox_subject.addItem("物理,化学,地理")
            self.comboBox_subject.addItem("物理,生物,政治")
            self.comboBox_subject.addItem("物理,生物,历史")
            self.comboBox_subject.addItem("物理,生物,地理")
            self.comboBox_subject.addItem("物理,政治,历史")
            self.comboBox_subject.addItem("物理,政治,地理")
            self.comboBox_subject.addItem("物理,历史,地理")
            self.comboBox_subject.addItem("化学,生物,政治")
            self.comboBox_subject.addItem("化学,生物,历史")
            self.comboBox_subject.addItem("化学,生物,地理")
            self.comboBox_subject.addItem("化学,政治,历史")
            self.comboBox_subject.addItem("化学,政治,地理")
            self.comboBox_subject.addItem("化学,历史,地理")
            self.comboBox_subject.addItem("生物,政治,历史")
            self.comboBox_subject.addItem("生物,政治,地理")
            self.comboBox_subject.addItem("生物,历史,地理")
            self.comboBox_subject.addItem("政治,历史,地理")
            self.comboBox_batch.addItem("本科批")
        elif province == "上海":
            self.comboBox_subject.addItem("物理,化学,生物")
            self.comboBox_subject.addItem("物理,化学,政治")
            self.comboBox_subject.addItem("物理,化学,历史")
            self.comboBox_subject.addItem("物理,化学,地理")
            self.comboBox_subject.addItem("物理,生物,政治")
            self.comboBox_subject.addItem("物理,生物,历史")
            self.comboBox_subject.addItem("物理,生物,地理")
            self.comboBox_subject.addItem("物理,政治,历史")
            self.comboBox_subject.addItem("物理,政治,地理")
            self.comboBox_subject.addItem("物理,历史,地理")
            self.comboBox_subject.addItem("化学,生物,政治")
            self.comboBox_subject.addItem("化学,生物,历史")
            self.comboBox_subject.addItem("化学,生物,地理")
            self.comboBox_subject.addItem("化学,政治,历史")
            self.comboBox_subject.addItem("化学,政治,地理")
            self.comboBox_subject.addItem("化学,历史,地理")
            self.comboBox_subject.addItem("生物,政治,历史")
            self.comboBox_subject.addItem("生物,政治,地理")
            self.comboBox_subject.addItem("生物,历史,地理")
            self.comboBox_subject.addItem("政治,历史,地理")
            self.comboBox_batch.addItem("本科批")

    # 静态方法 获取行数在表中创建
    @staticmethod
    def load_csv(tablewidget, filename):
        with open(filename, 'r') as f:  # 打开文件
            csvreader = csv.reader(f)  # 创建一个csv.reader对象
            for row_index, row in enumerate(csvreader):  # 遍历csv.reader对象的每一行
                for column_index, item in enumerate(row):  # 遍历这一行的每一列
                    tablewidget.setItem(row_index, column_index, QTableWidgetItem(item))

    # 静态方法 获取行数在表中创建
    @staticmethod
    def get_row_count(filename):
        with open(filename) as file:
            reader = csv.reader(file)
            row_count = sum(1 for _ in reader)
        return row_count

    # 静态方法 加载学校简介信息
    @staticmethod
    def loadCsvToTable(self, filename):
        with open(filename, newline='', encoding='gb2312') as csvfile:
            csvreader = csv.reader(csvfile)
            # 获取数据行数
            rows = list(csvreader)
            self.tableWidget_4.setRowCount(len(rows))

            for row_idx, row in enumerate(rows):
                for col_idx, cell in enumerate(row):
                    self.tableWidget_4.setItem(row_idx, col_idx, QTableWidgetItem(cell))

    # 静态方法 河南——将位次转化成23年对应分数(理科)
    @staticmethod
    def sec_to_score_lk(section):
        with open('Document/LK_score_section.json', 'r', encoding='gb2312') as file:
            # 使用json.load()方法解析JSON数据
            data = json.load(file)
        for key, value in data["data"]["search"].items():
            # print(f"Key: {key}")
            # print("rank_range:")
            # print(value['rank_range'])
            # print()
            start, end = map(int, value['rank_range'].split('-'))
            # 检查给定数字是否在范围内
            if start <= section <= end:
                print(key)
                return key
            else:
                pass

    # 静态方法 河南——将位次转化成23年对应分数(理科)
    @staticmethod
    def sec_to_score_wk(section):
        with open('Document/WK_score_section.json', 'r', encoding='gb2312') as file:
            # 使用json.load()方法解析JSON数据
            data = json.load(file)
        for key, value in data["data"]["search"].items():
            # print(f"Key: {key}")
            # print("rank_range:")
            # print(value['rank_range'])
            # print()
            start, end = map(int, value['rank_range'].split('-'))
            # 检查给定数字是否在范围内
            if start <= section <= end:
                print(key)
                return key
            else:
                pass

    # 工具 学校列表
    def sch_list(self):
        url = QUrl.fromLocalFile('Document\学校列表.txt')
        QDesktopServices.openUrl(url)

    # 工具 可视化
    def vis(self, m):
        try:
            filename = f"score_csv/{self.lineEdit_sch.text()}在{self.comboBox_pro.currentText()}的{self.comboBox.currentText()}{self.lineEdit_year.text()}年专业分数线.csv"

            file_list = os.listdir('score_csv')
            spe_name = f"{self.lineEdit_sch.text()}在{self.comboBox_pro.currentText()}的{self.comboBox.currentText()}{self.lineEdit_year.text()}年专业分数线.csv"
            if spe_name in file_list:
                score = vis_method.get_score(filename)
                name = vis_method.get_name(filename)
                vis_method.showwindow(name, score)
                print(spe_name)
            else:
                QMessageBox.critical(self.widget, f"错误", '请先查询专业分数线，再点击可视化')
        except (FileNotFoundError, RuntimeError):
            pass

    # 工具 数据分析最低位次结果
    def show_ana(self, m):
        name = str(self.lineEdit_sch.text())
        province = str(self.comboBox_pro.currentText())
        local_type = str(self.comboBox.currentText())
        csv_name = f'{name}在{province}的{local_type}'

        matching_files = find_files(csv_name)
        test_name = f'{name}在{province}的{local_type}.csv'

        if os.path.isfile(os.path.join('ana_csv', test_name)):
            try:
                test = matching_files[0]
                ana_window(matching_files, csv_name)
            except IndexError:
                pass
        else:
            QMessageBox.critical(self.widget, f"错误", '当前条件未进行数据分析，请先点击数据分析按钮')

    # 工具 数据分析最低分结果
    def show_ana_score(self, m):
        name = str(self.lineEdit_sch.text())
        province = str(self.comboBox_pro.currentText())
        local_type = str(self.comboBox.currentText())
        csv_name = f'{name}在{province}的{local_type}'

        matching_files = find_files(csv_name)
        test_name = f'{name}在{province}的{local_type}.csv'

        if os.path.isfile(os.path.join('ana_csv', test_name)):
            try:
                test = matching_files[0]
                ana_window_score(matching_files, csv_name)
            except IndexError:
                pass
        else:
            QMessageBox.critical(self.widget, f"错误", '当前条件未进行数据分析，请先点击数据分析按钮')

    # 槽函数 展示时间
    def show_time(self, object):
        try:
            self.textEdit_time.setText(f"查询完成，用时{round(object, 2)}秒")
        except TypeError:
            pass

    # 槽函数 展示招生计划
    def net_plan(self, object):
        try:
            # 动态生成表格的行数
            row_count = self.get_row_count(object)
            self.tableWidget_2.setRowCount(row_count)
            self.load_csv(tablewidget=self.tableWidget_2,
                          filename=object)
            self.tableWidget_2.resizeColumnsToContents()
        except TypeError:
            self.textEdit_time.clear()
            QMessageBox.critical(self.widget, f"类型错误", "当前条件找不到相关信息，请等待网站更新或检查输入条件是否有误")
        except FileNotFoundError:
            self.textEdit_time.clear()
            QMessageBox.critical(self.widget, f"网站数据不存在", "当前条件未公布数据，请等待网站更新或更换条件")
        except OSError:
            self.textEdit_time.clear()
            QMessageBox.critical(self.widget, f"文件错误", "当前条件找不到相关信息，请等待网站更新或更换条件")

    # 槽函数 展示专业分数线
    def net_score(self, object):
        try:
            # 动态生成表格的行数
            row_count = self.get_row_count(object)
            self.tableWidget.setRowCount(row_count)
            self.load_csv(tablewidget=self.tableWidget,
                          filename=object)
            self.tableWidget.resizeColumnsToContents()
        except TypeError:
            self.textEdit_time.clear()
            QMessageBox.critical(self.widget, f"输入类型错误", "当前条件找不到相关信息，请等待网站更新或检查输入条件是否有误")
        except FileNotFoundError:
            self.textEdit_time.clear()
            QMessageBox.critical(self.widget, f"网站数据不存在", "当前条件未公布数据，请等待网站更新")
        except OSError:
            self.textEdit_time.clear()
            QMessageBox.critical(self.widget, f"文件错误", "当前条件找不到相关信息，请等待网站更新或更换条件")

    # 槽函数 保存数据分析结果
    def get_ana(self, object):
        name = str(self.lineEdit_sch.text())
        province = str(self.comboBox_pro.currentText())
        local_type = str(self.comboBox.currentText())
        if object != None:
            try:
                self.textEdit_time.setText(f"分析完成，请点击工具栏数据分析按钮查看")
                data_csv = pd.read_csv(f'ana_csv/{name}在{province}的{local_type}.csv', header=None,
                                       names=['招生类型', '省控线', '最低分', '最低位次', '年'])  # 添加表头
                data_csv.to_csv(f'ana_csv/{name}在{province}的{local_type}.csv', index=False)  # 去除索引
                original_name = f'{name}在{province}的{local_type}'  # 获取数据分析的原始文件名
                group_csv(original_name)  # 分组
            except FileNotFoundError:
                self.textEdit_time.clear()
                QMessageBox.critical(self.widget, f"网络错误", "网络请求超时，请稍后重试")
        else:
            self.textEdit_time.clear()
            QMessageBox.critical(self.widget, f"错误", "查询失败，请检查输入名称名称或稍后重试")

    # 槽函数 展示网络状态
    def net_check_show(self, object):
        if object != None:
            self.label_check.setText(f"{proxies['https']} 网络正常，响应时间{int(object)}ms")
        else:
            self.label_check.setText(f"当前网络不可用,请检查网络状态或稍后重试")

    # 槽函数 展示学校简介
    def show_intro(self, object):
        if object == None:
            self.textEdit_time.clear()
            QMessageBox.critical(self.widget, f"错误", "当前学校无简介信息，或输入的学校名称不存在")
        elif object == 0:
            self.textEdit_time.clear()
            QMessageBox.critical(self.widget, f"错误", "请输入正确的学校名称")
        else:

            # 设置表格的列数 (假设CSV文件的列数已知)
            self.tableWidget_4.setColumnCount(1)

            # 从CSV文件中读取数据并写入到 QTableWidget 中
            self.loadCsvToTable(self, object)
            self.tableWidget_4.resizeColumnsToContents()

    # 槽函数 展示志愿填报
    def show_aspire(self, object):
        if object is not None:
            # 动态生成表格的行数
            row_count = self.get_row_count(object)
            self.tableWidget_3.setRowCount(row_count)
            self.load_csv(tablewidget=self.tableWidget_3,
                          filename=object)
            self.tableWidget_3.resizeColumnsToContents()
        elif object == 0:
            QMessageBox.critical(self.widget, f"网络错误", "请求超时，请稍后再试")
        else:
            QMessageBox.critical(self.widget, f"错误", "输入条件有误或当前条件下无志愿推荐（可能原因:如输入位次为一本位次，但选择了专科批。请选择符合情况的批次）")

    # 按钮事件 查专业分数线
    def special_score(self):
        global index1, index2, index3, index4, start  # 定义全局变量，使线程类中的方法能够访问控件中的内容。
        index1 = str(self.lineEdit_sch.text())
        index2 = str(self.comboBox_pro.currentText())
        index3 = str(self.comboBox.currentText())
        index4 = str(self.lineEdit_year.text())
        year_value = [str(2018), str(2019), str(2020), str(2021), str(2022), str(2023), str(2024)]
        if index4 in year_value:
            self.textEdit_time.setText(f"正在查询{index1}在{index2}的{index3}{index4}年专业分数线......")
            file_name = f"score_csv/{index1}在{index2}的{index3}{index4}年专业分数线.csv"
            start = time.time()
            if os.path.exists(file_name):
                # 动态生成表格的行数
                row_count = self.get_row_count(file_name)
                self.tableWidget.setRowCount(row_count)

                self.load_csv(tablewidget=self.tableWidget,
                              filename=file_name)
                self.tableWidget.resizeColumnsToContents()
                end = time.time()
                spend_time = (end - start)
                self.textEdit_time.setText(f"查询完成，用时{round(spend_time, 2)}秒")
            else:
                self.myth_score.start()
        else:
            QMessageBox.critical(self.widget, f"输入错误", "请输入范围内的年（2018-2024）")

    # 按钮事件 查招生计划
    def school_plan(self):
        global index1, index2, index3, index4, start
        index1 = str(self.lineEdit_sch.text())
        index2 = str(self.comboBox_pro.currentText())
        index3 = str(self.comboBox.currentText())
        index4 = str(self.lineEdit_year.text())
        year_value = [str(2018), str(2019), str(2020), str(2021), str(2022), str(2023), str(2024)]
        if index4 in year_value:
            self.textEdit_time.setText(f"正在查询{index1}在{index2}的{index3}{index4}年招生计划......")
            file_name = f"plan_csv/{index1}在{index2}的{index3}{index4}年招生计划.csv"
            start = time.time()
            if os.path.exists(file_name):
                # 动态生成表格的行数
                row_count = self.get_row_count(file_name)
                self.tableWidget_2.setRowCount(row_count)
                self.load_csv(tablewidget=self.tableWidget_2,
                              filename=file_name)
                self.tableWidget_2.resizeColumnsToContents()
                end = time.time()
                spend_time = (end - start)
                self.textEdit_time.setText(f"查询完成，用时{round(spend_time, 2)}秒")
            else:
                self.myth_plan.start()
        else:
            QMessageBox.critical(self.widget, f"输入错误", "请输入范围内的年（2018-2023）")

    # 按钮事件 数据分析
    def school_ana(self):
        # QMessageBox.critical(self.widget, f"维护中", "该功能正在维护，请等待版本更新")
        global index1, index2, index3, index4, start
        index1 = str(self.lineEdit_sch.text())
        index2 = str(self.comboBox_pro.currentText())
        index3 = str(self.comboBox.currentText())

        file_name = f"ana_csv/{index1}在{index2}的{index3}.csv"
        if os.path.exists(file_name):
            self.textEdit_time.setText(f"当前学校已进行过分析，请点击工具栏数据分析按钮查看")
        else:
            self.textEdit_time.setText(
                f"正在分析{index1}在{index2}的{index3}录取情况，请等待......")
            self.myth_ana.start()

    # 按钮事件 学校简介
    def school_intro(self):
        global sch_name
        sch_name = str(self.lineEdit_sch.text())

        if sch_name != '':
            self.textEdit_time.setText(f"正在查询{sch_name}学校简介......")
            file_name = f"intro_text/{sch_name}简介.csv"
            if os.path.exists(file_name):
                # 设置表格的列数 (假设CSV文件的列数已知)
                self.tableWidget_4.setColumnCount(1)
                # 从CSV文件中读取数据并写入到 QTableWidget 中
                self.loadCsvToTable(self, file_name)
                self.tableWidget_4.resizeColumnsToContents()

                self.textEdit_time.setText(f"查询完成")
            else:
                self.myth_intro.start()
        else:
            QMessageBox.critical(self.widget, f"输入错误", "请输入学校名称")

    # 按钮事件 检测网络状态
    def check_net(self):
        self.label_check.setText(f"IP:111.177.63.86:8888  正在检测网络状态......")
        self.myth_check.start()

    # 按钮事件 志愿
    def aspire(self):
        global province_a, classify_a, score_a, section_a, batch_a, optional_a, subject_a
        province_a = self.comboBox_pro_2.currentText()
        if province_a == "河南":
            batch_a = self.comboBox_batch.currentText()
            classify_a = self.comboBox_subject.currentText()

            try:
                section_a = int(self.lineEdit_sec.text())
                if classify_a == '理科':
                    subject_a = "理科"
                    optional_a = "理科"
                    score_a = self.sec_to_score_lk(section_a)
                elif classify_a == '文科':
                    score_a = self.sec_to_score_wk(section_a)
                    subject_a = "文科"
                    optional_a = "文科"

                filename = f"aspiration/{province_a}{classify_a}{score_a}{batch_a}志愿.csv"
                start = time.time()
                if os.path.exists(filename):
                    # 动态生成表格的行数
                    row_count = self.get_row_count(filename)
                    self.tableWidget_3.setRowCount(row_count)

                    self.load_csv(tablewidget=self.tableWidget_3,
                                  filename=filename)
                    self.tableWidget_3.resizeColumnsToContents()
                    end = time.time()
                    spend_time = (end - start)
                    self.textEdit_time.setText(f"查询完成，用时{round(spend_time, 2)}秒")
                else:
                    self.textEdit_time.setText(f"正在推荐志愿......")
                    self.myth_aspire.start()
            except ValueError:
                QMessageBox.critical(self.widget, f"输入错误", "请检查输入格式")
            except NameError:
                QMessageBox.critical(self.widget, f"输入错误", "请输入科目")

        elif province_a == "北京" or "山东":
            batch_a = self.comboBox_batch.currentText()
            classify_a = "综合"
            subject_a = self.comboBox_subject.currentText()
            optional_a = self.comboBox_subject.currentText()
            try:
                score_a = self.lineEdit_score.text()
                section_a = ""

                filename = f"aspiration/{province_a}{classify_a}{score_a}{batch_a}志愿.csv"
                start = time.time()
                if os.path.exists(filename):
                    # 动态生成表格的行数
                    row_count = self.get_row_count(filename)
                    self.tableWidget_3.setRowCount(row_count)

                    self.load_csv(tablewidget=self.tableWidget_3,
                                  filename=filename)
                    self.tableWidget_3.resizeColumnsToContents()
                    end = time.time()
                    spend_time = (end - start)
                    self.textEdit_time.setText(f"查询完成，用时{round(spend_time, 2)}秒")
                else:
                    self.textEdit_time.setText(f"正在推荐志愿......")
                    self.myth_aspire.start()
            except ValueError:
                QMessageBox.critical(self.widget, f"输入错误", "请检查输入格式")
            except NameError:
                QMessageBox.critical(self.widget, f"输入错误", "请输入科目")


# 线程 专业分数线
class ThreadScore(QThread):
    signal_csv = pyqtSignal(object)
    signal_time = pyqtSignal(object)

    with open('DICT/school_ID.csv', encoding='gb2312') as f1:
        csvfile = csv.reader(f1)
        listf1 = list(csvfile)
        schoolID_dic = dict(listf1)

    with open('DICT/province_ID.csv', encoding='gb2312') as f2:
        csvfile = csv.reader(f2)
        listf2 = list(csvfile)
        province_dic = dict(listf2)

    with open('DICT/type_ID.csv', encoding='gb2312') as f3:
        csvfile = csv.reader(f3)
        listf3 = list(csvfile)
        type_dic = dict(listf3)

    def __init__(self):
        self.score_csv = None
        self.time = None
        super(ThreadScore, self).__init__()

    def get_net_score(self):
        try:
            filename = f"score_csv/{index1}在{index2}的{index3}{index4}年专业分数线.csv"
            for i in range(1, 8):
                page_num = i
                special_params = {
                    "local_batch_id": "",
                    "local_province_id": f"{self.province_dic[f'{index2}']}",
                    "local_type_id": f"{self.type_dic[f'{index3}']}",
                    "page": f'{page_num}',
                    "school_id": f"{self.schoolID_dic[f'{index1}']}",
                    "size": 10,
                    "uri": "apidata/api/gk/score/special",
                    "year": f"{index4}"
                }

                resp = requests.post(url=url, params=special_params, headers=headers)

                dic = resp.json()  # 将请求结果保存成字典形式

                print(resp.url)
                try:
                    item = dic['data']['item']
                    name = item[0]['name']

                    f = open(filename, mode='a',
                             encoding="gb2312",
                             newline="")
                    # newline = '' 在保存CSV时不含空白行
                    csvwriter = csv.writer(f)
                    # 循环的意义：需求item内的每一个子集（【0】，【1】，【2】等）的min属性，each的含义是item内的每一个元组。
                    for each in item:
                        min_score = each['min']
                        spname = each['spname']
                        min_section = each['min_section']
                        local_batch_name = each['local_batch_name']
                        average = each['average']
                        csvwriter.writerow([spname, average, min_score, min_section, local_batch_name])
                        print(spname)
                    sleep_time = random.uniform(0.1, 0.2)
                    time.sleep(sleep_time)
                except(IndexError):
                    break

            end = time.time()
            spend_time = (end - start)

            self.time = spend_time
            self.score_csv = filename
        except(KeyError, TypeError):
            self.time = None
            self.score_csv = None

    def run(self):
        self.get_net_score()
        self.signal_csv.emit(self.score_csv)
        self.signal_time.emit(self.time)


# 线程 招生计划
class ThreadPlan(QThread):
    signal_csv = pyqtSignal(object)
    signal_time = pyqtSignal(object)

    with open('DICT/school_ID.csv', encoding='gb2312') as f1:
        csvfile = csv.reader(f1)
        listf1 = list(csvfile)
        schoolID_dic = dict(listf1)

    with open('DICT/province_ID.csv', encoding='gb2312') as f2:
        csvfile = csv.reader(f2)
        listf2 = list(csvfile)
        province_dic = dict(listf2)

    with open('DICT/type_ID.csv', encoding='gb2312') as f3:
        csvfile = csv.reader(f3)
        listf3 = list(csvfile)
        type_dic = dict(listf3)

    def __init__(self):
        self.plan_csv = None
        self.time = None
        super(ThreadPlan, self).__init__()

    def get_net_plan(self):
        try:
            for i in range(1, 8):
                page_num = i
                plan_params = {
                    "local_batch_id": "",
                    "local_province_id": f"{self.province_dic[f'{index2}']}",
                    "local_type_id": f"{self.type_dic[f'{index3}']}",
                    "page": f'{page_num}',
                    "school_id": f"{self.schoolID_dic[f'{index1}']}",
                    "size": 10,
                    "uri": "apidata/api/gkv3/plan/school",
                    "year": f"{index4}"
                }
                resp = requests.post(url=url, params=plan_params, headers=headers)
                dic = resp.json()
                try:
                    item = dic['data']['item']
                    name = item[0]['name']
                    f = open(f"plan_csv/{index1}在{index2}的{index3}{index4}年招生计划.csv", mode='a',
                             encoding="gb2312",
                             newline="")
                    # newline = '' 在保存CSV时不含空白行
                    csvwriter = csv.writer(f)
                    # 循环的意义：需求item内的每一个子集（【0】，【1】，【2】等）的min属性，each的含义是item内的每一个元组。
                    for each in item:
                        plan_num = each['num']
                        spname = each['spname']
                        length = each['length']
                        tuition = each['tuition']
                        local_batch_name = each['local_batch_name']
                        csvwriter.writerow([spname, plan_num, length, tuition, local_batch_name])
                    sleep_time = random.uniform(0.2, 0.3)
                    time.sleep(sleep_time)
                except IndexError:
                    break
                except UnicodeEncodeError:
                    pass
            end = time.time()
            spend_time = (end - start)
            self.time = spend_time
            self.plan_csv = f"plan_csv/{index1}在{index2}的{index3}{index4}年招生计划.csv"
        except(KeyError, TypeError):
            self.time = None
            self.plan_csv = None

    def run(self):
        self.get_net_plan()
        self.signal_csv.emit(self.plan_csv)
        self.signal_time.emit(self.time)


# 线程 学校简介
class ThreadIntro(QThread):
    signal_intro = pyqtSignal(object)
    signal_time = pyqtSignal(object)

    def __init__(self):
        self.intro = None
        self.time = None
        super(ThreadIntro, self).__init__()

    def get_intro(self):
        with open('DICT/school_ID.csv', encoding='gb2312') as f1:
            csvfile = csv.reader(f1)
            listf1 = list(csvfile)
            schoolID_dic = dict(listf1)

        start = time.time()
        try:
            sch_id = schoolID_dic[f'{sch_name}']
            filename = f"intro_text/{sch_name}简介.csv"
            resp = requests.get(url=f"https://static-data.gaokao.cn/www/2.0/school/{sch_id}/info.json", headers=headers)
            dic = resp.json()  # 将请求结果保存成字典形式

            f = open(filename, mode='a', encoding="gb2312", newline="")
            # newline = '' 在保存CSV时不含空白行
            csvwriter = csv.writer(f)

            csvwriter.writerow([f"{sch_name}"])
            csvwriter.writerow([f"{dic['data']['address']}"])
            csvwriter.writerow([f"{dic['data']['school_site']}"])
            csvwriter.writerow([f"{dic['data']['phone']}"])
            csvwriter.writerow([f"{dic['data']['email']}"])
            csvwriter.writerow([f"{dic['data']['belong']}"])
            csvwriter.writerow([f"{dic['data']['motto']}"])
            csvwriter.writerow([f"{dic['data']['type_name']}"])
            csvwriter.writerow([f"{dic['data']['area']}亩"])
            csvwriter.writerow([f"{dic['data']['ruanke_rank']}"])
            csvwriter.writerow([f"{dic['data']['xyh_rank']}"])
            csvwriter.writerow([f"{dic['data']['level_name']} {dic['data']['dual_class_name']}"])

            end = time.time()
            spend_time = (end - start)
            self.intro = filename
            self.time = spend_time
        except KeyError:
            self.intro = None
            self.time = None

    def run(self):
        self.get_intro()
        self.signal_intro.emit(self.intro)
        self.signal_time.emit(self.time)


# 线程 数据分析
class ThreadAna(QThread):
    signal_csv = pyqtSignal(object)
    signal_time = pyqtSignal(object)

    with open('DICT/school_ID.csv', encoding='gb2312') as f1:
        csvfile = csv.reader(f1)
        listf1 = list(csvfile)
        schoolID_dic = dict(listf1)

    with open('DICT/province_ID.csv', encoding='gb2312') as f2:
        csvfile = csv.reader(f2)
        listf2 = list(csvfile)
        province_dic = dict(listf2)

    with open('DICT/type_ID.csv', encoding='gb2312') as f3:
        csvfile = csv.reader(f3)
        listf3 = list(csvfile)
        type_dic = dict(listf3)

    def __init__(self):
        self.ana_csv = None
        self.time = None
        super(ThreadAna, self).__init__()

    def get_net_ana(self):
        try:
            start = time.time()
            for i in range(2018, 2023):
                params_year = {
                    "e_sort": "zslx_rank,min",
                    "e_sorttype": "zslx_rank,min",
                    "local_province_id": f"{self.province_dic[f'{index2}']}",
                    "local_type_id": f"{self.type_dic[f'{index3}']}",
                    "page": 1,
                    "school_id": f"{self.schoolID_dic[f'{index1}']}",
                    "size": 10,
                    "uri": "apidata/api/gk/score/province",
                    "year": i
                }
                resp = requests.post(url=url, params=params_year, headers=headers)
                dic = resp.json()
                print(dic)
                try:
                    item = dic['data']['item']
                    name = item[0]['name']
                    province = item[0]['local_province_name']
                    local_type = item[0]['local_type_name']
                    f = open(f"ana_csv/{name}在{province}的{local_type}.csv", mode='a',
                             encoding="utf-8",
                             newline="")
                    # newline = '' 在保存CSV时不含空白行
                    csvwriter = csv.writer(f)
                    for each in item:
                        proscore = each['proscore']
                        min = each['min']
                        min_section = each['min_section']
                        year = each['year']
                        zslx = each['zslx_name']
                        batch = each['local_batch_name']
                        zslx = f"{zslx}({batch})"
                        csvwriter.writerow([zslx, proscore, min, min_section, year])
                        sleep_time = random.uniform(0.5, 0.9)
                        time.sleep(sleep_time)
                except IndexError:  # 跳过没有数据的年
                    pass
            end = time.time()
            spend_time = (end - start)
            self.time = spend_time
            self.ana_csv = "ana_csv/{name}在{province}的{local_type}.csv"
        except(KeyError, TypeError):
            self.ana_csv = None
            self.time = None

    def run(self):
        self.get_net_ana()
        self.signal_csv.emit(self.ana_csv)
        self.signal_time.emit(self.time)


# 线程 检测网络状态
class ThreadChecknet(QThread):
    signal_time = pyqtSignal(object)

    def __init__(self):

        self.time = None
        super(ThreadChecknet, self).__init__()

    def check_net(self):
        params_test = {
            "local_batch_id": "7",
            "local_province_id": "41",
            "local_type_id": "1",
            "page": '1',
            "school_id": "31",
            "size": 10,
            "uri": "apidata/api/gkv3/plan/school",
            "year": "2020"
        }
        try:
            start = time.time()
            resp = requests.post(url=url, params=params_test, headers=headers)
            status_code = resp.status_code
            end = time.time()
            net_time = (end - start) * 1000
            if status_code == 200:
                self.time = net_time
            else:
                self.time = None
        except ProxyError:
            self.time = None

    def run(self):
        self.check_net()
        self.signal_time.emit(self.time)


# 线程 志愿填报
class ThreadAspire(QThread):
    signal_csv = pyqtSignal(object)
    signal_time = pyqtSignal(object)

    def __init__(self):
        self.aspire_csv = None
        self.time = None
        super(ThreadAspire, self).__init__()

    def get_aspire(self):
        start = time.time()
        url1 = 'https://mnzy.gaokao.cn/api/pc/v3/v1/query/recommendPage?'
        values = ['CHONG', 'WEN', 'BAO']
        dic_type = {
            'CHONG': '可冲击',
            'WEN': '较稳妥',
            'BAO': '可保底'
        }
        try:
            for aspire_type in values:
                if province_a == "北京":
                    params = {
                        'type': f'{aspire_type}',
                        'pageNum': 1,
                        'pageSize': 10,
                        'year': 2024,
                        'province': f'{province_a}',
                        'score': f'{score_a}',
                        'classify': f'{classify_a}',  # 部分省份的首选科目
                        'optional': f'{optional_a}',
                        'subjects': f'{subject_a}',
                        'ranks': f'{section_a}',
                        'batch': f'{batch_a}',
                        'gradeType': '本科',
                        'entrantType': 1
                    }
                elif province_a == "河南":
                    params = {
                        'type': f'{aspire_type}',
                        'pageNum': 1,
                        'pageSize': 10,
                        'year': 2024,
                        'province': f'{province_a}',
                        'score': f'{score_a}',
                        'classify': f'{classify_a}',  # 部分省份的首选科目
                        'optional': f'{optional_a}',
                        'subjects': f'{subject_a}',
                        'ranks': f'{section_a}',
                        'batch': f'{batch_a}',
                        'entrantType': 1
                    }
                elif province_a == "山东":
                    params = {
                        'type': f'{aspire_type}',
                        'pageNum': 1,
                        'pageSize': 10,
                        'year': 2024,
                        'province': f'{province_a}',
                        'score': f'{score_a}',
                        'classify': f'{classify_a}',  # 部分省份的首选科目
                        'optional': f'{optional_a}',
                        'subjects': f'{subject_a}',
                        'ranks': f'{section_a}',
                        'batch': f'{batch_a}',
                        'gradeType': '本科',
                        'entrantType': 1
                    }
                resp = requests.get(url1, headers=headers, params=params)
                dic = resp.json()
                try:
                    item = dic['body']['list']
                    print('start searching......')
                    filename = f"aspiration/{province_a}{optional_a}{score_a}{batch_a}志愿.csv"
                    f = open(filename, mode='a',
                             encoding="gb2312",
                             newline="")
                    # newline = '' 在保存CSV时不含空白行
                    csvwriter = csv.writer(f)
                    for each in item:
                        name = each['universityName']
                        recruitCode = each['recruitCode']
                        propertyName = each['propertyName']
                        categoryName = each['categoryName']
                        historyScore = each['historyScore']
                        planNum = each['planNum']
                        type = each['type']
                        advice = dic_type[f'{type}']
                        majorName = each['majorName']


                        data = json.loads(historyScore)

                        formatted_data = []
                        for item in data:
                            key, value = list(item.items())[0]
                            formatted_data.append(f"[{key}:{value.replace(',', ' ')}]")
                        result = "".join(formatted_data)
                        csvwriter.writerow([name, advice, recruitCode, propertyName, categoryName, result, planNum, majorName])
                    sleep_time = random.uniform(0.1, 0.2)
                    time.sleep(sleep_time)
                except IndexError:
                    pass
                except UnicodeEncodeError:
                    pass
            end = time.time()
            spend_time = (end - start)
            self.time = spend_time
            self.aspire_csv = filename
        except (TypeError, IndexError):
            print('error')
            self.aspire_csv = None
        except SSLError:
            print('超时')
            self.aspire_csv = 0
        except UnboundLocalError:
            self.aspire_csv = None

    def run(self):
        self.get_aspire()
        self.signal_csv.emit(self.aspire_csv)
        self.signal_time.emit(self.time)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()

    sys.exit(app.exec())
