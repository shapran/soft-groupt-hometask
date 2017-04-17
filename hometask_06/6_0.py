

import socket
import pickle
import json
import random
import re
from lxml import html, etree
#from e3 import -> toString with method convert from xpath to string

     
if __name__ == '__main__':
    with open('test.html') as file,  open('out.html', 'w') as out_file:
        content  = file.read()
        root = html.fromstring(content)
        links = root.xpath('//a')
        
        
        for link in links:
            if not link.xpath('./@href')[0].startswith('http'):
                link.attrib['href'] = 'http://google.com/' + link.xpath('./@href')[0]
                print(link.xpath('./@href'))
 
        print(etree.tostring(root))
        out_file.write(str(etree.tostring(root), 'utf-8'))
            
