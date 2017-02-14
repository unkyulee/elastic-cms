import lib.gmail as gmail
import web.util.tools as tools
import web.util.jinja as jinja
from . import config

def set_conf(host, index, conf):
    config.set_conf(host, index, 'gmail_id', conf.get('gmail_id'))
    config.set_conf(host, index, 'gmail_pw', conf.get('gmail_pw'))


def get_conf(host, index):
    conf = {
        'gmail_id': config.get_conf(host, index, 'gmail_id', ''),
        'gmail_pw': config.get_conf(host, index, 'gmail_pw', '')
    }
    return conf


def send(p):
    conf = get_conf(p['c']['host'], p['c']['index'])

    # transform header and message
    header = jinja.render(p['notification'].get('header'), p)
    message = jinja.render(p['notification'].get('message'), p)
    recipients = list(set(p['notification'].get('recipients')))

    gmail.send(
        conf.get('gmail_id'),
        conf.get('gmail_pw'),
        recipients,
        header,
        message
    )

    return True
