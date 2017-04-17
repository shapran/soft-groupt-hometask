__author__ = 'Oleksandr Shapran'

'''
Задание 6_2
Набор 1
fu, tofu, snafu
Набор 2
futz, fusillade, functional, discombobulated
Задача: напишите регулярное выражение, которое будет соответствовать всем словам из
первого набора и ни одному из второго.
'''

import re

def main():
    string = """fu, tofu, snafu
            futz, fusillade, functional, discombobulated"""
    result = re.findall(r"\b\w*fu\b", string)
    for x in result:
        print(x)


if __name__ == "__main__":
    main()    
