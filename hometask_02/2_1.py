__author__ = 'Oleksandr Shapran'

'''
Напишите метакласс, который, выполняет следующие функции:
- заменять все приватные атрибуты данных (не методы!) на публичные
- добавлять в наследующий класс статический метод, код которого,
приведен ниже [1]
- добавлять в наследующий класс метод, код которого приведен ниже
[2]
'''

# [1]
def pretty_func():
    print('Some useful message')
# [2]
def do_things(self):
    print(self.var)
    

class PublicMeta(type):

    
    def __new__(cls, name, bases, attrs, **kwargs):
        newattrs = dict()
        #private fields make public
        for k, v in attrs.items():
            if k.startswith('_'+name+'__') and not hasattr(v, "__call__"):
                k = k.replace('_'+name+'__', '')
                newattrs[k] = v
            else:
                newattrs[k] = v
        #add new methods        
        newattrs["do_things"] = do_things
        #add new static method  
        newattrs["pretty_func"] = staticmethod(pretty_func)                 

        return type(name, bases, newattrs)



class A( metaclass=PublicMeta):
    some = 20
    __var = 10
    def __init__(self, x):
        self.x = x
    def __my_private_method(self):
        print('I am still private!!')    
    def method(self):
        pass
    def another(self, y):
        pass


if __name__ == "__main__":
    a = A(9)
    print(a.var)
    a.pretty_func()
    a.do_things()
    a._A__my_private_method()
