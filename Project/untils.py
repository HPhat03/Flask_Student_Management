import hashlib
from Project.models import User

def check_user(username, password):
    if username and password:
        enc_pass = hashlib.md5(str(password).encode("utf-8")).hexdigest()
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(enc_pass)).first()