__author__ = 'Oleksandr Shapran'
    
'''
 Задача:
- Допишите функцию html_print (можно использовать как стандартные
библиотеки, так и собственную реализацию).
- Напишите декоратор writer, который первым аргументом принимает строку из
символов. Символы указывают на то, какие обрамляющие функции будут
применены к строке. Если в аргументе содержатся символы, для которых нет
обрамляющих функций – декоратор просто пропускает такой символ, переходя
к следующему. 

'''

import html

def html_p(s: str) -> str:
    new_s = '<p>{}<p>'.format(s)
    return new_s

def html_b(s: str) -> str:
    new_s = '<b>{}<b>'.format(s)
    return new_s

def html_i(s: str) -> str:
    new_s = '<i>{}<i>'.format(s)
    return new_s

def html_u(s: str) -> str:
    new_s = '<u>{}<u>'.format(s)
    return new_s

def writer(params):
    def decorator(func):
        def wrapper(str):
            res = str
            #call appropriate func if decorator parameters == p, b or i
            for x in params:
                if x == 'p':
                    res = html_p(res)
                elif x == 'b':
                    res = html_b(res)
                elif x == 'i':
                    res = html_i(res)
                 
            return func(res)
        return wrapper
    return decorator
            

@writer('bpx')
#@writer('')
def html_printer(s: str) -> str:
    return html.escape(s)
    

if __name__ == "__main__":
    print(html_printer("I'll give you +++ cash for this -> stuff."))

