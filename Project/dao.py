from Project.models import User, NhanVien
from Project import app
import hashlib

def load_user(user_id):
    return User.query.get(user_id)
def load_user_all():
    return User.query.all()