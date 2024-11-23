#!/usr/bin/env python
     
import base64
import os
import re     
secret = base64.b64encode(os.urandom(50)).decode('ascii')

file = open('.env', 'r') 
content = ''
try:
    content = file.read()
finally:
    file.close()

file = open('.env', 'w')
try:
    content = re.sub(r'^COOKIE_SECRET=', f'COOKIE_SECRET={secret}', content, flags=re.M)
    file.write(content) 
finally:
    file.close()