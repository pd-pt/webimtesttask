#!/usr/bin/env python
     
import base64
import os
     
secret = base64.b64encode(os.urandom(50)).decode('ascii')

file = open('.env', 'a') 
file.write(secret) 
file.close() 