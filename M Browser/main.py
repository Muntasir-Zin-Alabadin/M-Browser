from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5 import QtGui
from ursina import *
import json
import style
import runpy
from ftplib import FTP
from PyQt5.QtWidgets import QInputDialog
import urllib.request
import random
import sys
import os

bookmarks = []
bookmarkAddress = []
history = []
historyAddress = []

with open('bookmarks/bookmarks.json') as json_file:
    bookmarks = json.load(json_file)
    
with open('history.json') as json_file2:
    history = json.load(json_file2)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))
        global Browser
        Browser = self.browser
        self.setCentralWidget(self.browser)
        self.showMaximized()
        self.BookmarksWindow = BookmarksWindow()
        self.HistoryWindow = HistoryWindow()
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)
        self.setCentralWidget(self.browser)
        self.FTPWindow = FTPWindow()
        app.setWindowIcon(QtGui.QIcon('icons/MB logo.png'))
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        navtb = QToolBar("Nav")
        self.addToolBar(navtb) 
        navtb.setMovable(0)
        navtb.setContextMenuPolicy(Qt.PreventContextMenu)
        
        back_btn = QAction(self)
        back_btn.setIcon(QIcon("icons/back.png"))
        back_btn.setStatusTip("Back to the previous page")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)
        
        home_btn = QAction("Home", self)
        home_btn.setIcon(QIcon("icons/home.png"))
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)
        
        next_btn = QAction("Forward", self)
        next_btn.setIcon(QIcon("icons/forward.png"))
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.setIcon(QIcon("icons/refresh.png"))
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)
        
        navtb.addSeparator()
        
        stop_btn = QAction("X", self)
        stop_btn.setIcon(QIcon("icons/cross.png"))
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
    
        bookmark_btn = QAction("Bookmark", self)
        bookmark_btn.setIcon(QIcon("icons/bookmark.png"))
        bookmark_btn.setStatusTip("Bookmark this page")
        bookmark_btn.triggered.connect(self.addToBookmarks)
        navtb.addAction(bookmark_btn)
        
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        navtb.addWidget(self.spacer)
        
        viewBookmarks_btn = QAction("View Bookmarks", self)
        viewBookmarks_btn.setIcon(QIcon("icons/book-bookmark.png"))
        viewBookmarks_btn.setStatusTip("View all bookmarks")
        viewBookmarks_btn.triggered.connect(self.passingInfo)
        navtb.addAction(viewBookmarks_btn)
        
        snake_btn = QAction("Play Snake", self)
        snake_btn.setIcon(QIcon("icons/joystick.png"))
        snake_btn.setStatusTip("Play Snake")
        snake_btn.triggered.connect(self.playsnake)  
        navtb.addAction(snake_btn)      
        
        FTP_btn = QAction("FTP", self)
        FTP_btn.setIcon(QIcon("icons/ftp.png"))
        FTP_btn.setStatusTip("FTP")
        FTP_btn.triggered.connect(self.FTP)
        navtb.addAction(FTP_btn)
        
        viewHistory_btn = QAction("View History", self)
        viewHistory_btn.setIcon(QIcon("icons/history.png"))
        viewHistory_btn.setStatusTip("View history")
        viewHistory_btn.triggered.connect(self.passing)
        navtb.addAction(viewHistory_btn)
        
        self.show()
        
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - M" % title)
        
    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)
        
    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
        self.addToHistory()
    
    def addToBookmarks(self):
        a = (self.urlbar.text())
        b=str(a)
        if b in bookmarks:
            pass
        elif b == "":
            pass
        else:
            bookmarks.append(b)
        jsonObject = json.dumps(bookmarks)
        with open('bookmarks/bookmarks.json','w') as outfile:
            outfile.write(jsonObject)
            
    def addToHistory(self):
        a = (self.urlbar.text())
        b=str(a)
        if b == "":
            pass
        else:
            history.append(b)
        jsonObject = json.dumps(history)
        with open('history.json','w') as outfile:
            outfile.write(jsonObject)

    def passingInfo(self):
        self.BookmarksWindow.displayInfo()
        
    def passing(self):
        self.HistoryWindow.displayInfo()
        
    def playsnake(self):
        runpy.run_path(path_name='snake.py')
        
    def FTP(self):
        self.FTPWindow.displayInfo()

class BookmarksWindow(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        self.setWindowTitle('Bookmarks')
        self.move(0,0)
        layout = QGridLayout()
        self.listwidget = QListWidget()
        for x in bookmarks:
            i = 0
            self.listwidget.insertItem(i, x)
            i = i + 1
        self.listwidget.itemClicked.connect(self.getItem)
        layout.addWidget(self.listwidget, 0, 0, 1, 0)
        connect = QPushButton('Connect', self)
        connect.clicked.connect(self.connect)
        refresh = QPushButton('Refresh', self)
        refresh.clicked.connect(self.refresh)
        delete = QPushButton('Delete', self)
        delete.clicked.connect(self.delete)
        layout.addWidget(connect, 1, 0)
        layout.addWidget(refresh, 1, 1)
        layout.addWidget(delete, 1, 2)
        self.setLayout(layout)
          
    def getItem(self, clickedItem):
        self.item = clickedItem.text()
        
    def connect(self):
        address = self.item
        Browser.setUrl(QUrl(address))
        
    def refresh(self):
        self.listwidget.clear()
        for x in bookmarks:
            i = 0
            self.listwidget.insertItem(i, x)
            i = i + 1
        
    def delete(self):
        address = self.item
        if len(bookmarks) != 0:
            bookmarks.remove(address)
        self.listwidget.clear()
        for x in bookmarks:
            i = 0
            self.listwidget.insertItem(i, x)
            i = i + 1
        jsonObject = json.dumps(bookmarks)
        with open('bookmarks/bookmarks.json','w') as outfile:
            outfile.write(jsonObject)
            
    def addToHistory(self):
        a = self.item
        b=str(a)
        if b == "":
            pass
        else:
            history.append(b)
        jsonObject = json.dumps(history)
        with open('history.json','w') as outfile:
            outfile.write(jsonObject)
        
    def displayInfo(self):
        self.show()
        
class HistoryWindow(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        self.setWindowTitle('History')
        self.move(0,0)
        layout = QGridLayout()
        self.listwidget = QListWidget()
        global list
        list = self.listwidget
        for x in history:
            i = 0
            self.listwidget.insertItem(i, x)
            i = i + 1
        self.listwidget.itemClicked.connect(self.getItem)
        layout.addWidget(self.listwidget, 0, 0, 1, 0)
        connect = QPushButton('Connect', self)
        connect.clicked.connect(self.connect)
        refresh = QPushButton('Refresh', self)
        refresh.clicked.connect(self.refresh)
        delete = QPushButton('Delete', self)
        delete.clicked.connect(self.delete)
        layout.addWidget(connect, 1, 0)
        layout.addWidget(refresh, 1, 1)
        layout.addWidget(delete, 1, 2)
        self.setLayout(layout)
          
    def getItem(self, clickedItem):
        self.item = clickedItem.text()
        self.index = list.currentRow()
        
    def connect(self):
        address = self.item
        index = self.index
        Browser.setUrl(QUrl(address))
        
    def refresh(self):
        self.listwidget.clear()
        for x in history:
            i = 0
            self.listwidget.insertItem(i, x)
            i = i + 1
        
    def delete(self):
        address = self.item
        index = self.index
        index = index + 1
        ind = len(history) - index
        if len(history) != 0:
            history.pop(ind)
        self.listwidget.clear()
        for x in history:
            i = 0
            self.listwidget.insertItem(i, x)
            i = i + 1
        jsonObject = json.dumps(history)
        with open('history.json','w') as outfile:
            outfile.write(jsonObject)
        
    def addToHistory(self):
        a = self.item
        b=str(a)
        if b == "":
            pass
        else:
            history.append(b)
        jsonObject = json.dumps(history)
        with open('history.json','w') as outfile:
            outfile.write(jsonObject)
        
    def displayInfo(self):
        self.show()
        
    def displayInfo(self):
        self.show()

class FTPWindow(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(350)
        self.setFixedWidth(500)
        self.setWindowTitle('FTP')
        self.move(0,0)
        allFiles = []
        session = FTP('ftp.byethost12.com', timeout=9999)
        session.cwd('MBrowser')
        allFiles = session.nlst()
        layout = QGridLayout()
        self.listwidget = QListWidget()
        for x in allFiles:
            i = 0
            if x == ".":
                pass
            elif x == "..":
                pass
            else:
                self.listwidget.insertItem(i, x)
                i = i + 1
        self.listwidget.itemClicked.connect(self.clicked)
        layout.addWidget(self.listwidget, 0, 0, 1, 0)
        send = QPushButton("Upload", self)
        send.clicked.connect(self.upload)
        delete = QPushButton('Delete', self)
        delete.clicked.connect(self.delete)
        receive = QPushButton("Download", self)
        receive.clicked.connect(self.download)
        layout.addWidget(send, 1, 0)
        layout.addWidget(delete, 1, 1)
        layout.addWidget(receive, 1, 2)
        self.setLayout(layout)
        session.quit()
        
    def open_dialog_box(self):
        fileName = QFileDialog.getOpenFileName()
        
    def upload(self):    
        session = FTP('ftp.byethost12.com', timeout=9999)
        session.cwd('MBrowser')
        fileName = QFileDialog.getOpenFileName(parent=self, caption='Select the file you want to upload', directory=os.getcwd())
        fileName = str(fileName)
        fileName = fileName.replace("', 'All Files (*)')","")
        fileName = fileName.replace("('","")
        name = os.path.basename(fileName)
        file = open(fileName,'rb')                 
        session.storbinary('STOR %s'%name, file)     
        file.close()                                    
        session.retrlines('LIST')
        allFiles = session.nlst()
        self.listwidget.clear()
        for x in allFiles:
            i = 0
            if x == ".":
                pass
            elif x == "..":
                pass
            else:
                self.listwidget.insertItem(i, x)
                i = i + 1
        
        session.quit()
        
        
    def download(self):
        session = FTP('ftp.byethost12.com', timeout=9999)
        session.cwd('MBrowser')
        filename = "pic.png"
        filename = self.item
        with open(filename, "wb") as file:
            session.retrbinary(f"RETR {filename}", file.write)
        session.quit()
        
    def delete(self):
        session = FTP('ftp.byethost12.com', timeout=9999)
        session.cwd('MBrowser')
        filename = self.item
        session.delete(filename)
        allFiles = session.nlst()
        self.listwidget.clear()
        for x in allFiles:
            i = 0
            if x == ".":
                pass
            elif x == "..":
                pass
            else:
                self.listwidget.insertItem(i, x)
                i = i + 1
        session.quit()
    
    def clicked(self, clickedItem):
        self.item = clickedItem.text()
        
    def displayInfo(self):
        self.show()     
        

app = QApplication(sys.argv)
QApplication.setApplicationName('M Browser')
window = MainWindow()
app.setStyleSheet(style.stylesheet)
app.exec_()