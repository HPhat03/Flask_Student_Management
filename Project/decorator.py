from flask import session, redirect, url_for
from Project.models import UserRole
def role_only(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if UserRole[session.get('role')] == role:
                return func(*args, **kwargs)
            return redirect(url_for('index'))
        return wrapper
    return decorator