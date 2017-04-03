'''
Цель: дописать класс мультипоточного web-скрапера, заготовка которого представлена на
последней странице.
Класс Scraper в качестве аргументов принимает поисковый запрос, страницу с которой
начнется скрапинг, страницу на которой скрапинг закончится (включительно) и лимит для
ограничения одновременно активных потоков.
При вызове метода start() скрапер должен начать процесс скрапинга и по его окончанию
вернуть результат работы.
Задача:
- реализовать запуск метода crawl для каждой страницы сайта в отдельном
потоке
- реализовать способ для ограничения одновременно запущенных потоков
- напишите метод notify, который будет печатать сообщение следующего вида с
помощью модуля logging:
Task done: page_url, где page_url – ссылка на страницу, которую обработал
метод crawl
Пример:
INFO:root:Task done: https://www.olx.ua/chernovtsy/q-iphone/?page=1
- метод notify должен вызываться автоматически при завершении работы
каждого потока (то-есть как только crawl вернул результат работы,
автоматически будет вызван notify)
- метод start должен возвращать результат работы всеx потоков
Условия:
- можно использовать любой способ для запуска метода crawl в потоках
- можно использовать любое количество вспомогательных методов, если есть
необходимость
- нельзя менять уже написанный код в заготовке класса
- код должен быть максимально читаемым и хорошо комментированным
(только там, где это действительно требуется)

'''


import requests
from lxml import html
import logging

import threading
from queue import Queue

logging.basicConfig(level=logging.INFO,
                     format='%(levelname)s:%(name)s:%(message)s',)
 

class Scrapper:
    def __init__(self, query, page_from, page_to, limit=2):
        self.query = query
        self.page_from = page_from
        self.page_to = page_to + 1
        self.limit = limit
        
    def __prepare(self):
        HEADERS = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, lzma, sdch',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.olx.ua',
            'Referer': 'https://www.olx.ua/',
            'Save-Data': 'on',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36 OPR/41.0.2353.69',
        }
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def start(self):
        self.__prepare()

        #queue for threads
        self.q = Queue()
        #semaphore for limitation
        self.semaphore = threading.BoundedSemaphore(value = self.limit)
        threads = []
        result = []

        #create a thread for each page
        for i in range(self.page_from, self.page_to):
            name = 'thread_{}'.format(i)
            link = self.get_link(i)
            t = threading.Thread(target=self.get_crawl_result_for_each_thread,
                                 name=name, args=(link,))
            self.semaphore.acquire()
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

        while not self.q.empty():
            result += self.q.get()
            self.q.task_done()

        return result
    

    def notify(self, url):
        text = "Task done: " + url
        logging.info(text)

    def get_crawl_result_for_each_thread(self, link):
        result = self.crawl(link)
        self.notify(link)
        self.semaphore.release()
        self.q.put(result)
        

    def get_link(self, page):
        link = 'https://www.olx.ua/chernovtsy/q-{0}/?page={1}'.format(self.query, page)
        return link

    def crawl(self, url):
        resp = self.session.get(url)
        if resp.status_code == 200:
            page = resp.text
            root = html.fromstring(page)
            items = []
            offers = root.xpath('//td[@class="offer "]')


        for offer in offers:
            try:
                title = offer.xpath('.//div[@class="space rel"]/h3/a/strong/text()')[0]
                price = offer.xpath('.//td[@class="wwnormal tright td-price"]//p/strong/text()')[0]
                items.append((title, price))
            except:
                pass
        return items

if __name__ == '__main__':
    scrapper = Scrapper('iphone', 1, 3, limit=2)
    results = scrapper.start()
    for result in results:
        offer, price = result
        print(offer, price)

