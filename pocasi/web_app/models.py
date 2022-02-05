from flask_login import UserMixin

from pocasi.web_app import login_manager


@login_manager.user_loader
def load_user(user_id):
    if user_id == "0":
        return User()
    else:
        return None


# Projekt má jen jednoho uživatele
class User(UserMixin):
    id = 0
