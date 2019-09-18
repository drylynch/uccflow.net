#!/usr/bin/env python3

# outputs a nice error page to a user who stumbles on a http error

from webpage import Skeleton
import os

# ----------------------------------------

html = Skeleton()

code = os.environ.get('REDIRECT_STATUS')

# error codes -> relevant html
error_html = {"404": "<h1>you have become lost in the ocean.</h1>\n"
                     "<img src='/img/ocean.jpg'>\n"
                     "<p><a href='/'>but the tides gently sweeps you home.</a></p>",
              "403": "<h1>the ocean pushes you back.</h1>\n"
                     "<img src='/img/ocean.jpg'>\n"
                     "<p>the tide whispers in your ear... <em>'get outta here you lil scamp'</em></p>\n"
                     "<p><a href='/'>you should probably swim home.</a></p>",
              "200": "<h1>the ocean is confused, but delighted.</h1>\n"
                     "<img src='/img/ocean.jpg'>\n"
                     "<p>it beckons you to email <a href='mailto:david.rl@gmx.com'>david.rl@gmx.com</a> to explain your feat of discovery.</p>\n"
                     "<p><em>a small pearl has been added to your inventory.</em></p>"}

if code:
    if code in error_html:  # show em the payoff
        html.main = error_html[code]
    else:  # code given but not in dictionary
        html.main = "<h1>the ocean has become too violent to enter.</h1>\n" \
                     "<img src='/img/ocean.jpg'>\n" \
                     "<p>the flow needs time to recover.</p>\n" \
                     "<p><em>you should come back later.</em></p>"

# ----------------------------------------

# print page
html.printy()
print("<!--", code, "-->")
