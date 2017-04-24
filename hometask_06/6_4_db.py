
'''
Class Crawler gether info from site http://forum.overclockers.ua/viewforum.php?f=26
about: post title, author, price, currency, url and first title
==========================
Цель: написать веб-скрапер для одного из разделов сайта forum.overclockers.ua
На сайте overclockers.ua по адресу http://forum.overclockers.ua/viewforum.php?f=26
существует раздел с продажей товаров. Необходимо с помощью асинхронных модулей
asinco и aiohttp написать веб-скрапер, который выполняет следующие действия:
- проходится по заданному, перед стартом скрапера, количеству страниц раздела,
собирая заголовок каждой темы (название темы), ссылку на тему и ник автора
темы
- для всех собранных тем получает содержимое (текст) первого поста
- если возможно, находит в тексте первого сообщение цену товара
- записывает в файл все обработанные топики в JSON формате следующего вида
(одна строка для одного топика):
{‘title’: ‘commodore 64’, ‘url’:
‘http://forum.overclockers.ua/viewtopic.php?f=26&t=99999’,
‘author’: ‘Amigo77’, ‘text’: ‘Selling retro PC –Commodore
64. Buy now price – 100 usd’, ‘price’: ‘100’, ‘currency’:
‘usd’}, где
title – название темы
url – ссылка на тему
author – ник автора темы
text – содержимое первого поста темы
price – цена
currency - валюта
Условия:
- для работы с DOM деревом использовать модуль lxml
- для поиска информации в тексте использовать модуль re
- текст в топике может находиться под спойлером – его тоже необходимо
заполучить.
- в первом посте может и не содержатся информация о цене либо же цена может
быть указана словами, а не цифрами - в таком случае в поле price следует записать
ноль
- если информация о цене в виде цифр все таки содержится в первом посте, эта цена
может указываться в разных валютах (не обязательно в гривнах). Необходимо это
учитывать. Так же, необходимо учитывать разные варианты написания валюты.
- если цена указана без указания валюты – считать это гривнами, с записью в
соответствующее поле
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
import logging
import csv

logging.basicConfig(level=logging.INFO)

class Scrapper:

    def __init__(self, page_from, page_to, limit=2):
        #self.query = query
        self.URL_BASIC = 'http://forum.overclockers.ua'
        self.page_from = page_from
        self.page_to = page_to + 1
        self.limit = limit
        self.results = {}
        self.links = []
        #prepare connection for postgreSQL
        self.__prepare_connection()

    def __prepare_connection(self):
        self.connect = psycopg2.connect(database='Learning', user='postgres', host='localhost', password='Aletok12')
        self.cursor = self.connect.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS scrapper_overclockers(title TEXT, url TEXT, author TEXT, text TEXT, price INT, currency TEXT);")
        self.connect.commit()

    async def __prepare(self):
        HEADERS = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '__cfduid=da3ab835b6bb8404c3d8e7801e08e03891492290665; U=58f28c6917; _ym_uid=1492290672481880173; phpbb3_t78ru_u=1; phpbb3_t78ru_k=; phpbb3_t78ru_sid=35024fac99fd52cb00c696a4b277c6b5; b=b; _ga=GA1.2.1293831531.1492290672; _gid=GA1.2.2115812602.1493056872; _ym_isad=2; _ym_visorc_1648927=w',
            'Host': 'forum.overclockers.ua',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Mobile Safari/537.36',
        }

        conn = aiohttp.TCPConnector(verify_ssl=True)
        self.session = aiohttp.ClientSession(connector=conn, headers=HEADERS)
        return

    def start(self):

        event_loop = asyncio.get_event_loop()
        try:
            event_loop.run_until_complete(self.__prepare())
            ##results = event_loop.run_until_complete(self.__run())
            #first loop get titles
            event_loop.run_until_complete(self.__run())
            #second loop get posts
            event_loop.run_until_complete(self.run_crawl_post())
            
        finally:
            self.session.close()
            event_loop.close()
        #return results

    async def __run(self):
        links = [self.get_link(page) for page in range(self.page_from, self.page_to)]

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

        async with semaphore:

            resp = await self.session.get(url)

            if resp.status == 200:
                page = await resp.text()
                root = html.fromstring(page)

                items = []

                posts = root.xpath('//div[@class="list-inner"]')
                
                #pass header of posts table
                for x in posts[1:]:
                    post_info = {'title': '', 'url':'', 'author': '', 'text': '', 'price': '', 'currency':''}

                    title = x.xpath('./a')[0].xpath('./text()')[0]
                    result = re.search(r'.*\]\s(.*)', title)
                    title = result.group(1)
                    
                    post_info['title'] = title

                    link = x.xpath('./a')[0].xpath('./@href')[0]
                    link_without_session = self.URL_BASIC + link[1:link.find('&sid=')]
                    link = self.URL_BASIC + link[1:]
                    
                    post_info['url'] = link_without_session

                    author = x.xpath('./div[@class="hidden responsive-show"]/strong/a')[0].xpath('./text()')[0]
                    post_info['author'] = author

                    price = ''
                    currency = ''
                    if title:
                        price, currency = self.get_price_if_present(title)
                        post_info['price'] = price
                        post_info['currency'] = currency

                    #pass double link
                    if link_without_session in self.links:
                        print("YET!!! {} - ".format(link_without_session))
                        continue
                    #append to results
                    self.results[link] = post_info
                    self.links.append(link_without_session)
                    ##
                    print('{} -> {} -> {} -> {} -> {} '.format(title, link_without_session, author, price, currency))
                return


    async def run_crawl_post(self):
        #create a task pool for asynchronous execution
        posts_url =  self.results.keys()

        semaphore = asyncio.BoundedSemaphore(self.limit)
        tasks = []

        for link in posts_url:           
            tasks.append(self.crawl_post(link, semaphore))

        for task in asyncio.as_completed(tasks):
            result = await task 
            task.close()
        return

    async def crawl_post(self, link, semaphore):
        #crawl separated post by link 
        async with semaphore:
            request_result = requests.get(link)
            if request_result.status_code == 200:
                page = request_result.text
                logging.debug("[-]Crawler gets info from post {0}".format(link))
                root = html.fromstring(page)
                content = root.xpath('//div[@class="content"]/descendant-or-self::text()')
                text = ''
                for elem in content:
                    elem = elem.strip().replace('\n\r', ' ')
                    text += elem
                #update Text, Price and Currency fields in result
                self.results[link]['text'] = text
                if not self.results[link]['price']:
                    price, currency = self.get_price_if_present(text)
                    
                    self.results[link]['price'] = price
                    self.results[link]['currency'] = currency
                return
            

    def get_link(self, page):
        # generate link
        posts_start = 40 * page #40 == NUMBER_POSTS_PER_PAGE
        link = 'http://forum.overclockers.ua/viewforum.php?f=26&start={0}'.format(posts_start)
        return link

    def get_price_if_present(self, text):
        #extract price and currency from text 
        templates_for_price = {
                r'\s?(\d*)\s?грн': 'uah',
                r'\s?(\d*)\s?uah': 'uah',
                r'[Цц][еі]на:?\s?(\d*)': 'uah'
                }
        for key in templates_for_price.keys():
            result = re.search(key, text)
            if result:
                return (result.group(1), templates_for_price[key])
        return ('', '')

    def save_to_file(self):
        with open('results.txt', 'w', encoding='utf-8') as file:
            for value in self.results.values():
                json.dump(value, file, ensure_ascii=False)
                file.write('\n')


    def save_to_postgre(self):
        try:
            for v in self.results.values():
                query = 'INSERT INTO scrapper_overclockers VALUES (%s, %s, %s, %s, %s, %s);'
                data = (v['title'], v['url'], v['author'], v['text'], int(v['price']) if v['price'] else None, v['currency'])
                ##
                print(query)
                self.cursor.execute(query, data)
                self.connect.commit()          
            
        except Exception as e:
            print(e)
            self.connect.close()

    def display_data_saved(self):
        print('='*20)
        try:
            self.cursor.execute("SELECT * FROM scrapper_overclockers;")
            for row in self.cursor:
                title, url, author, text, price, currency = row
                print('{0}, {1}, {2}, {3}, {4}, {5}'.format(title, url, author, text, price, currency))
        except Exception as e:
            print(e)
            self.connect.close()
            
    def conn_close(self):
        self.connect.close()

       
if __name__ == "__main__":
    start_time = time.time()
    scrapper = Scrapper(1, 3, limit=2)
    scrapper.start()
    #scrapper.save_to_file()
    scrapper.save_to_postgre()
    #scrapper.display_data_saved()
    scrapper.conn_close()
    
    print("--- %s seconds ---" % (time.time() - start_time))
    ## 93 seconds
  
