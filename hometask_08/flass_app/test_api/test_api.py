from requests import put, get
import json


#load data by coin name
print('load data by coin name')
result1 = get('http://localhost:5000/api/?login=1&symbol=BTC' ).json() 
print(result1)
print("="*50)
#load error
print('load error')
result3 = get('http://localhost:5000/api/?login=9' ).json() 
print(result3)
print("="*50)
#load latest data
print('load latest data')
result2 = get('http://localhost:5000/api/?login=1' ).json() 
print(result2)
print("="*50)


