__author__ = 'Oleksandr Shapran'

'''
Выше приведен граф наследования. Реализуйте этот граф в виде классов (с
соответствующим наследованием) и напишите очередность разрешения
методов в классе H.
* Заметка: в классе H в скобках приведена последовательность наследования
для этого класса. Реализация должна использовать ту же
последовательность.

'''

class A():
    pass

class B(A):
    def __init__(self):
        print('__init__ method in B')

class C(A):
    pass

class D(B):
    def some(self):
        print('D: some method')

class E(D, B):
    def do_smth(self):
        print('I am E')

class F(C):
    
    def do_smth(self):
        print('I am F')

class G(C):
    def __init__(self):
        print('__init__ method in G')
    def do_smth(self):
        print('I am G')
    def some(self):
        print('G: some method')    

class H(F, E, G):
    pass


    
if __name__ == "__main__":
    print(H.__mro__)
    h = H()
    h.do_smth()
    h.some()  





     
