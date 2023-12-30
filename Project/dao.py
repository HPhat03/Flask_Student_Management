from Project.models import User, ChangedNotification
from Project import app
import hashlib

def load_user(user_id):
    return User.query.get(user_id)
def load_user_all():
    return User.query.all()
def load_changed_notification():
    return ChangedNotification.query.order_by(ChangedNotification.id.desc())