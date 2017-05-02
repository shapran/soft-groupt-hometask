#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Simple application displays data from SQLite db
and allows to save it in file.

author: Olexandr Shapran 
"""

import sys
import sqlite3
import json
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, \
     QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QPushButton, \
     QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot 
from SQLite_downloader import SQLite_downloader
from multiprocessing.pool import ThreadPool

SQLite_LOCATION = r'F:\Python\ChernLearning\Lesson7_flask_win32\flask_curses_example-master\flask_curses_example-master\db\db.db'
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Simple PyQt5 app'
        
        self.left = 50
        self.top = 50
        self.width = 800
        self.height = 600
        self.initUI()
        
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.createTable()
        self.createBtns()
 
        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        #Add elements to layout
        self.layout.addWidget(self.btn1)
        self.layout.addWidget(self.btn2)
        self.layout.addWidget(self.tableWidget)
        
        self.setLayout(self.layout)  
        # Show widget
        self.show() 


    def createBtns(self):
        '''Create 2 buttons'''
        #create 1st button
        self.btn1 = QPushButton('Fill')
        self.btn1.clicked.connect(self.fillTable)
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.move(10, 10)
        #create 2nd button
        self.btn2 = QPushButton('Export')
        self.btn2.setEnabled(False)
        self.btn2.clicked.connect(self.saveFileDialog)
        self.btn2.resize(self.btn2.sizeHint())
        self.btn2.move(110, 10)


    def createTable(self):
        '''Create table'''
        self.tableWidget = QTableWidget()
        self.tableWidget.move(0, 0) 
 
        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)
 
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def fillTable(self):
        ''' fill table '''

        #create connection
        sqlite_connector = SQLite_downloader(SQLite_LOCATION)
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(sqlite_connector.start )
        #get data downloaded from sqlite
        self.data = async_result.get()
        width = len(self.data[0])
        height = len(self.data) 
         
        #set row and column
        self.tableWidget.setRowCount( height )
        self.tableWidget.setColumnCount(width)
        #fill cells
        for h in range(height ):
            for w in range(width):
                cell = str(self.data[h][w]) if self.data[h][w] else ''
                self.tableWidget.setItem(h, w, QTableWidgetItem( cell ))
        self.btn2.setEnabled(True)        

    def saveFileDialog(self):
        ''' Save file to located place '''
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, ext = QFileDialog.getSaveFileName(self,"File saver","","Text Files (*.txt)", options=options)
        if fileName:            
            ext = '.txt' if ext == "Text Files (*.txt)" else ''  
            self.saveData(fileName + ext)
            print( fileName + ext )
            self.displayMsgBox("File saved!")
            
    def saveData(self, path):
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False)
            
    def displayMsgBox(self, title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()



if __name__ == '__main__':
 
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
