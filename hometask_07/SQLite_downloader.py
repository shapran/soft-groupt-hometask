'''
Class implements
1. SQLite connection
2. read data
3. save file to txt file
'''

import sqlite3
import json
#from PyQt5.QtCore import QThread

class SQLite_downloader():
    def __init__(self, data_location):
        super().__init__()
        self.data_location = data_location
        self.data = []
        

    def start(self):
        '''Select data from database'''    
        print('='*20)       
        self.sqllite_con = sqlite3.connect(self.data_location)
        self.sqllite_cur = self.sqllite_con.cursor()
        try:
            self.sqllite_cur.execute("SELECT title, url, author, price, currency FROM 'scrapper_overclockers' ;") ##limit 0, 10
            for row in self.sqllite_cur:
                self.data.append(row)
                title, url, author, price, currency = row                
                ##print('{0}, {1}, {2}, {3}, {4}'.format(title, url, author, price, currency))
            print('Data dowloaded from SQLite')
            return self.data
        except Exception as e:
            print(e)
            self.sqllite_cur.close()
            self.sqllite_con.close()
    
    def getCell(self, h, w):
        return self.data[h][w]
    
    def dataWidth(self):
        return len(self.data[0])

    def dataHeight(self):
        return len(self.data)

    def printData(self):
        for x in self.data:
            print(x[0])


            
    def __exit__(self, *args):
        '''
        close all conncetions        
        '''     
        #close sqllite connection        
        self.sqllite_cur.close()
        self.sqllite_con.close()

if __name__ == '__main__':
    data = SQLite_downloader(r'F:\Python\ChernLearning\Lesson7_flask_win32\flask_curses_example-master\flask_curses_example-master\db\db.db')

    from multiprocessing.pool import ThreadPool
    pool = ThreadPool(processes=1)

    async_result = pool.apply_async(data.start )  

    val = async_result.get()   
    print(val)
 
