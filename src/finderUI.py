from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow, QTableWidgetItem, QFileDialog,QHeaderView,QActionGroup
import sys
import os
from commonutils import calculateDistance  
import argparse
import subprocess
from gzip import compress as gc
from lzma import compress as lc
from bz2 import compress as bc

class ConvertThread(QtCore.QThread): #worker that performs file comparison
    
    progress = QtCore.pyqtSignal(object) #Async UI thread updating

    def __init__(self, filename,db,tempfile,cp,cached=False):
        QtCore.QThread.__init__(self)
        self.filename = filename
        self.db = db
        self.tempfilename = tempfile
        self.compress = cp
        self.cached = cached

    def run(self):
        cmd = ["./GetMaxFreqs", "-w", self.tempfilename, self.filename]
        popen = subprocess.Popen(cmd)
        popen.wait()
        try:
            with open(self.tempfilename, "rb") as f:
                trans = f.read()
        except:
            self.progress.emit({"title":f"Failed to process {self.filename}"})
            return
        results = []
        if self.cached:
            totalfiles = len(self.db.keys())
            counter = 0
            for keyname,modelbytes in self.db.items():
                results.append( (keyname, calculateDistance(trans,modelbytes,self.compress) ))
                counter+=1
                prog = int(counter/totalfiles*100)
                results  = sorted(results,key=lambda x: x[1])[:10]
                self.progress.emit( {"percent":prog,"results":results} )
                self.progress.emit({"title":f"Finished Processing {self.filename}"})
            return
        
        #irrelevant if DB is already in memory
        filelist = os.listdir(self.db)
        filelist = [ f for f in filelist if not os.path.isdir(f"{self.db}/{f}")] # remove dirs from consideration
        totalfiles = len(filelist)
        counter = 0
        for f in filelist:
            keyname = f.removesuffix(".freqs")
            fullpath = f"{self.db}/{f}"
            with open(fullpath,"rb") as tmpfile:
                modelbytes = tmpfile.read()
            results.append( (keyname, calculateDistance(trans,modelbytes,self.compress) ))
            counter+=1
            prog = int(counter/totalfiles*100)
            results  = sorted(results,key=lambda x: x[1])[:10]
            self.progress.emit( {"percent":prog,"results":results} )
            self.progress.emit({"title":f"Finished Processing {self.filename}"})


class Ui_MainWindow(object):
    
    def closeEvent(self, event):
        # here you can terminate your threads and do other stuff
        if self.workThread:
            self.workThread.exit()
        if os.path.exists(self.tempfilename):
            os.remove(self.tempfilename)
        # and afterwards call the closeEvent of the super-class
        super(QMainWindow, self).closeEvent(event)
        
    def setupUi(self, MainWindow,db,cache): #This function is automatically generated other than small segments for the most part it's fully ignorable

        #state management
        self.tempfilename = "./tempfile"
        tempfilenum = 0
        while os.path.exists(f"{self.tempfilename}{tempfilenum}.freqs"):
            tempfilenum+=1
        self.tempfilename+=str(tempfilenum)+".freqs"
        self.compress = gc
        self.db = db
        self.cache = cache

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(783, 629)
        MainWindow.setMaximumSize(QtCore.QSize(783, 629))
        MainWindow.setMinimumSize(QtCore.QSize(783, 629))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget_8 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_8.setGeometry(QtCore.QRect(-10, 0, 811, 601))
        self.horizontalLayoutWidget_8.setObjectName("horizontalLayoutWidget_8")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_8)
        self.horizontalLayout_13.setContentsMargins(30, 20, 30, 10)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.splitter = QtWidgets.QSplitter(self.horizontalLayoutWidget_8)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.horizontalWidget_5 = QtWidgets.QWidget(self.splitter)
        self.horizontalWidget_5.setMaximumSize(QtCore.QSize(16777215, 50))
        self.horizontalWidget_5.setObjectName("horizontalWidget_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.horizontalWidget_5)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.filename_label = QtWidgets.QLabel(self.horizontalWidget_5)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.filename_label.setFont(font)
        self.filename_label.setText("")
        self.filename_label.setAlignment(QtCore.Qt.AlignCenter)
        self.filename_label.setWordWrap(True)
        self.filename_label.setObjectName("filename_label")
        self.horizontalLayout_7.addWidget(self.filename_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.progressBarContainer = QtWidgets.QWidget(self.splitter)
        self.progressBarContainer.setMaximumSize(QtCore.QSize(16777215, 50))
        self.progressBarContainer.setObjectName("progressBarContainer")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.progressBarContainer)
        self.horizontalLayout.setContentsMargins(40, 1, 40, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.progressBarContainer)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.cancel = QtWidgets.QPushButton(self.progressBarContainer)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.frame = QtWidgets.QFrame(self.splitter)
        self.setAcceptDrops(True)
        self.frame.setAcceptDrops(True)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(10)
        self.frame.setObjectName("frame")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 90, 751, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(88, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.submitbutton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.submitbutton.setObjectName("submitbutton")
        self.horizontalLayout_2.addWidget(self.submitbutton)
        spacerItem3 = QtWidgets.QSpacerItem(88, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(2, 20, 751, 80))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.frame_2 = QtWidgets.QFrame(self.splitter)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.frame_2)
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 0, 751, 259))
        self.tableWidget_2.setMinimumSize(QtCore.QSize(0, 200))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setRowCount(0)
        self.horizontalLayout_13.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        #custom code stuff
        self.frame_2.resizeEvent = self.tableFrameResizeEvent
        self.progressBarContainer.setVisible(False)
        self.frame.dragEnterEvent = lambda s: self.frameEnterEvent(s)
        self.frame.dropEvent = lambda s: self.frameDropEvent(s)
        self.cancel.clicked.connect(self.cancelThread)
        self.tableWidget_2.setHorizontalHeaderLabels(["File","Distance"])
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.submitbutton.clicked.connect(self.fileSelectPress)
        self.workThread = None
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        
        actionComp = self.menubar.addMenu("Compressor")
        self.actGroup = QActionGroup(actionComp) #group them into radio rather than checkbox

        gzipcheck = actionComp.addAction("gzip")
        self.actGroup.addAction(gzipcheck)
        gzipcheck.setCheckable(True)
        gzipcheck.setChecked(True)
        gzipcheck.triggered.connect(lambda _: self.setCompress("gzip"))
        
        lzmacheck = actionComp.addAction("lzma")
        self.actGroup.addAction(lzmacheck)
        lzmacheck.setCheckable(True)
        lzmacheck.setChecked(False)
        lzmacheck.triggered.connect(lambda _: self.setCompress("lzma"))
        
        bzipcheck = actionComp.addAction("bzip2")
        self.actGroup.addAction(bzipcheck)
        bzipcheck.setCheckable(True)
        bzipcheck.setChecked(False)
        bzipcheck.triggered.connect(lambda _: self.setCompress("bzip"))

        MainWindow.setMenuBar(self.menubar)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setCompress(self,name):
        if self.workThread:
            self.cancelThread()
        if name=="bzip":
            self.compress = bc
        elif name=="lzma":
            self.compress = lc
        elif name=="gzip":
            self.compress = gc

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Media Finder"))
        self.cancel.setText(_translate("MainWindow", "Cancel"))
        self.submitbutton.setText(_translate("MainWindow", "Or Click Here"))
        self.label.setText(_translate("MainWindow", "Drop Wav Files Here"))

    
    def frameEnterEvent(self, event):
        self.frame.setStyleSheet("QFrame#frame {border : 5px double lightblue;}")
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()


    def frameDropEvent(self, event):
        self.frame.setStyleSheet("")
        files = [u.url() for u in event.mimeData().urls()]
        if len(files)!=1:
            self.filename_label.setText("1 file at a time please")
            return
        filename = files[0]
        filename = filename[6:]
        self.processFile(filename)
        

    def dragEnterEvent(self,event):
        self.frame.setStyleSheet("QFrame#frame {border : 5px double lightblue;}")
        event.accept()

    def dragLeaveEvent(self,event):
        self.frame.setStyleSheet("")
        event.ignore()

    def dropEvent(self, event):
        self.frame.setStyleSheet("")
        event.ignore()

    def processUpdate(self,results):
        if "title" in results: #this is just a title setting message
            self.filename_label.setText(results["title"])
            return
        percent = results["percent"]
        self.progressBar.setValue(percent)
        list = results["results"]
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setRowCount(len(list))
        for idx,x in enumerate(list):
            self.tableWidget_2.setItem(idx,0,QTableWidgetItem(x[0]))
            self.tableWidget_2.setItem(idx,1,QTableWidgetItem( str(round(x[1],6))) )

    def processFile(self,filename):
        self.filename_label.setText(f"Processing results for {filename.split('/')[-1]}")
        self.progressBarContainer.setVisible(True)
        self.progressBar.setValue(0)
        self.frame.setVisible(False)
        
        if self.cache:
            self.workThread = ConvertThread(filename,self.cache,self.tempfilename,self.compress, cached=True)
        else:
            self.workThread = ConvertThread(filename,self.db,self.tempfilename,self.compress)
        self.workThread.progress.connect(self.processUpdate)
        self.workThread.finished.connect(self.resetVisuals)
        self.workThread.start()
        

    def cancelThread(self):
        self.filename_label.setText("Processing Cancelled")
        self.workThread.quit()
        self.workThread.wait()
        self.workThread = None
       
    def resetVisuals(self):
        self.progressBarContainer.setVisible(False)
        self.frame.setVisible(True)


    def fileSelectPress(self):
        file , check = QFileDialog.getOpenFileName(None, "Select an audio file",
                                               "", "All Files (*);;Wav Files (*.wav);;Flac Files (*.flac)")
        if check:
            self.processFile(file)

    def tableFrameResizeEvent(self,event):
        width = self.frame_2.frameGeometry().width()
        height = self.frame_2.frameGeometry().height()
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 0, width, height))





class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, db = None, cache = None):
        super(MyApp, self).__init__(parent)
        self.setupUi(self,db,cache)

if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--db",help="Folder with known songs", required=True)
    parser.set_defaults(mem=False)
    parser.add_argument("--cache", help="enable caching database", dest="mem",action="store_true")
    parser.add_argument("--no-cache", help="disable caching database, default state", dest="mem",action="store_false")
    args = parser.parse_args()

    cache = None
    if args.mem:
        filelist = os.listdir(args.db)
        filelist = [ f for f in filelist if not os.path.isdir(f"{args.db}/{f}")] # remove dirs from consideration
        cache = {}
        for f in filelist:
            keyname = f.removesuffix(".freqs")
            fullpath = f"{args.db}/{f}"
            with open(fullpath,"rb") as tmpfile:
                modelbytes = tmpfile.read()
                cache[keyname] = modelbytes

    app = QApplication(sys.argv)
    form = MyApp(db=args.db, cache= cache)
    form.show()
    sys.exit(app.exec_())