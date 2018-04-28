# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, 
    QAction, QFileDialog, QApplication, QTextEdit)
from PyQt5.QtCore import QThread,Qt,pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from test import Ui_MainWindow
import re
import subprocess
from pathlib import Path
import time

defaultPath = 'C:\\' 

class toPrint(QThread):
    output = pyqtSignal(str)
    cont = pyqtSignal()
    def __init__(self,p,tasknum,setflag):
        super().__init__()
        self.p = p
        self.tasknum = tasknum
        self.setflag = setflag
        
    def run(self):
        returncode = self.p.poll()    
        #print(self.p)
        #print("toPrint running,return code is:"+str(returncode))
        while returncode is None:   #检查子程序是否结束
            line = self.p.stdout.readline()    #若没有，则获取子程序的输出
            returncode = self.p.poll()
            line = line.strip()
            self.output.emit(line)
            #print(line)
        self.output.emit(self.p.stdout.read())
        if self.tasknum==1 and self.setflag:
            self.cont.emit()
    

class mywindow(QtWidgets.QMainWindow,Ui_MainWindow): 
    p=0
    q=0
    def __init__(self): 
        super(mywindow,self).__init__()  
        self.setupUi(self)  
        self.tabWidget.currentChanged.connect(self.tabchanged)      
        #T1 net:open net file
        self.btnT1OpenNet.clicked.connect(self.openT1net)
        #T1 net:init combo lists
        self.cmbT1NetType.addItem("mlp")
        self.cmbT1NetType.addItem("lenet")
        self.cmbT1NetType.addItem("lenetnoise")
        self.cmbT1NetType_2.addItem("mlp")
        self.cmbT1NetType_2.addItem("cnn")
        #T1 net:confirm button 1-4
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
        #T1 net:add file button
        self.btnT1AddFile_2.clicked.connect(self.T1addfile2)
        #T1 net:remove file button
        self.btnT1RemoveFile_2.clicked.connect(self.T1removefile2)
        #T1 net:remove all file button
        self.btnT1RemoveAll_2.clicked.connect(self.T1removeall2)
        #T1 net:export file list
        self.btnT1ExportList_2.clicked.connect(self.T1export2)
        #T1 net:import file list
        self.btnT1ImportList_2.clicked.connect(self.T1import2)
        #T1 net:Path Selection
        self.btnT1PathSelection.clicked.connect(self.T1path)
        #T1 net:add type into type list
        self.btnT1AddType.clicked.connect(self.T1addtype)
        #T1 net:remove type from type list
        self.btnT1RemoveType.clicked.connect(self.T1removetype)
        #T1 net:add size into batch size list
        self.btnT1AddSize.clicked.connect(self.T1addsize)
        #T1 net:remove size from batch size list
        self.btnT1RemoveSize.clicked.connect(self.T1removesize)
        
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
        #T3 test case:add image file
        self.btnT3AddImage.clicked.connect(self.T3addimage)
        #T3 test case:remove image file
        self.btnT3RemoveImage.clicked.connect(self.T3removeimage)
        #T3 test case:remove all image
        self.btnT3RemoveAllImage.clicked.connect(self.T3removeallimage)
        #T3 test case:add config file
        self.btnT3AddConfig.clicked.connect(self.T3addconfig)
        #T3 test case:remove config file
        self.btnT3RemoveConfig.clicked.connect(self.T3removeconfig)
        #T3 test case:remove all config file
        self.btnT3RemoveAllConfig.clicked.connect(self.T3removeallconfig)
        #T3 test case:open net file
        self.btnT3OpenNet.clicked.connect(self.T3opennet)
        #T3 test case:select output path
        self.btnT3PathSelection.clicked.connect(self.T3path)
        #T3 test case:save test case
        self.btnT3SaveCase.clicked.connect(self.T3savecase)
        #T3 test case:load test case
        self.btnT3LoadCase.clicked.connect(self.T3loadcase)
        #T3 test case:confirm button
        self.btnT3Confirm1.clicked.connect(self.T3confirm)
        #T3 test case:init combo lists
        self.cmbT3NetType_2.addItem("mlp")
        self.cmbT3NetType_2.addItem("cnn")
        self.cmbT3NetType.addItem("mlp")
        self.cmbT3NetType.addItem("lenet")
        self.cmbT3NetType.addItem("lenetnoise")           
        #T3 test case:add type into type list
        self.btnT3AddType.clicked.connect(self.T3addtype)
        #T3 test case:remove type from type list
        self.btnT3RemoveType.clicked.connect(self.T3removetype)
        #T3 test case:add size into batch size list
        self.btnT3AddSize.clicked.connect(self.T3addsize)
        #T3 test case:remove size from batch size list
        self.btnT3RemoveSize.clicked.connect(self.T3removesize)
        
        #T4 hardware simulation:start simulation
        self.btnT4StartSimulation.clicked.connect(self.T4startsimulation)
        #T4 hardware simulation:open python path
        self.btnT4Python.clicked.connect(self.T4python)
        #
        self.cmbT4NetType.addItem("mlp")
        self.cmbT4NetType.addItem("lenet")
        self.cmbT4NetType.addItem("lenetnoise")
        #T4 hardware simulation:start train
        self.btnT4StartTrain.clicked.connect(self.T4starttrain)
        #T4 hardware simulation:open net path
        self.btnT4OpenNet.clicked.connect(self.T4opennet)
        #T4 hardware simulation:output path
        self.btnT4Output.clicked.connect(self.T4outputpath)
        
        #T5 result:clear button
        self.btnT5Clear.clicked.connect(self.T5clear)
        #T5 result:show process status
        self.btnT5ShowProcess.clicked.connect(self.T5showprocess)
        #T5 result:stop subprocess
        self.btnT5Stop.clicked.connect(self.T5stop)
        #T5 result:save result
        self.btnT5SaveResult.clicked.connect(self.T5saveresult)
               
    #T5 result:save result
    def T5saveresult(self):
        fname = QFileDialog.getSaveFileName(self,'Open file',defaultPath,'Text Files (*.txt);;All Files (*)')
        if fname[0]:            
            with open(fname[0],'w') as f:
                f.write(self.txtT5Result.toPlainText())
    
    #T5 result:stop subprocess
    def T5stop(self):
        if self.p!=0:
            self.p.terminate() 
        if self.q!=0:
            self.q.terminate()
            
    #T5 result:show process
    def T5showprocess(self):
        if self.p!=0:
            self.txtT5Result.append("Subprocess return code:"+str(self.p.poll()))
            self.txtT5Result.append("Subprocess PID:"+str(self.p.pid))           
        if self.q!=0:
            self.txtT5Result.append("Subprocess return code:"+str(self.q.poll()))
            self.txtT5Result.append("Subprocess PID:"+str(self.q.pid))
    
    #T5 result:clear
    def T5clear(self):
        reply = QMessageBox.information(self,                         #使用infomation信息框  
                                    "清空确认",  
                                    "确定清空结果显示窗口？",  
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.txtT5Result.setText("")
                                    
     
    def T5output(self,out):
        #print("T5output triggered")
        self.txtT5Result.append(out)
        
    #T4 hardware simulation:output path 
    def T4outputpath(self):
        fname = QFileDialog.getSaveFileName(self,'Open file',defaultPath,'Image Files (*.npz);;All Files (*)')
        if fname[0]:   
            self.txtT4OpenNet_2.setText(fname[0])
            with open(fname[0],'w') as f:
                f.write("")
    
    #T4 hardware simulation:open net path
    def T4opennet(self):
        fname = QFileDialog.getOpenFileName(self,'Open file',defaultPath,'Image Files (*.npz);;All Files (*)')
        if fname[0]:
            self.txtT4OpenNet.setText(fname[0])
        
        
    #T4 hardware simulation:start train
    def T4starttrain(self):
        self.tabWidget.setCurrentIndex(4)
        try:
            self.q = subprocess.Popen(self.txtT4Python.text()+"\python TrainStarter.py "+self.cmbT4NetType.currentText()+\
            " "+self.txtT4BatchSize_2.text()+" "+self.txtT4EPoch.text()+" "+self.txtT4Output.text()+" "+\
            self.txtT4OpenNet.text(),stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines=True,shell=True)
            self.th = toPrint(self.q,1,self.chkT4auto.isChecked())
            self.th.output.connect(self.T5output)
            self.th.cont.connect(self.T4startsimulation)
            self.th.start()

        except FileNotFoundError:
            self.txtT5Result.setText("FileNotFoundError!\n")    
            
    #T4 hardware simulation:open python path
    def T4python(self):
        fname = QFileDialog.getExistingDirectory(self,'Open file',defaultPath)
        if fname:
            self.txtT4Python.setText(fname)
        
    #T4 hardware sumulation:start simulation
    def T4startsimulation(self):
        self.tabWidget.setCurrentIndex(4)
        for i in range(self.lstT4NetList.count()):
            if self.lstT4ImageList.count()<=i:
                break
            if self.lstT4ConfigList.count()<=i:
                break
            if self.lstT4TypeList.count()<=i:
                break
            if self.lstT4SizeList.count()<=i:
                break
            try:
                self.p = subprocess.Popen(self.txtT4Python.text()+"\python SimStarter.py "+self.lstT4NetList.item(i).text()+\
                " "+self.lstT4ImageList.item(i).text()+" "+self.lstT4SizeList.item(i).text()+" "+self.lstT4TypeList.item(i).text()+" "+\
                self.lstT4ConfigList.item(i).text(),shell=True,stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines=True)
                self.th = toPrint(self.p,2,False)
                self.th.output.connect(self.T5output)
                self.th.start()    
            except FileNotFoundError:
                self.txtT5Result.setText("FileNotFoundError!\n")
     
    #T3 test case:remove size from batch size list
    def T3removesize(self):
        item_deleted=self.lstT3SizeList.takeItem(self.lstT3SizeList.currentRow())
        item_deleted=None
        
    #T3 test case:add size into batch size list
    def T3addsize(self):
        self.lstT3SizeList.addItem(self.txtT3BatchSize_3.text())
    
    #T3 test case:remove type from type list
    def T3removetype(self):
        item_deleted=self.lstT3TypeList.takeItem(self.lstT3TypeList.currentRow())
        item_deleted=None
    
    #T3 test case:Add net type into type list
    def T3addtype(self):
        self.lstT3TypeList.addItem(self.cmbT3NetType_2.currentText())
     
    #T3 test case:confirm button
    def T3confirm(self):
        self.tabWidget.setCurrentIndex(3)
        
    #T3 test case:load test case
    def T3loadcase(self):
        fname = QFileDialog.getOpenFileName(self,'Open file',defaultPath,'Test case Files (*.case);;All Files (*)')
        if fname[0]:    
            with open(fname[0], "r") as fi:
                f = fi.read()
                
                a = f.find("?Net", 0)
                b = f.find("?", a+1)
                Net = f[a+len("?Net")+1:b-1]
                names = re.split('\n',Net)
                i = self.lstT3NetList.count()
                while(i>=0):
                    i=i-1
                    item_deleted=self.lstT3NetList.takeItem(i)
                    item_deleted=None
                i = self.lstT1NetList.count()
                while(i>=0):
                    i=i-1
                    item_deleted=self.lstT1NetList.takeItem(i)
                    item_deleted=None           
                for name in names:
                    self.lstT3NetList.addItem(name) 
                    self.lstT1NetList.addItem(name)
                
                a = f.find("?Image", 0)
                b = f.find("?", a+1)
                Image = f[a+len("?Image")+1:b-1]
                names = re.split('\n',Image)
                i = self.lstT3ImageList.count()
                while(i>=0):
                    i=i-1
                    item_deleted=self.lstT3ImageList.takeItem(i)
                    item_deleted=None
                i = self.lstT1ImageList.count()
                while(i>=0):
                    i=i-1
                    item_deleted=self.lstT1ImageList.takeItem(i)
                    item_deleted=None          
                for name in names:
                    self.lstT3ImageList.addItem(name)
                    self.lstT1ImageList.addItem(name)
                
                a = f.find("?Config", 0)
                b = f.find("?", a+1)
                Config = f[a+len("?Config")+1:b-1]
                names = re.split('\n',Config)
                i = self.lstT3ConfigList.count()
                while(i>=0):
                    i=i-1
                    item_deleted=self.lstT3ConfigList.takeItem(i)
                    item_deleted=None
                i = self.lstT2ConfigList.count()
                while(i>=0):
                    i=i-1
                    item_deleted=self.lstT2ConfigList.takeItem(i)
                    item_deleted=None
                for name in names:
                    self.lstT3ConfigList.addItem(name)
                    self.lstT2ConfigList.addItem(name)
                    
                a = f.find("?SizeList", 0)
                b = f.find("?", a+1)
                sizelist = f[a+len("?SizeList")+1:b-1]
                names = re.split('\n',sizelist)
                i = self.lstT3SizeList.count()
                while(i>=0):
                    i=i-1
                    item_deleted=self.lstT3SizeList.takeItem(i)
                    item_deleted=None
                i = self.lstT1SizeList.count()
                while(i>=0):
                    i=i-1
                    item_deleted=self.lstT1SizeList.takeItem(i)
                    item_deleted=None
                for name in names:
                    self.lstT3SizeList.addItem(name)
                    self.lstT1SizeList.addItem(name)
                    
                a = f.find("?TypeList", 0)
                b = f.find("?", a+1)
                TypeList = f[a+len("?TypeList")+1:b-1]
                names = re.split('\n',TypeList)
                i = self.lstT3TypeList.count()
                while(i>=0):
                    i=i-1
                    item_deleted=self.lstT3TypeList.takeItem(i)
                    item_deleted=None
                i = self.lstT1TypeList.count()
                while(i>=0):
                    i=i-1
                    item_deleted=self.lstT1TypeList.takeItem(i)
                    item_deleted=None
                for name in names:
                    self.lstT3TypeList.addItem(name)
                    self.lstT1TypeList.addItem(name)
                    
                a = f.find("?Train",0)
                b = f.find("\n", a)
                Batch = f[a+len("?Train")+1:b]
                self.txtT3BatchSize.setText(Batch)
                self.txtT1BatchSize.setText(Batch)
                
                a = b+1
                b = f.find("\n",a)
                EPoch = f[a:b]
                self.txtT3EPoch.setText(EPoch)
                self.txtT1EPoch.setText(EPoch)
                
                a = b+1
                b = f.find("\n",a)
                SNet = f[a:b]
                self.txtT3OpenNet.setText(SNet)
                self.txtT1OpenNet.setText(SNet)
                
                a = b+1
                b = f.find("\n",a)
                Path = f[a:b]
                self.txtT3OutputPath.setText(Path)
                self.txtT1OutputPath.setText(Path)
                
                a = b+1
                b = f.find("\n",a)
                Type = f[a:b]
                t = self.cmbT3NetType.findText(Type)
                self.cmbT3NetType.setCurrentIndex(t)
                self.cmbT1NetType.setCurrentIndex(t)
                
        
    #T3 test case:save test case
    def T3savecase(self):
        fname = QFileDialog.getSaveFileName(self,'Open file',defaultPath,'Test case Files (*.case);;All Files (*)')
        if fname[0]:            
            with open(fname[0],'w') as f:
                f.write("?Net ")
                i=0
                while(i<self.lstT3NetList.count()):
                    f.write(self.lstT3NetList.item(i).text()+"\n")
                    i=i+1  
                f.write("?Image ")
                i=0
                while(i<self.lstT3ImageList.count()):
                    f.write(self.lstT3ImageList.item(i).text()+"\n")
                    i=i+1  
                f.write("?Config ")
                i=0
                while(i<self.lstT3ConfigList.count()):
                    f.write(self.lstT3ConfigList.item(i).text()+"\n")
                    i=i+1  
                f.write("?SizeList ")
                i=0
                while(i<self.lstT3SizeList.count()):
                    f.write(self.lstT3SizeList.item(i).text()+"\n")
                    i=i+1 
                f.write("?TypeList ")
                i=0
                while(i<self.lstT3TypeList.count()):
                    f.write(self.lstT3TypeList.item(i).text()+"\n")
                    i=i+1 
                
                f.write("?Train ")
                f.write(self.txtT3BatchSize.text()+"\n")
                f.write(self.txtT3EPoch.text()+"\n")
                f.write(self.txtT3OpenNet.text()+"\n") 
                f.write(self.txtT3OutputPath.text()+"\n")
                f.write(self.cmbT3NetType.currentText()+"\n")

                
    #T3 test case:select output path
    def T3path(self):
        fname = QFileDialog.getSaveFileName(self,'Open file',defaultPath,'Image Files (*.npz);;All Files (*)')
        if fname[0]:
            self.txtT3OutputPath.setText(fname[0])
            with open(fname[0],'w') as f:
                f.write("")
                
    #T3 test case:open net file
    def T3opennet(self):
        fname = QFileDialog.getOpenFileName(self,'Open file',defaultPath,'Net Files (*.npz);;All Files (*)')
        if fname[0]:
            self.txtT3OpenNet.setText(fname[0])
        
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
        fname = QFileDialog.getExistingDirectory(self,'Open file',defaultPath)
        if fname:
            self.lstT3ConfigList.addItem(fname)
    
    #T3 test case:remove all image
    def T3removeallimage(self):
        i = self.lstT3ImageList.count()
        while(i>=0):
            i=i-1
            item_deleted=self.lstT3ImageList.takeItem(i)
            item_deleted=None
            
    #T3 test case:remove image file
    def T3removeimage(self):
        item_deleted=self.lstT3ImageList.takeItem(self.lstT3ImageList.currentRow())
        item_deleted=None
        
    #T3 test case:add image file
    def T3addimage(self):
        fname = QFileDialog.getOpenFileNames(self,'Open file',defaultPath,'Image Files (*.npy);;All Files (*)')
        if fname[0]:
            for name in fname[0]:
                self.lstT3ImageList.addItem(name)
    
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
        fname = QFileDialog.getOpenFileNames(self,'Open file',defaultPath,'Net Files (*.npz);;All Files (*)')
        if fname[0]:
            for name in fname[0]:
                self.lstT3NetList.addItem(name)
    
    #T2 config:confirm
    def T2confirm(self):
        self.tabWidget.setCurrentIndex(2)

    #T2 Config:import list
    def T2import(self):
        fname = QFileDialog.getOpenFileName(self,'Open file',defaultPath,'Config List Files (*.Clist);;All Files (*)')
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
        fname = QFileDialog.getSaveFileName(self,'Open file',defaultPath,'Config List Files (*.Clist);;All Files (*)')
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
        fname = QFileDialog.getExistingDirectory(self,'Open file',defaultPath)
        if fname:
            self.lstT2ConfigList.addItem(fname)

     
    #T2 config:Load settings
    def T2load(self):
        fname = QFileDialog.getOpenFileName(self,'Open file',defaultPath,'Config Files(*.conf);;All Files (*)')
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
        fname = QFileDialog.getExistingDirectory(self,'Open file',defaultPath)
        if fname:
            a = fname+'/simconfig'
            b = Path(a)
            if b.exists():
                result = QMessageBox.information(self,                        
                                    "文件覆盖警告",  
                                    "确定要覆盖当前目录中的simconfig文件么？",  
                                    QMessageBox.Yes | QMessageBox.No)  
            
                if result==QMessageBox.Yes:
                    i=0
                    with open(a,'w') as f:
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
                    
            else:
                i=0
                with open(a,'w') as f:
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
    

    #T1 net:remove size from batch size list
    def T1removesize(self):
        item_deleted=self.lstT1SizeList.takeItem(self.lstT1SizeList.currentRow())
        item_deleted=None
        
    #T1 net:add size into batch size list
    def T1addsize(self):
        self.lstT1SizeList.addItem(self.txtT1BatchSize_3.text())
    
    #T1 net:remove type from type list
    def T1removetype(self):
        item_deleted=self.lstT1TypeList.takeItem(self.lstT1TypeList.currentRow())
        item_deleted=None
    
    #T1 net:Add net type into type list
    def T1addtype(self):
        self.lstT1TypeList.addItem(self.cmbT1NetType_2.currentText())
    
    #T1 net:Path selection
    def T1path(self):
        fname = QFileDialog.getSaveFileName(self,'Open file',defaultPath,'Image Files (*.npz);;All Files (*)')
        if fname[0]:
            self.txtT1OutputPath.setText(fname[0])
            with open(fname[0],'w') as f:
                f.write("")
     
    #T1 net:import list
    def T1import2(self):
        fname = QFileDialog.getOpenFileName(self,'Open file',defaultPath,'List Files (*.list);;All Files (*)')
        if fname[0]:
            i = self.lstT1ImageList.count()
            while(i>=0):
                i=i-1
                item_deleted=self.lstT1ImageList.takeItem(i)
                item_deleted=None
            with open(fname[0],'r') as f:
                my_txt=f.read()
                m=re.split('\n',my_txt)
                for name in m:               
                    self.lstT1ImageList.addItem(name)

    #T1 net:export list
    def T1export2(self):
        fname = QFileDialog.getSaveFileName(self,'Open file',defaultPath,'List Files (*.list);;All Files (*)')
        if fname[0]:
            i=0
            with open(fname[0],'w') as f:
                while(i<self.lstT1ImageList.count()):
                    if i+1==self.lstT1ImageList.count():
                        f.write(self.lstT1ImageList.item(i).text())
                    else:
                        f.write(self.lstT1ImageList.item(i).text()+"\n")
                    i=i+1              


    #T1 net:remove all button
    def T1removeall2(self):
        i = self.lstT1ImageList.count()
        while(i>=0):
            i=i-1
            item_deleted=self.lstT1ImageList.takeItem(i)
            item_deleted=None

    #T1 net:remove file button
    def T1removefile2(self):
        item_deleted=self.lstT1ImageList.takeItem(self.lstT1ImageList.currentRow())
        item_deleted=None

    #T1 net:add file button
    def T1addfile2(self):
        fname = QFileDialog.getOpenFileNames(self,'Open file',defaultPath,'Image Files (*.npy);;All Files (*)')
        if fname[0]:
            for name in fname[0]:
                self.lstT1ImageList.addItem(name)
     
    #T1 net:import list
    def T1import(self):
        fname = QFileDialog.getOpenFileName(self,'Open file',defaultPath,'List Files (*.list);;All Files (*)')
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
        fname = QFileDialog.getSaveFileName(self,'Open file',defaultPath,'List Files (*.list);;All Files (*)')
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
        fname = QFileDialog.getOpenFileNames(self,'Open file',defaultPath,'Net Files (*.npz);;All Files (*)')
        if fname[0]:
            for name in fname[0]:
                self.lstT1NetList.addItem(name)

    #T1 net:confirm button 1-3
    def T1confirm(self):
        self.tabWidget.setCurrentIndex(1)

    #T1 net:open import net file
    #def openT1importnet(self):
    #    fname = QFileDialog.getOpenFileName(self,'Open file',defaultPath)
    #    if fname[0]:
    #        self.txtT1ImportNet.setText(fname[0])     

    #T1 net:open import image file
    #def openT1importimage(self):
    #    fname = QFileDialog.getOpenFileName(self,'Open file',defaultPath)
    #    if fname[0]:
    #        self.txtT1ImportImage.setText(fname[0])             

    #T1 net:open net file
    def openT1net(self):
        fname = QFileDialog.getOpenFileName(self,'Open file',defaultPath,'Net Files (*.npz);;All Files (*)')
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
            i = self.lstT3ImageList.count()
            while(i>=0):
                i=i-1
                item_deleted=self.lstT3ImageList.takeItem(i)
                item_deleted=None
            i = 0
            while(i<self.lstT1ImageList.count()):
                self.lstT3ImageList.addItem(self.lstT1ImageList.item(i).text())
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
            i = self.lstT3SizeList.count()
            while(i>=0):
                i=i-1
                item_deleted=self.lstT3SizeList.takeItem(i)
                item_deleted=None
            i = 0
            while(i<self.lstT1SizeList.count()):
                self.lstT3SizeList.addItem(self.lstT1SizeList.item(i).text())
                i=i+1
            i = self.lstT3TypeList.count()
            while(i>=0):
                i=i-1
                item_deleted=self.lstT3TypeList.takeItem(i)
                item_deleted=None
            i = 0
            while(i<self.lstT1TypeList.count()):
                self.lstT3TypeList.addItem(self.lstT1TypeList.item(i).text())
                i=i+1
            self.txtT3OpenNet.setText(self.txtT1OpenNet.text())
            self.txtT3BatchSize.setText(self.txtT1BatchSize.text())
            self.txtT3EPoch.setText(self.txtT1EPoch.text())
            self.txtT3OutputPath.setText(self.txtT1OutputPath.text())
            self.cmbT3NetType.setCurrentIndex(self.cmbT3NetType.findText(self.cmbT1NetType.currentText()))
        if self.tabWidget.currentIndex() == 3:
            i = self.lstT4NetList.count()
            while(i>=0):
                i=i-1
                item_deleted=self.lstT4NetList.takeItem(i)
                item_deleted=None
            i = 0
            while(i<self.lstT1NetList.count()):
                self.lstT4NetList.addItem(self.lstT1NetList.item(i).text())
                i=i+1
            i = self.lstT4ImageList.count()
            while(i>=0):
                i=i-1
                item_deleted=self.lstT4ImageList.takeItem(i)
                item_deleted=None
            i = 0
            while(i<self.lstT1ImageList.count()):
                self.lstT4ImageList.addItem(self.lstT1ImageList.item(i).text())
                i=i+1
            i = self.lstT4ConfigList.count()
            while(i>=0):
                i=i-1
                item_deleted=self.lstT4ConfigList.takeItem(i)
                item_deleted=None
            i = 0
            while(i<self.lstT2ConfigList.count()):
                self.lstT4ConfigList.addItem(self.lstT2ConfigList.item(i).text())
                i=i+1
            i = self.lstT4TypeList.count()
            while(i>=0):
                i=i-1
                item_deleted=self.lstT4TypeList.takeItem(i)
                item_deleted=None
            i = 0
            while(i<self.lstT1TypeList.count()):
                self.lstT4TypeList.addItem(self.lstT1TypeList.item(i).text())
                i=i+1
            i = self.lstT4SizeList.count()
            while(i>=0):
                i=i-1
                item_deleted=self.lstT4SizeList.takeItem(i)
                item_deleted=None
            i = 0
            while(i<self.lstT1SizeList.count()):
                self.lstT4SizeList.addItem(self.lstT1SizeList.item(i).text())
                i=i+1
            self.txtT4OpenNet.setText(self.txtT1OpenNet.text())
            self.txtT4BatchSize_2.setText(self.txtT1BatchSize.text())
            self.txtT4EPoch.setText(self.txtT1EPoch.text())
            self.txtT4Output.setText(self.txtT1OutputPath.text())
            self.cmbT4NetType.setCurrentIndex(self.cmbT4NetType.findText(self.cmbT3NetType.currentText()))
            
if __name__=="__main__":  
    import sys  
  
    app=QtWidgets.QApplication(sys.argv)  
    myshow=mywindow()  
    myshow.show()  
    sys.exit(app.exec_())