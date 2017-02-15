import lib.gmail as gmail
import web.util.tools as tools
import web.util.jinja as jinja

def set_conf(host, conf):
    tools.set_conf(host, '-1', 'gmail_id', conf.get('gmail_id'))
    tools.set_conf(host, '-1', 'gmail_pw', conf.get('gmail_pw'))


def get_conf(host):
    conf = {
        'gmail_id': tools.get_conf(host, '-1', 'gmail_id', ''),
        'gmail_pw': tools.get_conf(host, '-1', 'gmail_pw', '')
    }
    return conf


def send(p, header, message, recipients):
    conf = get_conf(p['host'])

    # transform header and message
    header = jinja.render(header, p)
    message = jinja.render(message, p)
    recipients = list(set(recipients))

    gmail.send(
        conf.get('gmail_id'),
        conf.get('gmail_pw'),
        recipients,
        header,
        message
    )

    return True
