import lib.gmail as gmail
import web.util.tools as tools
import web.util.jinja as jinja

def set_conf(h, n, conf):
    tools.set_conf(h, n, 'gmail_id', conf.get('gmail_id'))
    tools.set_conf(h, n, 'gmail_pw', conf.get('gmail_pw'))

def get_conf(h, n):
    conf = {
        'gmail_id': tools.get_conf(h, n, 'gmail_id', ''),
        'gmail_pw': tools.get_conf(h, n, 'gmail_pw', '')
    }
    return conf

def send(p):
    h = p['host']; n = p['navigation']['id'];
    gmail_id = tools.get_conf(h, n, 'gmail_id', '')
    gmail_pw = tools.get_conf(h, n, 'gmail_pw', '')

    # transform header and message
    header = jinja.render(p['notification'].get('header'), p)
    message = jinja.render(p['notification'].get('message'), p)

    gmail.send(
        gmail_id,
        gmail_pw,
        p['notification'].get('recipients'),
        header,
        message
    )

    return True
