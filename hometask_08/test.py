from requests import put, get
import json



## select currency by name of symbol
data_currency = {
    'method': 'get_by_name',
    'name': 'BTC',
    'key': 1    
    }
result2 = get('http://localhost:9999/', data=data_currency).json() 
print(result2 )
print('*'*50)

##select all data
data_all = {
    'method': 'get_all',
    'key': 1
    }
result1 = get('http://localhost:9999/', data=data_all).json() 
print(result1)


