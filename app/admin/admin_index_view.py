from flask_admin import AdminIndexView
from flask_login import current_user
from flask import abort

class NoteAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        abort(404)

