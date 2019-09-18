#!/usr/bin/env python3

# deborg

from http.cookies import SimpleCookie

# ----------------------------------------

# gimme debug cookie
cookie = SimpleCookie()
cookie['debug'] = 1
cookie['debug']['expires'] = 31536000

# ----------------------------------------

print('Content-Type: text/html')
print(cookie)
print()
print("""<!DOCTYPE html><html><head><meta http-equiv='refresh' content="0;URL='https://uccflow.net'"/><body onload="window.location = 'https://uccflow.net'"></body></head></html>""")
