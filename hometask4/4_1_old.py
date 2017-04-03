'''
Цель: запустить 10 экземпляров функции worker в разных потоках. Каждому экземпляру
передать один и тот же файл для совместной записи. В каждый момент времени только
один экземпляр функции должен иметь возможность осуществлять запись в файл – иначе
говоря, все потоки должны корректно делить между собой доступ к файлу.

'''

from queue import Queue
import threading
from threading import RLock, Lock, Semaphore
import time
import random

def worker(file: object, *args):
    ''' worker function writes two strings with random pause to shared
    file using synchronization primitive
    :param file: file-object
    :return: '''
    
    q.put(threading.currentThread().name)
 
    with lock:
        file.write(threading.currentThread().name + ': ' + 'started.\n')        
        time.sleep(random.random() * 5)
        file.write(threading.currentThread().name + ': ' + 'done.\n')

    return None
 
    

if __name__ == '__main__':
    file = open('test.txt', 'a')
 

    q = Queue()
    threads = []
    lock = RLock()

    for i in range(1, 11):
        name = 'thread_{}'.format(i)
        t = threading.Thread(target=worker, name=name, args=(file, q, lock))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()        

    while not q.empty():
        q.get()
        q.task_done()
    else:
        file.close()


