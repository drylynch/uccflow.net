# html template for different pages

import mine

_index_html = """<h1><em>keep flowin.</em></h1>
<p><a href='/listen' target='_blank' class='listenbtn'>click to listen LIVE</a></p>
<p>use the box below to send us a message.<p>
<p>requests, comments, notions.<br>all are welcome.</p>
<form action='/' method='post'><table id='msgbox'>
<tr><th>Name<br>(optional)</th><td><input type='text' name='name' id='name' maxlength='20'></td></tr>
<tr><th>Message</th><td><textarea cols='50' rows='10' name='message' id='message' maxlength='500' required></textarea></td></tr>
<tr><td colspan='2'><input type='submit' value='Send feedback'></td></tr>
</table></form>"""

_about_html = """<p>flow is ucc's flagship morning breakfast show</p>
<p>we play (good) music, feature new music from local artists, and talk about nothing.</p>
<br>
<p><b>when?</b><br>8am - 11am, friday mornings.</p>
<p><b>where?</b><br>on 98.3fm, or online at <a href='http://ucc983fm.rocks/' target='_blank'>ucc983fm.rocks</a></p>
<br>
<p>listen to previous shows, musician interviews, and more on our <a href='https://www.mixcloud.com/Flow983/' target='_blank'><img src='/img/mix.png' alt='mixcloud' title='mixcloud'></a>"""

_contact_html = """<h1>contact?</h1>
<div id='contact'>
<table>
<tr><th colspan='2'>the brand.</th></tr>
<tr><th>twitter</th><td><a href='https://twitter.com/flow983' target='_blank'>@flow983</a></td></tr>
<tr><th>facebook</th><td><a href='https://facebook.com/flow983' target='_blank'>@flow983</a></td></tr>
<tr><th>instagram</th><td><a href='https://www.instagram.com/flow98.3/' target='_blank'>@flow98.3</a></td></tr>
</table>
<table>
<tr><th colspan='2'>the people.</th></tr>
<tr><th>liz</th><td><a href='https://twitter.com/liz_hession' target='_blank'>@liz_hession</a></td></tr>
<tr><th>tim</th><td><a href='https://twitter.com/tim_o_mahony' target='_blank'>@tim_o_mahony</a></td></tr>
<tr><th>dave</th><td><a href='https://twitter.com/drylynch' target='_blank'>@drylynch</a></td></tr>
</table>
<p><em>site enquiries: <a href='mailto:david.rl@gmx.com'>david.rl@gmx.com</a></em></p>
</div>"""

error_html = """<h1>oh snap.</h1>
<p>something went wrong on our end, check back in a while.</p>
<p>thanks for listening either way, pal</p>"""


class Skeleton:
    """ webpage skeleton with presets """

    def __init__(self):
        self.main = "nothing here... (//_-)"
        self._banner_feedback = ""
        self._liveheader = ""

    def index(self):
        # main page
        self.main = _index_html

    def contact(self):
        # contact page
        self.main = _contact_html

    def offline(self):
        # when not broadcasting
        self.main = "<h1>we're offline.</h1>\n"
        self.main += _about_html

    def about(self):
        # about the cru + show
        self.main = "<h1>about flow...</h1>\n"
        self.main += _about_html

    def stats(self):
        # get that feedback
        self.main = mine.get_feedback()

    def error(self):
        # shit
        self.main = error_html
        mine.add_new_feedback('UH OH SHIT IS FUCKED, PANIC TIME', 'PANIC ROBOT', '69.69.69.666')

    def add_feedback_banner(self):
        # show little banner of confirmation for sent feedback
        self._banner_feedback = "<div id='banner-message'>message sent!</div>\n"

    def printy(self):
        # print it
        if mine.show_is_live():  # add stuff to the header when show is live
            self._liveheader = "<a href='https://www.last.fm/user/uccfm' target='_blank'><img src='/img/lastfm.png' alt='our playlist' title='our playlist'></a>\n"  # last.fm link

        print('Content-Type: text/html')
        print()
        print("""<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>flow | ucc 98.3fm</title>
<link rel='icon' href='/favicon.ico'>
<link rel='stylesheet' type='text/css' href='/style.css'>
<meta property='og:title' content='flow.' />
<meta property='og:type' content='music.radio_station' />
<meta property='og:url' content='https://uccflow.net' />
<meta property='og:image' content='https://uccflow.net/img/previmg.jpg' />
<meta property='og:image:type' content='image/jpeg' />
<meta property='og:description' content="ucc 98.3fm's flagship music breakfast show" />
</head>
<body>

<header>
<p id='home'><a href='/'>flow | ucc 98.3fm</a></p>
<p id='links'>
<a href='https://twitter.com/flow983' target='_blank'><img src='/img/twitter.png' alt='twitter' title='twitter'></a>
<a href='https://www.facebook.com/flow983/' target='_blank'><img src='/img/fb.png' alt='facebook' title='facebook'></a>
<a href='https://www.instagram.com/flow98.3/' target='_blank'><img src='/img/insta.png' alt='instagram' title='instagram'></a>
{2}</p>
</header>

<main>
{1}{0}
</main>

<footer>
<a href='/about'>about</a> | <a href='/contact'>contact</a>
</footer>

</body>
</html>""".format(self.main, self._banner_feedback, self._liveheader))
