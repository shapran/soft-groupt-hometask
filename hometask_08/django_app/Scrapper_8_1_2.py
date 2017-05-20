
'''

'''

__author__ = 'Oleksandr Shapran'

import re
import requests
import json
import time
import asyncio
import psycopg2
import aiohttp
from lxml import html
import html as h
##import logging
import csv
import pymongo
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Color, colors, Alignment
from datetime import datetime
from django.utils import timezone
import django
    
##logging.basicConfig(level=logging.INFO)

class Scrapper:
    def __init__(self, url, limit=2):
        self.url = url
        self.limit = limit
        self.results = []
        self.links = []
        
 
    async def __prepare(self):
        HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, sdch, br',
            'accept-language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
            'cookie': '__cfduid=d411cccf4e5f1772e67bfe5e7fcfcddb51493969528; __gads=ID=d549c4e37012c484:T=1493969538:S=ALNI_MZnB1bQ6C74zWdtY-3y6MBT0MD2rg; _ga=GA1.2.1992315233.1493969540; _gid=GA1.2.1201668070.1493972828',
            'if-modified-since': 'Fri, 05 May 2017 08:25:12 GMT',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Mobile Safari/537.36',
           # ':authority': 'coinmarketcap.com',
           # ':method': 'GET',
           # ':path': '/all/views/all/',
           # ':scheme': 'https',
            }

        conn = aiohttp.TCPConnector(verify_ssl=True)
        self.session = aiohttp.ClientSession(connector=conn, headers=HEADERS)
        return

    def start(self):
        ''' create loop for scrapping'''
        event_loop = asyncio.get_event_loop()
        try:
            event_loop.run_until_complete(self.__prepare())
            event_loop.run_until_complete(self.__run())
            
        finally:
            self.session.close()
            event_loop.close()
        

    async def __run(self):
        ''' Crawl URL '''
        links = [self.url]

        semaphore = asyncio.BoundedSemaphore(self.limit)
        tasks = []
        results = []

        for link in links:
            tasks.append(self.crawl(link, semaphore))

        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
            task.close()

        return results


    async def crawl(self, url, semaphore):
        ''' Crawl URL '''
        async with semaphore:

            resp = await self.session.get(url)

            if resp.status == 200:
                page = await resp.text()
                root = html.fromstring(page)

                currencies = root.xpath('//table[@id="currencies-all"]/tbody/tr')
                for currency in currencies:
                    item = []
                    try:
                        #position
                        position = int(self.get_xpath_value(currency, './td', 0, './text()'))
                        item.append(position)
                        
                        #name
                        name = self.get_xpath_value(currency, './td', 1, './a/text()')
                        item.append(name)
                        #symbol
                        symbol = self.get_xpath_value(currency, './td', 2, './text()')
                        item.append(symbol)
                        #market_cap
                        market_cap = self.get_xpath_value(currency, './td', 3, './text()')
                        item.append(self.get_number(market_cap))
                        #price
                        price = self.get_xpath_value(currency, './td', 4, './a/text()')
                        item.append(self.get_number(price))
                        #supply
                        supply = self.get_xpath_value(currency, './td', 5, './descendant-or-self::text()', -1)
                        item.append(self.get_number(supply))
                        #volume
                        volume = self.get_xpath_value(currency, './td', 6, './a/text()')
                        item.append(self.get_number(volume))
                        #h1
                        h1 = self.get_xpath_value(currency, './td', 7, './text()')
                        item.append(self.get_number(h1))
                        #h24
                        h24 = self.get_xpath_value(currency, './td', 8, './text()')
                        item.append(self.get_number(h24))
                        #d7
                        d7 = self.get_xpath_value(currency, './td', 9, './text()')
                        item.append(self.get_number(d7))
                        #appends to results
                        self.results.append(item)

                       ## print("{} -> {}-> {}-> {}-> {}-> {}-> {}-> {}-> {}-> {}-> {}".format(position, name, symbol,
                         #   #                    market_cap, price, supply,
                        # #                       volume, h1, h24, d7)) 
                    except Exception as e:
                        print(e)
                return

    def get_xpath_value(self, element, selecto1, number1, selector2, number2=0):
        try:
            if number2 != -1:
                return element.xpath(selecto1)[number1].xpath(selector2)[number2].strip()
            else:
                list_inner_text = element.xpath(selecto1)[number1].xpath(selector2)
                return ''.join( map((lambda x: x.strip()), list_inner_text) )
        except Exception as e:
            ##print("{} -> {}-> {}-> {} ".format(selecto1, number1, selector2, number2))
            print(e)
            return ''

 
    def save_to_xlsx(self):
        ''' Save data to formatted xlsx file'''
        #output file name and path
        file = "output.xlsx"

        wb = Workbook()
        # grab the active worksheet
        wsheet = wb.active
        
        #set styles for columns 
        RED = Font(color=colors.RED)
        GREEN = Font(color=colors.GREEN)
        BLUE = Font(color=colors.BLUE)
        BLACK = Font(color=colors.BLACK)    
        RERSENT_FORMAT = '0.00%;[Red]-0.00%'
        DOLLAR_FORMAT = '[$$-409]#,##0;[RED]-[$$-409]#,##0'
        DOLLAR_FORMAT_EXT = '[$$-409]#,##0.00;[RED]-[$$-409]#,##0.00'
        NUMBER_FORMAT = '# ##0'
        DEFAULT_FORMAT = "@"
        
        colunm_style = {
            "B": {'color': BLUE, 'format': DEFAULT_FORMAT, 'width': 25 },
            "D": {'color': BLACK, 'format': DOLLAR_FORMAT, 'width': 25 },
            "E": {'color': BLUE, 'format': DOLLAR_FORMAT_EXT },
            "F": {'color': BLUE, 'format': NUMBER_FORMAT, 'width': 25 },
            "G": {'color': BLUE, 'format': DOLLAR_FORMAT, 'width': 25 },
            "H": {'color': GREEN, 'format': RERSENT_FORMAT },
            "I": {'color': GREEN, 'format': RERSENT_FORMAT },
            "J": {'color': GREEN, 'format': RERSENT_FORMAT }
            }
        for k, v in colunm_style.items():
            col = wsheet.column_dimensions[k]
            col.font = v['color']
            col.number_format = v['format']
            if 'width' in v:
                col.width = v['width']

        #set style for header
        wsheet.row_dimensions[1].font = BLACK
        wsheet.row_dimensions[1].alignment=Alignment(horizontal='center')
        
        #create header
        column_header = ['#', 'Name', 'Symbol', 'Market Cap', 'Price', \
                         'Circulating Supply', 'Volume (24h)', '% 1h', '% 24h', '% 7d']
        for x in range(1, len(column_header)+1):
            wsheet.cell(row = 1, column = x).value = column_header[x-1]
            
     
        #fill table with scrapped data
        for y in range(0, len(self.results)):
            for x in range(0, len(self.results[0])):
                value = self.results[y][x]
                if x >= 3:
                    value = self.get_number(value)
                wsheet.cell(row = y+2, column = x+1).value = value

        # Save the file
        wb.save(file)
        print('File saved!!!')


    
    def get_number(self, string):
        try:
            re_expression = re.compile(r'([-0123456789.]+)')
            result = re_expression.findall(string)
            string_cleared = float(''.join(result))
            return string_cleared
            #return string_cleared/100 if string.find('%')>0 else string_cleared
        except:
            return 0.0


    def sqlite_save(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        ##import django
        django.setup()
        from scrab.models import Coins, Rating
        now = timezone.now()
        
        #fill table with scrapped data
        for y in range(0, len(self.results)):
            try:
                ## how to do
                #coin = self.add_coin(self.results[y][1], self.results[y][2])
                print("Adding {} -> {} ->{}".format(y+1, self.results[y][1], self.results[y][2]))
                coin = Coins.objects.get_or_create(name=self.results[y][1], symbol=self.results[y][2])[0]
                print("--Added or returned {} ".format( coin ))
            except Coin.DoesNotExist:
                coin = None

                #add rating
            if coin:
                r = Rating.objects.get_or_create(rating = self.results[y][0], name_coin = coin,
                                             market_cap = self.results[y][3], price = self.results[y][4],
                                             supply = self.results[y][5], volume = self.results[y][6],
                                             h1 = self.results[y][7], h24 = self.results[y][8],
                                             d7 = self.results[y][9], pub_date = now)[0]
                
                #rate = self.add_rating(self.results[y][0], coin, self.results[y][3],
                 #              self.results[y][4], self.results[y][5], self.results[y][6],
                  #             self.results[y][7], self.results[y][8], self.results[y][9], now )
             

        print('SQLite saved!!!')


    def sqlite_display(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        ##import django
        django.setup()
        from scrab.models import Coins, Rating
        for c in Coins.objects.all():
            print("{} -> {}".format(c.name, c.symbol ))
            for r in Rating.objects.filter(name_coin=c):
                print("{} - {} - {} - {}".format(r.rating, r.name_coin, r.price,  r.pub_date.strftime('%Y-%m-%d %H:%M')))

        


    def add_rating(self, rating, name_coin,  market_cap, price, supply, volume, h1, h24, d7, pub_date=None):
        if pub_date is None:
            pub_date = timezone.now()
            
        r = Rating.objects.get_or_create(rating = rating, name_coin = name_coin,
                                         market_cap = market_cap, price = price,
                                         supply = supply, volume = volume,
                                         h1 = h1, h24 = h24,
                                         d7 = d7, pub_date = pub_date)[0]
        return r


    def add_coin(self, name, symbol):
        c = Coins.objects.get_or_create(name=name, symbol=symbol)[0]
        return c
    
if __name__ == "__main__":
    print("Starting coin's scrapping script...")
    start_time = time.time()
    ##
    print("Start")
    URL = 'https://coinmarketcap.com/all/views/all/'
    scrapper = Scrapper(URL, limit=2)
    scrapper.start()
    scrapper.sqlite_save()
    scrapper.sqlite_display()
    #scrapper.save_to_xlsx()
    print("--- %s seconds ---" % (time.time() - start_time))
 
     

    
    
  
