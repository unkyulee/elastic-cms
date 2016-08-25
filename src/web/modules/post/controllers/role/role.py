from flask import request, render_template
from Web.lib import *
from Web.model import *
from Web.module_navigation_setting.form import *

def GetHTML(p):

    if p["path"] == "role":
        # Role List
        # Load Role List
        p["RoleList"] = Role.query.filter_by(SiteId = p["SiteId"]).all()
        # Load Permission List
        p["PermissionList"] = {}
        for r in p["RoleList"]:
            p["PermissionList"][r.id] = []
            Permissions = Permission.query.filter_by(RoleId=r.id).all()
            for perm in Permissions:
                p["PermissionList"][r.id].append(perm.LoginId)

        return render_template("post/admin.html", p=p)


    elif p["path"] == "new_role":
        # Role
        form = RoleForm(request.form)
        # Save Role
        NewRole = Role(form.SiteId.data, form.Name.data)
        db.session.add(NewRole)
        db.session.commit()
        # Create Permission
        for v in request.form.getlist('AssignedUsers'):
            db.session.add(Permission(NewRole.id, v))
        db.session.commit()

        return redirect(p["Site"], p["Navigation"],
            "{}/role".format(p["Operation"]) )


    elif p["path"] == "save_role":
        form = RoleForm(request.form)
        # Save Role
        EditRole = Role.query.filter_by(id=form.id.data).first()
        EditRole.Name = form.Name.data
        # Delete Existing Permission
        Permission.query.filter_by(RoleId=form.id.data).delete()
        # Create Permission
        for v in request.form.getlist('AssignedUsers'):
            db.session.add(Permission(EditRole.id, v))
        db.session.commit()
        return redirect(p["Site"], p["Navigation"],
            "{}/role".format(p["Operation"]) )


    elif p["path"] == "delete_role":
        # Role
        form = RoleForm(request.form)
        Permission.query.filter_by(RoleId=form.id.data).delete()
        Role.query.filter_by(id=form.id.data).delete()
        db.session.commit()

        return redirect(p["Site"], p["Navigation"],
            "{}/role".format(p["Operation"]) )
