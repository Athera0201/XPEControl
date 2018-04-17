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
        self.tabWidget.currentChanged.connect(self.tabchanged)      
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
        #T2 config:init Design Optimization combo box
        self.cmbT2DO.addItem("None")
        #T2 config:init Cell Type combo box
        self.cmbT2CellType.addItem("DigitalRRAMTHU")
        #T2 config:Default settings
        self.btnT2Default.clicked.connect(self.T2default)
        #T2 config:Save settings to file
        self.btnT2Save.clicked.connect(self.T2save)
        #T2 config:Load settings from file
        self.btnT2Read.clicked.connect(self.T2load)
        #T2 config:add file button
        self.btnT2AddFile.clicked.connect(self.T2addfile)
        #T2 config:remove file button
        self.btnT2RemoveFile.clicked.connect(self.T2removefile)
        #T2 config:remove all file button
        self.btnT2RemoveAll.clicked.connect(self.T2removeall)
        #T2 config:export file list
        self.btnT2ExportList.clicked.connect(self.T2export)
        #T2 config:import file list
        self.btnT2ImportList.clicked.connect(self.T2import)
        #T2 config:confirm
        self.btnT2Confirm1.clicked.connect(self.T2confirm)
        self.btnT2Confirm2.clicked.connect(self.T2confirm)
        #T3 test case:add net file
        self.btnT3AddNet.clicked.connect(self.T3addnet)
        #T3 test case:remove net file
        self.btnT3RemoveNet.clicked.connect(self.T3removenet)
        #T3 test case:remove all net
        self.btnT3RemoveAllNet.clicked.connect(self.T3removeallnet)
        #T3 test case:add config file
        self.btnT3AddConfig.clicked.connect(self.T3addconfig)
        #T3 test case:remove config file
        self.btnT3RemoveConfig.clicked.connect(self.T3removeconfig)
        #T3 test case:remove all config file
        self.btnT3RemoveAllConfig.clicked.connect(self.T3removeallconfig)
        
    #T3 test case:remove all config files
    def T3removeallconfig(self):
        i = self.lstT3ConfigList.count()
        while(i>=0):
            i=i-1
            item_deleted=self.lstT3ConfigList.takeItem(i)
            item_deleted=None
            
    #T3 test case:remove config file
    def T3removeconfig(self):
        item_deleted=self.lstT3ConfigList.takeItem(self.lstT3ConfigList.currentRow())
        item_deleted=None
        
    #T3 test case:add config file
    def T3addconfig(self):
        fname = QFileDialog.getOpenFileNames(self,'Open file','c:\\')
        if fname[0]:
            for name in fname[0]:
                self.lstT3ConfigList.addItem(name)
                
    #T3 test case:remove all nets
    def T3removeallnet(self):
        i = self.lstT3NetList.count()
        while(i>=0):
            i=i-1
            item_deleted=self.lstT3NetList.takeItem(i)
            item_deleted=None
            
    #T3 test case:remove net file
    def T3removenet(self):
        item_deleted=self.lstT3NetList.takeItem(self.lstT3NetList.currentRow())
        item_deleted=None
        
    #T3 test case:add net file
    def T3addnet(self):
        fname = QFileDialog.getOpenFileNames(self,'Open file','c:\\')
        if fname[0]:
            for name in fname[0]:
                self.lstT3NetList.addItem(name)
    
    #T2 config:confirm
    def T2confirm(self):
        self.tabWidget.setCurrentIndex(2)

    #T2 Config:import list
    def T2import(self):
        fname = QFileDialog.getOpenFileName(self,'Open file','c:\\','Config List Files (*.Clist)')
        if fname[0]:
            i = self.lstT2ConfigList.count()
            while(i>=0):
                i=i-1
                item_deleted=self.lstT2ConfigList.takeItem(i)
                item_deleted=None
            with open(fname[0],'r') as f:
                my_txt=f.read()
                m=re.split('\n',my_txt)
                for name in m:               
                    self.lstT2ConfigList.addItem(name)

    #T2 config:export list
    def T2export(self):
        fname = QFileDialog.getSaveFileName(self,'Open file','c:\\','Config List Files (*.Clist)')
        if fname[0]:
            i=0
            with open(fname[0],'w') as f:
                while(i<self.lstT2ConfigList.count()):
                    if i+1==self.lstT2ConfigList.count():
                        f.write(self.lstT2ConfigList.item(i).text())
                    else:
                        f.write(self.lstT2ConfigList.item(i).text()+"\n")
                    i=i+1              


    #T2 config:remove all button
    def T2removeall(self):
        i = self.lstT2ConfigList.count()
        while(i>=0):
            i=i-1
            item_deleted=self.lstT2ConfigList.takeItem(i)
            item_deleted=None

    #T2 config:remove file button
    def T2removefile(self):
        item_deleted=self.lstT2ConfigList.takeItem(self.lstT2ConfigList.currentRow())
        item_deleted=None

    #T2 config:add file button
    def T2addfile(self):
        fname = QFileDialog.getOpenFileNames(self,'Open file','c:\\')
        if fname[0]:
            for name in fname[0]:
                self.lstT2ConfigList.addItem(name)

     
    #T2 config:Load settings
    def T2load(self):
        fname = QFileDialog.getOpenFileName(self,'Open file','c:\\','Config Files(*.conf)')
        if fname[0]:    
            with open(fname[0], "r") as fi:
                f = fi.read()
                a = f.find("CellType", 0)
                b = f.find("\n", a)
                CellType  = f[a+len("CellType")+1:b]
                if CellType == "DigitalRRAMTHU":
                    self.params = {}
                    paramlist = ["CellType", "WeightBits", "CellBits",
                        "Rmax", "Rmin", "ReadVoltage", "IOBits",
                        "numArrayCol", "numArrayRow", "numCoreVMax",
                        "numCoreHMax"]
                    for i in paramlist:
                        a = f.find("-"+i, 0)
                        b = f.find("\n", a)
                        paramvalue = f[a+len(i)+2:b]
                        self.params[i] = paramvalue
                    self.txtT2CoreVMax.setText(self.params["numCoreVMax"])
                    self.txtT2CoreHMax.setText(self.params["numCoreHMax"])
                    self.txtT2IOBits.setText(self.params["IOBits"])
                    self.txtT2ArrayCol.setText(self.params["numArrayCol"])
                    self.txtT2ArrayRow.setText(self.params["numArrayRow"])
                    self.txtT2WeightBits.setText(self.params["WeightBits"])
                    self.txtT2CellBits.setText(self.params["CellBits"])
                    self.txtT2RMin.setText(self.params["Rmin"])
                    self.txtT2RMax.setText(self.params["Rmax"])
                    self.txtT2Voltage.setText(self.params["ReadVoltage"])
                
                    
    #T2 config:Save settings
    def T2save(self):
        fname = QFileDialog.getSaveFileName(self,'Open file','c:\\','Config Files(*.conf)')
        if fname[0]:
            i=0
            with open(fname[0],'w') as f:
                f.write("-DesignOptimization None\n")
                f.write("-numCoreVMax "+self.txtT2CoreVMax.text()+"\n")
                f.write("-numCoreHMax "+self.txtT2CoreHMax.text()+"\n")
                f.write("-IOBits "+self.txtT2IOBits.text()+"\n")
                f.write("-numArrayCol "+self.txtT2ArrayCol.text()+"\n")
                f.write("-numArrayRow "+self.txtT2ArrayRow.text()+"\n")
                f.write("-CellType DigitalRRAMTHU\n")
                f.write("-WeightBits "+self.txtT2WeightBits.text()+"\n")
                f.write("-CellBits "+self.txtT2CellBits.text()+"\n")
                f.write("-Rmin "+self.txtT2RMin.text()+"\n")
                f.write("-Rmax "+self.txtT2RMax.text()+"\n")
                f.write("-ReadVoltage "+self.txtT2Voltage.text()+"\n")
        
    #T2 config:Default settings
    def T2default(self):
        self.txtT2CoreVMax.setText("20")
        self.txtT2CoreHMax.setText("20")
        self.txtT2IOBits.setText("8")
        self.txtT2ArrayCol.setText("256")
        self.txtT2ArrayRow.setText("256")
        self.txtT2WeightBits.setText("8")
        self.txtT2CellBits.setText("4")
        self.txtT2RMin.setText("25e3")
        self.txtT2RMax.setText("265e3")
        self.txtT2Voltage.setText("0.15")
        
    #T1 net:import list
    def T1import(self):
        fname = QFileDialog.getOpenFileName(self,'Open file','c:\\','List Files (*.list)')
        if fname[0]:
            i = self.lstT1NetList.count()
            while(i>=0):
                i=i-1
                item_deleted=self.lstT1NetList.takeItem(i)
                item_deleted=None
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
                    if i+1==self.lstT1NetList.count():
                        f.write(self.lstT1NetList.item(i).text())
                    else:
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
            
    def tabchanged(self):
        #print(self.tabWidget.currentIndex())
        if self.tabWidget.currentIndex() == 2:
            i = self.lstT3NetList.count()
            while(i>=0):
                i=i-1
                item_deleted=self.lstT3NetList.takeItem(i)
                item_deleted=None
            i = 0
            while(i<self.lstT1NetList.count()):
                self.lstT3NetList.addItem(self.lstT1NetList.item(i).text())
                i=i+1
            i = self.lstT3ConfigList.count()
            while(i>=0):
                i=i-1
                item_deleted=self.lstT3ConfigList.takeItem(i)
                item_deleted=None
            i = 0
            while(i<self.lstT2ConfigList.count()):
                self.lstT3ConfigList.addItem(self.lstT2ConfigList.item(i).text())
                i=i+1
            self.txtT3OpenNet.setText(self.txtT1OpenNet.text())
            self.txtT3BatchSize.setText(self.txtT1BatchSize.text())
            self.txtT3EPoch.setText(self.txtT1EPoch.text())
            self.txtT3Path.setText(self.txtT1Path.text())
  
if __name__=="__main__":  
    import sys  
  
    app=QtWidgets.QApplication(sys.argv)  
    myshow=mywindow()  
    myshow.show()  
    sys.exit(app.exec_())