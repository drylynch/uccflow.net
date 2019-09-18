#!/usr/bin/env python3

# redirects user to radio site + logs their button click

import mine
import os

# ----------------------------------------

# simple redirect page
html = """<!DOCTYPE html><html><head><meta http-equiv='refresh' content="0;URL='http://ucc983fm.rocks/'"/><body onload="window.location = 'http://ucc983fm.rocks/'"></body></head></html>"""
user_ip = os.environ.get('REMOTE_ADDR')

# add to listeners (button clickers) file, if they're not there already
mine.add_new_user(user_ip, 'LISTENERS')

# ----------------------------------------

# print page
print('Content-Type: text/html')
print()
print(html)
