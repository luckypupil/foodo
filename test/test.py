#!/usr/bin/python
import requests

r = requests.get('http://www.google.com')

with open('test.html','wb') as html:
    html.write(r.text)
    
