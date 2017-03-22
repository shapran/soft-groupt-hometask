__author__ = 'Oleksandr Shapran'

'''
Используя модуль os, напишите класс, который частично имитирует
встроенную функцию open, а именно:
- имеет два обязательных аргумента и один аргумент по умолчанию:
- filename (полный путь к файлу)
- mode (режим работы с файлом)
- encoding (кодировка файла, по умолчанию должна быть юникод)
- поддерживает как прямое обращение к классу, так и менеджер
контекста [1,2]
- поддерживает три режима (‘r’, ‘w’, ‘a’) и их комбинации (‘rw’, ‘wa’, и
т.д)
- имеет следующие методы:
o read(n) – читает n символов из файла, либо весь файл, если n не
указан
o readLine() – читает одну строку из файла
o write(s) – записывает в файл строку s
o writeLine(s) – записывает в файл с новой строки строку s
o close() – закрывает файл
Условия:
- запрещается использовать для работы с файлом как встроенную
функцию open, так и любые другие модули, кроме os
- допускается любое (разумное!) количество вспомогательных классов,
декораторов или функций для реализации необходимого
функционала, но все взаимодействие с пользователем должно
осуществляться так же, как и при использовании встроенной функции
open
- после завершения взаимодействия с файлом, он должен быть
корректно закрыт (вручную методом close или автоматически, в случае
менеджера контекста)

'''

import os
class AOpen:
    def __init__(self, path, mode,  encoding='utf-8'):
        descriptorModeStatus = {'r' : os.O_RDONLY,
                      'w': os.O_WRONLY|os.O_CREAT,
                      'a': os.O_APPEND|os.O_CREAT,
                      'rw': os.O_RDWR|os.O_CREAT,
                      'ra' : os.O_RDONLY|os.O_APPEND|os.O_CREAT,
                      'wa': os.O_APPEND|os.O_CREAT}
        
        #create decriptor for the file
        fileDescriptor = os.open(path, descriptorModeStatus[mode])
        
        fileNodeStatus = {'r' : 'r',
                      'w': 'w',
                      'a': 'a',
                      'rw': 'r+',
                      'ra' : 'a+',
                      'wa': 'w+' }
        #open file
        self.file = os.fdopen(fileDescriptor, fileNodeStatus[mode] )         

    def __enter__(self):
        return self

    def __exit__(self, exc_ty, exc_val, exc_tb):
        self.close()

    def read(self, number=''):
        if number == '':
            return self.file.read()
        return self.file.read(number)

    def readLine(self):
        return self.file.readline()
        
    def seek(self, number):
        return self.file.seek(number)
        
    def write(self, text):
        return self.file.write(text)    

    def writeLine(self, line):
        return self.file.write('\n' + line)

    def close(self):
        self.file.close()

    

 

     
if __name__ == "__main__":
    with AOpen( 'F:\\temp\\fooClass.txt', 'rw' ) as file:

        file.write('Method Write 1 \nMethod Write 2 \n')
        file.writeLine('Method write line')
        file.seek(0)
        print(file.read())
        x = file.readLine()
        while x:
            print(x, end='')
            x = file.readLine() 


    f =  AOpen( 'F:\\temp\\foo.txt', 'rw' ) 
    f.write('Method Write 1 \nMethod Write 2 \n')
    f.writeLine('Method write line')
    f.seek(0)
    print(f.read())
    x = f.readLine()
    while x:
        print(x, end='')
        x = f.readLine() 
   
