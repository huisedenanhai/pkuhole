from urllib.request import urlopen
import termcolor
import base64
import json

SHOW_DEBUG = False
SHOW_INLINE_IMAGE = False
url = 'http://pkuhelper.pku.edu.cn/services/pkuhole'

def set_SHOW_DEBUG(show_debug):
    global SHOW_DEBUG
    SHOW_DEBUG = show_debug

def set_SHOW_INLINE_IMAGE(show_img):
    global SHOW_INLINE_IMAGE
    SHOW_INLINE_IMAGE = show_img

def add_params(url, params):
    newurl = url + '?'
    for k, v in params.items():
        newurl += k + '=' + v + '&'
    newurl = newurl[:-1]
    return newurl

def get_responds(params):
    global SHOW_DEBUG
    list_url = add_params(url + '/api.php', params)
    if SHOW_DEBUG:
        print(list_url)
    try:
        js = urlopen(list_url)
        js = json.load(js)
    except:
        termcolor.cprint('Failed to get responds',color='red')
        return None
    return js

def get_image(filename):
    '''
    fetch the content of the required image

    :param filename: image filename, usually stored in the 'url' field
    :return: the content of the required image
    '''
    img_url = url + '/images/' + filename
    if SHOW_DEBUG:
        print(img_url)
    try:
        img = urlopen(img_url)
        img = img.read()
    except:
        termcolor.cprint('Failed to load image',color='red')
        return None
    return img

def show_op_data(op_data):
    '''
    show the msg of the original poster

    :param op_data: the 'data' feild of the original poster's decoded json
    :return: no return
    '''
    print(op_data['pid'])
    print(op_data['text'])
    if SHOW_INLINE_IMAGE:
        if op_data['url'] is not '':
            op_img = get_image(op_data['url'])
            if op_img is not None:
                show_image(op_img)
    print('Reply: {0}, Likes: {1}'.format(op_data['reply'], op_data['likenum']))

def show_comment_entry(comment):
    '''
    print a single entry in comments

    :param comment: the single entry of comments to print
    :return: no return
    '''
    print('#{0}'.format(comment['cid']))
    print(comment['text'])

def show_image(img_content, inline = 1, **kwargs):
    '''
    Show inline image in iTerm2

    :param img_content: the content of the image
    :param kwargs:
        name                    base-64 encoded filename. Defaults to "Unnamed file".
        size                    File size in bytes. Optional; this is only used by the progress indicator.
        width                   Width to render. See notes below.
        height                  Height to render. See notes below.
        preserveAspectRatio     If set to 0, then the image's inherent aspect ratio will not be respected;
                                otherwise, it will fill the specified width and height as much as possible
                                without stretching. Defaults to 1.
        inline                  If set to 1, the file will be displayed inline. Otherwise, it will be downloaded with
                                no visual representation in the terminal session. Defaults to 0.

        The width and height are given as a number followed by a unit, or the word "auto".

        + N: N character cells.
        + Npx: N pixels.
        + N%: N percent of the session's width or height.
        + auto: The image's inherent size will be used to determine an appropriate dimension.
    :return: no return
    '''
    img_encoded = base64.b64encode(img_content).decode('utf8')
    protocol_str = '\033]1337;File='

    opt_args = 'inline=' + str(inline)
    for k,v in kwargs.items():
        opt_args += ';' + k + '=' + v

    protocol_str += opt_args
    protocol_str += ':' + img_encoded
    protocol_str += '\a'
    print(protocol_str)
