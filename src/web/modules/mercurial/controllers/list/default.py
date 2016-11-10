from flask import render_template
import os
import hglib

def get(p):
    # load mercury list
    repository = p['c'].get('mercurial_path')
    client = hglib.client.hgclient(repository, None, None, False)
    client._args += ['--cwd', repository]
    client.open()

    p['hg'] = {}
    p['hg']['status'] = client.status()
    manifest = client.manifest()
    p['hg']['manifest'] = []
    for m in manifest:
        # ignore hidden files
        if m[-1].startswith('.'):
            continue

        # get status
        status = [status[0] for status in p['hg']['status'] \
                    if status[-1] == m[-1]]
        if len(status) > 0:
            status = status[-1]
        else:
            status = ''

        # get last changed author
        log = client.log(files=[m[-1]], limit=1)
        if len(log): log = log[0]

        item = {
            'manifest': m,
            'filename': m[-1],
            'status': status,
            'revision': log[0],
            'revision_id': log[1],
            'updated_by': log[4],
            'updated': log[-1]
        }

        p['hg']['manifest'].append(item)


    return render_template("mercurial/list/default.html", p=p)
