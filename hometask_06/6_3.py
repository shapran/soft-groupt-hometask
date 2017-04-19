
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
from lxml import html
import logging

logging.basicConfig(level=logging.INFO)

class Crawler():
    def __init__(self, page_to=0, limit=2):
        self.URL_BASIC = 'http://forum.overclockers.ua'
        self.page_to = page_to + 1
        self.limit = limit
        self.results = {}
        
    def start(self):
        '''
        Collects information about links to posts in usual loop with 1 second pause.
        Then it starts asynchronous requests to collect information about individual posts.
        The result is saved in a file as json-objects    
        '''
        #main block - geather info from lists of post
        for i in range(self.page_to):
            link = self.get_link(i)
            request_result = requests.get(link)
            if request_result.status_code == 200:
                page = request_result.text
                logging.debug("[-]Crawler get info from post list {0}".format(link))
                root = html.fromstring(page)
                posts = root.xpath('//div[@class="list-inner"]')
                #pass header of posts table
                for x in posts[1:]:
                    post_info = {'title': '', 'url':'', 'author': '', 'text': '', 'price': '', 'currency':''}
                    title = x.xpath('./a/text()')
                    if len(title) > 0: 
                        title = title[0]
                        #title = title[title.find(']')+2:]
                        title = re.search(r'.*\]\s(.*)', title).group(1)
                        post_info['title'] = title
                    link = x.xpath('./a/@href')
                    if len(link) > 0:
                        link = link[0]
                        link = self.URL_BASIC + link[1:link.find('&sid=')]
                        post_info['url'] = link
                    author = x.xpath('./div[@class="hidden responsive-show"]/strong/a/text()')
                    if len(author) > 0:
                        author = author[0]
                        post_info['author'] = author
                    price = ''
                    currency = ''
                    if title:
                        price, currency = self.get_price_if_present(title)
                        post_info['price'] = price
                        post_info['currency'] = currency

                    #append to results
                    self.results[link] = post_info
                    
                    print('{} -> {} -> {} -> {} -> {}'.format(title, link, author, price, currency))
            time.sleep(1)

        #create a loop for asynchronous execution
        event_loop = asyncio.get_event_loop()
        try:
            event_loop.run_until_complete( self.run_crawl_post() )
        finally:
            event_loop.close()
        self.save_to_file()
        print('Task done!!!')     

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
                    ##
                    print('price {0}, currency {1}'.format(price, currency))
                    self.results[link]['price'] = price
                    self.results[link]['currency'] = currency
                return
            

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


    def get_link(self, page):
        # generate link
        posts_start = 40 * page #40 == NUMBER_POSTS_PER_PAGE
        link = 'http://forum.overclockers.ua/viewforum.php?f=26&start={0}'.format(posts_start)
        return link


    
if __name__ == "__main__":
    crawler =   Crawler()
    crawler.start()
 
  
