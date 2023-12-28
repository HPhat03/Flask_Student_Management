import hashlib
from Project.models import User, UserRole, Employee, Admin, UserRoles
from flask import session


def check_user(username, password, type):
    enc_pass = hashlib.md5(str(password).encode("utf-8")).hexdigest()
    user = User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(enc_pass)).first()
    if type != "HOCSINH" and user:
        roles = UserRoles.query.filter(UserRoles.user_id.__eq__(user.id)).all()
        for r in roles:
            if UserRole[type] == r.role:
                print('True')
                session['role'] = type
                return user

    session['role'] = None
    return user
