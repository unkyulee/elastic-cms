import web.util.tools as tools

def get(p):

    # default - site configuration
    if not p["operation"]:
        from .controllers import default
        return default.get(p)


    elif p["operation"] == 'admin':
        from .controllers import admin
        return admin.get(p)


    elif p["operation"] == 'logout':
        from .controllers import logout
        return logout.get(p)


    return "web/modules/auth/control"


def authorize(p):
    return True
