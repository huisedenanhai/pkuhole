from urllib.request import urlopen
import json

url = 'http://www.pkuhelper.com/services/pkuhole/api.php'
SHOW_DEBUG = False

def add_params(url, params):
    newurl = url + '?'
    for k, v in params.items():
        newurl += k + '=' + v + '&'
    newurl = newurl[:-1]
    return newurl

def get_responds(params):
    list_url = add_params(url, params)
    if SHOW_DEBUG:
        print(list_url)
    try:
        js = urlopen(list_url)
        js = json.load(js)
    except:
        print('Failed to get responds')
        return None
    return js

def show_op_data(op_data):
    '''
    show the msg of the original poster

    :param op_data: the 'data' feild of the original poster's decoded json
    :return: no return
    '''
    print(op_data['pid'])
    print(op_data['text'])
    print('Reply: {0}, Likes: {1}'.format(op_data['reply'], op_data['likenum']))

def show_comment_entry(comment):
    '''
    print a single entry in comments

    :param comment: the single entry of comments to print
    :return: no return
    '''
    print('#{0}'.format(comment['cid']))
    print(comment['text'])

def get_list(page_num = 1):
    params = {'action': 'getlist', 'p': str(page_num)}
    entrys = get_responds(params)
    if entrys == None:
        return
    for msg in entrys['data']:
        print('-----------------------------------')
        show_op_data(msg)

def get_entry(pid):
    params = {'action': 'getcomment', 'pid': str(pid)}
    comments = get_responds(params)
    params = {'action': 'getone', 'pid': str(pid)}
    op = get_responds(params)
    if comments == None or op == None:
        return
    print('-----------------------------------')
    show_op_data(op['data'])
    for comment in comments['data']:
        print('...................................')
        show_comment_entry(comment)

if __name__ == '__main__':
    get_list()
    get_entry(336767)