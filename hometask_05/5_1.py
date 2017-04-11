__author__ = 'Oleksandr Shapran'

'''
Напишите программу, которая использует API сайта openweathermap.org для вывода
данных о текущей температуре воздуха.
Программа должна запускаться из командной строки и принимать два возможных
аргумента (ключа):
 --location (-l): для поиска данных по названию города и коду страны (не
обязательно)
 --id (-i): для поиска данных по id города
При запуске программы следует использовать один из аргументов. Если указаны оба
аргумента – приоритет необходимо отдать поиску по id.
'''

import requests
import json
import argparse

class Tempearture_getter():
    '''
    Return temperature from openweathermap. It uses api from its site
    '''
    
         
    def __init__(self):
        self.URL = 'http://api.openweathermap.org/data/2.5/weather'
        self.params = {
            'units': 'metric',
            'appid': 'd2968c098695927f74c48b398eedcb5b'
            }
        
        parser = argparse.ArgumentParser()
        parser.add_argument('-I', "--id", dest="Id", type=int, help="city id for api") 
        parser.add_argument('-l', "--location", nargs='+', dest="location", help="location (city name) for api")
        #get arguments
        args = vars(parser.parse_args())

        #set last url parameter
        if args['Id']:
            self.params['id'] = str(args['Id'])
        elif args['location']:
            self.params['q'] = ','.join( args['location'] )
        else:
            raise Exception('No parameters')
        

    def get_temperature(self):
        #returns the temperature from api response 
        request_result = requests.get(self.URL, params=self.params)
        if request_result.status_code == 200:
            request_text = request_result.text
            result_dict = json.loads(request_text)
            return result_dict['main']['temp'] 
            



if __name__ == "__main__":
    getter = Tempearture_getter()
    print("Current temp: {}° C".format(getter.get_temperature())) #\u00B0
    
 
  
