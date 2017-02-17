from flask import request, send_from_directory
import web.util.jinja as jinja
import web.util.tools as tools

def get(p):
    start = request.url.find("/file/view/") + 11
    finish = request.url.rfind("?") if tools.get("id") else len(request.url)
    filename = request.url[start:finish]
    if filename.startswith("."):
        return "error"

    id = tools.get('id')
    shortname = jinja.filename(filename, id)

    if tools.get('download'):
        return send_from_directory(p['c']['upload_dir'],
            filename, as_attachment=True,
            attachment_filename=shortname)
    
    return send_from_directory(
        p['c']['upload_dir'],
        filename, as_attachment=False)
