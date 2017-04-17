__author__ = 'Oleksandr Shapran'

'''
Задание 6_1
Набор 1
afoot, catfoot, dogfoot, fanfoot, foody, foolery, foolish, fooster, footage, foothot, footle,
footpad, footway, hotfoot, jawfoot, mafoo, nonfood, padfoot, prefool, sfoot, unfool
Набор 2
Atlas, Aymoro, Iberic, Mahran, Ormazd, Silipan, altered, chandoo, crenel , crooked, fardo,
folksy, forest, hebamic, idgah, manlike, marly, palazzo, sixfold, tarrock, unfold
Задача: напишите регулярное выражение, которое будет соответствовать всем словам из
первого набора и ни одному из второго.
'''

import re

def main():
    string = """afoot, catfoot, dogfoot, fanfoot, foody, foolery, foolish, fooster, footage, foothot, footle,
        footpad, footway, hotfoot, jawfoot, mafoo, nonfood, padfoot, prefool, sfoot, unfool 
        Atlas, Aymoro, Iberic, Mahran, Ormazd, Silipan, altered, chandoo, crenel , crooked, fardo,
        folksy, forest, hebamic, idgah, manlike, marly, palazzo, sixfold, tarrock, unfold"""
    result = re.findall(r"\b\w*foo\w*\b", string)
    for x in result:
        print(x)


if __name__ == "__main__":
    main()   
 
  
