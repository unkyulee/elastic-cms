from flask import render_template, request
import os
import hglib
import web.util.tools as tools
from hglib.error import CommandError

def get(p):
    # load mercury list
    repository = p['c'].get('mercurial_path')
    client = hglib.client.hgclient(repository, None, None, False)
    client._args += ['--cwd', repository]
    client.open()

    p['hg'] = {}

    # open the file
    filepath = '/'.join(p['nav'][3:])
    p['hg']['filename'] = filepath
    p['hg']['filepath'] = os.path.join(repository, filepath)

    with file(p['hg']['filepath']) as f:
        p['hg']['content'] = f.read()

    if request.method == "POST":
        return post(p, client)

    # get status
    status = client.status()
    status = [s[0] for s in status if s[-1] == filepath]
    if len(status) > 0:
        status = status[-1]
    else:
        status = ''

    # diff
    p['hg']['diff'] = client.diff([filepath])

    # get details of the file
    log = client.log(files=[filepath], limit=1)
    if len(log): log = log[0]
    p['hg']['log'] = {
        'status': status,
        'revision': log[0],
        'revision_id': log[1],
        'updated_by': log[4],
        'updated': log[-1]
    }

    return render_template("mercurial/commit/default.html", p=p)



def post(p, client):

    # check if commit message exists
    if not tools.get('comment'):
        return tools.alert('requires comment')

    # commit changes
    try:
        client.commit(
            message=tools.get('comment'),
            user=p['login'],
            include=[p['hg']['filename']]
        )
    except CommandError as e:
        return tools.alert(str(e))

    return tools.redirect("{}/view/{}".format(p['url'], p['hg']['filename']))
