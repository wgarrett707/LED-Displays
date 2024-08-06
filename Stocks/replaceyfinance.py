#!/usr/bin/env python
path = "/home/pi/.local/lib/python2.7/site-packages/yfinance/utils.py"

f = open(path, "r+")
content = f.readlines()
f.write(content.replace(b'maxsplit=1', b'1'))
content = [w.replace('maxsplit=1', '1') for w in content]
