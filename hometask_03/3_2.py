__author__ = 'Oleksandr Shapran'
    
'''
 Цель: написать фабрику классов, которая порождает классы-конвертеры с
определенными характеристиками. Характеристиками класса-конвертора является
форматы импорта и экспорта.

Задача:
- Допишите функции csv_load/save и json_load/save. Функции load должны
загружать данные из соответствующего формата в строку. Функции save
должны сохранять данные из строки в соответствующий формат. В качестве
файла функции должны принимать объект, возвращаемый встроенной
функцией open.
- Функции должны быть написанные таким образом, чтобы метод load мог
прочитать файл в строку и затем любой метод write мог записать эту строку уже
в другом формате [см. пример]
- Десериализация строк из/в JSON должна производится в том же порядке, как и
в исходном файле (обычный словарь – неупорядоченная структура, или иначе –
не сохраняет порядок). То есть, порядок строк после сохранения в JSON и
последующей загрузке обратно в строку, должен сохранятся.
- Допишите класс ConverterFabric так, чтобы он содержал реализацию метода
абстрактного класса. Этот метод должен конструировать класс Converter
(должен наследовать класс AbstractConverter), который содержит выбранные
методы load и save.


'''
from abc import ABC, abstractmethod
from collections import OrderedDict 
import csv
import json

def csv_load(file: object) -> str:
    csv_reader = csv.reader(file, delimiter=';')
    result = ''
    for row in csv_reader:
        result += ' '.join(row)
        result += '\n'
    return result.rstrip('\n')

def csv_save(s: str, file: object) -> None:
    rowsList = s.split('\n')
    csv_writer = csv.writer(file)
    for row in rowsList:
       row = row.replace(' ', ';')
       csv_writer.writerow([row]) 

def json_load(file: object) -> str:
    #file_content = json.loads(file.read())
    file_content = json.load(file, object_pairs_hook=OrderedDict)
    result = '\n'.join(file_content['rows'])
    return result
    

def json_save(s: str, file: object) -> None:
    dictionary_to_dump = {}
    dictionary_to_dump['rows'] = s.split('\n')
    file.write(json.dumps(dictionary_to_dump))
    return None

    

class AbsConverterFabric(ABC):
    @abstractmethod
    def create_converter(self, _from: str, _to: str) -> object:
        raise NotImplemented

class AbstractConverter(ABC):
    @abstractmethod
    def load(self, file: object) -> str:
        raise NotImplemented
    @abstractmethod
    def save(self, s: str, file: object) -> object:
        raise NotImplemented

class ConverterFabric(AbsConverterFabric):
    def create_converter(self, _from: str, _to: str) -> object:

        class DynamicClass(AbstractConverter):
            def load(self, file):
                if _from == 'csv':
                    return csv_load(file)
                elif _from == 'json':
                    return json_load(file)
                else:
                    raise Exception('Unknown format FROM converter')

            def save(self, s, file):
                if _to == 'csv':
                    return csv_save(s, file)
                elif _to == 'json':
                    return json_save(s, file)
                else:
                    raise Exception('Unknown format FROM converter')

        return DynamicClass()

    #type meta



if __name__ == "__main__":

    fab = ConverterFabric()
    converter1 = fab.create_converter('csv', 'json')
    converter2 = fab.create_converter('json', 'csv')
    with open('csv.txt', 'r') as file:
        result = converter1.load(file)
        print(result)
    print()
    with open('json.txt', 'w') as file:
        converter1.save(result, file)
    with open('json.txt', 'r') as file:
        result = converter2.load(file)
        print(result)
    with open('csv.txt', 'w', newline='') as file:
        converter2.save(result, file)



