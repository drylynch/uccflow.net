# functions for other scripts

import datetime
import os

today = str(datetime.date.today())  # 'YYYY-MM-DD'
clock = datetime.datetime.today().strftime('%H:%M%p').lower()  # HH:MM(am|pm)

LISTENERFILE = '/home/users/drylynch/uccflow/listeners/' + today + '.txt'  # people who click the button
PAGEHITSFILE = '/home/users/drylynch/uccflow/pagehits/' + today + '.txt'  # people who visit the page
FEEDBACKFILE = '/home/users/drylynch/uccflow/feedback/' + today  # messages people sent
DEFAULT_USERNAME = 'Anonymous'


# ----------------------------------------


def show_is_live():
    """ if it's between 8 and 11 am on a friday, we broadcasting
        debug setting - always true if cookie with debug = 1 is given """
    if _debug_mode():
        return True

    now = datetime.datetime.now()
    day = now.strftime('%A')
    hour = now.strftime('%H')

    return day == 'Friday' and 8 <= int(hour) <= 11


def add_new_user(user_ip, filecode):
    """ adds user to specified file, if not in there already """
    file = _get_path(filecode)  # get path of desired file
    _create_if_nonexist(file)  # create file if it doesn't exist yet

    # check for ip in file
    with open(file, 'r') as f:
        for line in f:
            if user_ip == line.strip():
                return  # found

    with open(file, 'a') as f:  # add ip to file
        f.write(user_ip + '\n')


def add_new_feedback(message, name, ip):
    """ adds feedback messages to file """
    import shelve
    import time

    if not name:  # give default name if user doesn't enter one
        name = DEFAULT_USERNAME
    unixtime = str(int(time.time()))  # future proofing - allow ajax to get new posts. currently not used
    head_bg, head_text, body_bg, body_text = css_colours(ip)  # generate colours based on ip

    # shove the whole post in a dictionary
    post = {'name': name,
            'ip': ip,
            'message': message,
            'clocktime': clock,
            'unixtime': unixtime,
            'head_bg': head_bg,
            'head_text': head_text,
            'body_bg': body_bg,
            'body_text': body_text}

    # add the new post to the feedback file
    with shelve.open(FEEDBACKFILE, writeback=True) as file:
        if 'feedback' not in file:  # create an empty postlist if there isn't one already
            file['feedback'] = []
        postlist = file['feedback']  # take out the list of post dicts
        postlist.append(post)  # append the new post
        file['feedback'] = postlist  # plop it back inside the file


def get_feedback():
    """ returns a blob of html of all messages, headed by count of page hit, button click and message """
    import shelve

    msgcount = 0
    msgblob = ""

    # create each file if they don't exist for today yet
    _create_if_nonexist(LISTENERFILE)
    _create_if_nonexist(PAGEHITSFILE)

    # count number of listeners and page hits
    listencount = _count_lines(LISTENERFILE)
    pagehitcount = _count_lines(PAGEHITSFILE)

    # go through all messages and add them to a nice big html blob
    # file is a single key dict containing a list (postlist) of dicts (p)
    with shelve.open(FEEDBACKFILE) as file:
        if 'feedback' in file:
            postlist = file['feedback']  # pull out list of posts
            for p in postlist:  # for each post dict p
                msgcount += 1
                msgblob += "<table class='post' cellspacing='0'>\n"
                msgblob += "<thead title='{0}' style='background:{1};color:{2};'><tr><td>{3} @ {4}</td></tr></thead>\n".format(p['ip'], p['head_bg'], p['head_text'], p['name'], p['clocktime'])
                msgblob += "<tbody style='background:{0};color:{1};'><tr><td>{2}</td></tr></tbody>\n".format(p['body_bg'], p['body_text'], p['message'])
                msgblob += "</table>"

    # stitch it up and poop it out
    html = "<p>{0} pagehits, {1} listeners, {2} messages</p>\n".format(pagehitcount, listencount, msgcount)
    html += msgblob

    return html


def clean_input(string, maxlength):
    """ goodbye xss """
    from html import escape

    string = string[:maxlength]  # chop off anything above max length
    string = string.strip()  # strip trailing spaces and newlines
    string = escape(string)  # escape whatever's left
    string = string.replace('\r\n', '\n')  # windows newline to unix
    string = string.replace('\r', '\n')  # mac newline to unix
    string = _trim_replace(string, '\n', '<br>')  # remove excess newlines
    string = string.encode('ascii', 'xmlcharrefreplace').decode('utf-8')  # replace danger boys with safe boys

    return string


def css_colours(seed_ip):
    """ returns nice css colours (bg & text for both header & body) for each user's posts """
    import colorsys
    import random

    random.seed(seed_ip)  # use ip here, but can be anything user specific

    # rgb1/hsv1 = header
    # rgb2/hsv2 = body

    # generate an initial colour with random hsv percentages, 0.0 -> 1.0
    h1, s1, v1 = random.random(), random.random(), random.random()  # rgb1 to hsv1

    # cap lightness for header at 85%
    if v1 > .85:  # the body will always be lighter by 15%, so this guarantees consistency
        v1 = .85

    # convert hsv1 into both rgbs
    r1, g1, b1 = colorsys.hsv_to_rgb(h1, s1, v1)
    r2, g2, b2 = colorsys.hsv_to_rgb(h1, s1, v1 + .15)  # rgb2 is just a slighty lighter rgb1

    # convert rgb percentages into standard ints, 0 -> 255
    r1, g1, b1 = round(r1 * 255), round(g1 * 255), round(b1 * 255)
    r2, g2, b2 = round(r2 * 255), round(g2 * 255), round(b2 * 255)

    # convert rgb1 and rgb2 into usable css hex colours
    head_bg = "#%02x%02x%02x" % (r1, g1, b1)
    body_bg = "#%02x%02x%02x" % (r2, g2, b2)

    # determine whether to use black or white text for best contrast
    head_text = _contrasting_text_colour(r1, g1, b2)
    body_text = _contrasting_text_colour(r2, g2, b2)

    return head_bg, head_text, body_bg, body_text


# ---------------------------------------- private functions ----------------------------------------


def _debug_mode():
    """ returns true if debug cookie sent (debug = 1) """
    return os.environ.get('HTTP_COOKIE') == 'debug=1'


def _create_if_nonexist(filename):
    """ creates a file called filename if it doesn't exist """
    if not os.path.exists(filename):
        open(filename, 'w').close()  # touch file


def _get_path(filecode):
    """ return actual path of filecode """
    if filecode == 'LISTENERS':
        return LISTENERFILE
    elif filecode == 'PAGEHITS':
        return PAGEHITSFILE
    else:  # uh oh
        raise ValueError('invalid filecode: %s' % str(filecode))


def _count_lines(path):
    """ return number of lines in given file """
    count = 0
    with open(path, 'r') as f:
        for _ in f:
            count += 1
    return count


def _contrasting_text_colour(r, g, b):
    """ determines whether black or white text would look best on a given rgb background """
    # weird way of finding contrast, but it just works(tm)
    # taken from https://stackoverflow.com/questions/3942878/
    if (r * 0.299) + (g * 0.587) + (b * 0.114) > 149:  # originally > 186, lower => black text more often
        return '#000'  # bright colour, so black text
    else:
        return '#fff'  # dark colour, so white text


def _trim_replace(string, old, new=None):
    """ replaces old char with new, per instance max of 2
            eg.
        'aaaa_ccc_aaa_aa_a', old='a', new='b'
            becomes
        'bb_ccc_bb_bb_b'
    """
    import re

    if not len(old) == 1:  # sux but that's life
        raise ValueError('old can only be one character long')

    # if new is undefined, just trim excess old chars
    if not new:
        new = old

    found = []

    # use regex to find all instances of old, plus surrounding whitespace (\s*)
    for match in re.finditer(r'\s*' + old + r'+\s*', string):
        # adds (start, end) tuple of indeces to found list
        # start is inclusive, end is exclusive
        found.append(match.span())

    # replace each set of matching old chars, working backwards to not upset lower indeces with potential size changes
    for tup in found[::-1]:
        # if the matched string is more than 2 chars, the replacement will be capped out at double the new input
        if (tup[1] - tup[0]) >= 2:
            replace = new * 2
        else:
            replace = new

        # everything up to (and excluding) the first index in the old string is added to the new string
        # then the replacement 'overwrites' everything between the indeces
        # and the rest of the old string is stuck on the end
        string = string[:tup[0]] + replace + string[tup[1]:]

    return string


# ---------------------------------------- DEBUG  ----------------------------------------


def __remove_listeners():
    # remove all of today's listeners
    open(PAGEHITSFILE, 'w').close()


def __remove_feedback():
    # remove all of today's feedback
    open(FEEDBACKFILE, 'w').close()


def __remove_listener_me():
    # just remove my ip
    bad_ip = os.environ.get('REMOTE_ADDR')
    with open(LISTENERFILE, 'r') as f:
        new = f.read()  # store whole file in variable
        new = new.replace(bad_ip, '')  # remove the ip
        new = new.replace('\n\n', '\n')  # remove blank lines left behind
    with open(LISTENERFILE, 'w') as f:
        f.write(new)  # pop var contents into clean file


# --------------------------------------------------------------------------------

if __name__ == '__main__':
    print('Content-Type: text/html')
    print()
    print("you really shouldn't be here, bucko...<br>but tell me how you found this and i'll high five you or something<br>david.rl@gmx.com<br>:^)")
