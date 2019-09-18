#!/usr/bin/env python3

# landing page

from cgi import FieldStorage
from webpage import Skeleton
import mine
import os

# ----------------------------------------

form_data = FieldStorage()
html = Skeleton()

user_ip = os.environ.get('REMOTE_ADDR')  # not spoofable afaik
feedback_name = ''
feedback_msg = ''


if mine.show_is_live():
    html.index()  # welcome
    if form_data:
        # something sent? reel it in
        feedback_name = mine.clean_input(form_data.getfirst('name', ''), 20)
        feedback_msg = mine.clean_input(form_data.getfirst('message', ''), 500)
    try:  # to read files
        mine.add_new_user(user_ip, 'PAGEHITS')  # add user to page hits file, if they're not there already
        if feedback_msg:
            # if they sent feedback, add it
            mine.add_new_feedback(feedback_msg, feedback_name, user_ip)
            html.add_feedback_banner()  # adds a little confirmation banner
    except IOError:
        # oops
        html.error()

else:  # show isn't broadcasting
    html.offline()

# ----------------------------------------

# print page
html.printy()
