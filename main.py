# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, 
    QAction, QFileDialog, QApplication, QTextEdit)
from test import Ui_MainWindow
import re

class mywindow(QtWidgets.QMainWindow,Ui_MainWindow):  
    def __init__(self):  
        super(mywindow,self).__init__()  
        self.setupUi(self)  
        #T1 net:open net file
        self.btnT1OpenNet.clicked.connect(self.openT1net)
        #T1 net:open import net file
        self.btnT1ImportNet.clicked.connect(self.openT1importnet)
        #T1 net:confirm button 1-3
        self.btnT1confirm1.clicked.connect(self.T1confirm)
        self.btnT1confirm2.clicked.connect(self.T1confirm)
        self.btnT1confirm3.clicked.connect(self.T1confirm)
        #T1 net:add file button
        self.btnT1AddFile.clicked.connect(self.T1addfile)
        #T1 net:remove file button
        self.btnT1RemoveFile.clicked.connect(self.T1removefile)
        #T1 net:remove all file button
        self.btnT1RemoveAll.clicked.connect(self.T1removeall)
        #T1 net:export file list
        self.btnT1ExportList.clicked.connect(self.T1export)
        #T1 net:import file list
        self.btnT1ImportList.clicked.connect(self.T1import)

    #T1 net:import list
    def T1import(self):
        fname = QFileDialog.getOpenFileName(self,'Open file','c:\\','List Files (*.list)')
        if fname[0]:
            with open(fname[0],'r') as f:
                my_txt=f.read()
                m=re.split('\n',my_txt)
                for name in m:               
                    self.lstT1NetList.addItem(name)

    #T1 net:export list
    def T1export(self):
        fname = QFileDialog.getSaveFileName(self,'Open file','c:\\','List Files (*.list)')
        if fname[0]:
            i=0
            with open(fname[0],'w') as f:
                while(i<self.lstT1NetList.count()):
                    f.write(self.lstT1NetList.item(i).text()+"\n")
                    i=i+1              


    #T1 net:remove all button
    def T1removeall(self):
        i = self.lstT1NetList.count()
        while(i>=0):
            i=i-1
            item_deleted=self.lstT1NetList.takeItem(i)
            item_deleted=None

    #T1 net:remove file button
    def T1removefile(self):
        item_deleted=self.lstT1NetList.takeItem(self.lstT1NetList.currentRow())
        item_deleted=None

    #T1 net:add file button
    def T1addfile(self):
        fname = QFileDialog.getOpenFileNames(self,'Open file','c:\\')
        if fname[0]:
            for name in fname[0]:
                self.lstT1NetList.addItem(name)

    #T1 net:confirm button 1-3
    def T1confirm(self):
        self.tabWidget.setCurrentIndex(1)

    #T1 net:open import net file
    def openT1importnet(self):
        fname = QFileDialog.getOpenFileName(self,'Open file','c:\\')
        if fname[0]:
            self.txtT1ImportNet.setText(fname[0])      

    #T1 net:open net file
    def openT1net(self):
        fname = QFileDialog.getOpenFileName(self,'Open file','c:\\')
        if fname[0]:
            self.txtT1OpenNet.setText(fname[0])

	
  
if __name__=="__main__":  
    import sys  
  
    app=QtWidgets.QApplication(sys.argv)  
    myshow=mywindow()  
    myshow.show()  
    sys.exit(app.exec_())