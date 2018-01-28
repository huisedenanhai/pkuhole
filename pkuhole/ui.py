from . import utils

def show_debug_info(show_debug):
    utils.set_SHOW_DEBUG(show_debug)

def show_inline_image(show_inline_image):
    utils.set_SHOW_INLINE_IMAGE(show_inline_image)

def get_list(page_num = 1):
    params = {'action': 'getlist', 'p': str(page_num)}
    entrys = utils.get_responds(params)
    if entrys == None:
        return
    for msg in entrys['data']:
        print('-----------------------------------')
        utils.show_op_data(msg)

def get_entry(pid):
    params = {'action': 'getcomment', 'pid': str(pid)}
    comments = utils.get_responds(params)
    params = {'action': 'getone', 'pid': str(pid)}
    op = utils.get_responds(params)
    if comments == None or op == None:
        return
    print('-----------------------------------')
    utils.show_op_data(op['data'])
    for comment in comments['data']:
        print('...................................')
        utils.show_comment_entry(comment)