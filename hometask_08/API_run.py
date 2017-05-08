from flask import Flask, request
from flask_restful import Resource, Api, abort

import sqlite3
import json

class SQLite_connection:

    def __init__(self):
        #prepare connection to SQLite
        self.__prepare_sqlite_connection()

    def __exit__(self, *args):
        '''
        close all conncetions        
        '''    
        #close sqllite connection        
        self.sqllite_cur.close()
        self.sqllite_con.close()

    def __prepare_sqlite_connection(self):
        self.sqllite_con = sqlite3.connect(r'.\db\db.db')
        self.sqllite_cur = self.sqllite_con.cursor()
          
    def get_data_all(self):        
        ''' select whole table from currencies '''
        try:
            self.sqllite_cur.execute("SELECT * FROM currencies;")
            return  self.sqllite_cur.fetchall()     
        except Exception as e:
            print(e)
            self.sqllite_cur.close()
            self.sqllite_con.close()

    def get_currency_by_name(self, currency):        
        ''' select only 1 row from currencies table by name or symbol  '''
        try:
            self.sqllite_cur.execute("SELECT * FROM 'currencies' where name='" + currency + "' or symbol='" + currency + "' LIMIT 0,1")
            return  self.sqllite_cur.fetchall()     
        except Exception as e:
            print(e)
            self.sqllite_cur.close()
            self.sqllite_con.close()
    def close_sqlite(self):
        self.sqllite_cur.close()
        self.sqllite_con.close()




app = Flask(__name__)
api = Api(app)


class MainAPIClass(Resource):
    def __init__(self):
        self.sql = SQLite_connection( )
        
    def get(self):
        '''
        Returns data from currency table.
        Depending on parameters returns all data or for a specific currency
        '''
        #abort if key is not passed 
        if not request.form['key']:
            abort(404, message="Key is not present. Denied!")
        if request.form['key'] != '1':
            abort(404, message="Key is not registered. Denied!")

        method = request.form['method']
            
        if method == 'get_all':
            return self.sql.get_data_all() 
        elif method == 'get_by_name':
            return self.sql.get_currency_by_name( request.form['name'] )

        

api.add_resource(MainAPIClass, '/') 

if __name__ == '__main__':
    app.run(port=9999, debug=True)
    
