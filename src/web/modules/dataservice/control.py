
def get(p):

    if not p['operation']:
        from .controllers import default
        return default.get(p)

    elif p["operation"] == "json":
        from .controllers import json
        return json.get(p)

    elif p["operation"] == "create":
        from .controllers import create
        return create.get(p)

    elif p["operation"] == "delete":
        from .controllers import delete
        return delete.get(p)

    elif p["operation"] == "edit":
        from .controllers import edit
        return edit.get(p)

    return "dataservice/control"


def authorize(p):
    return True
