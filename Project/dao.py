from Project.models import User, ChangedNotification, UserRole
from Project import app
import hashlib

def load_user(user_id):
    return User.query.get(user_id)
def load_user_all():
    return User.query.all()
def load_changed_notification(filter = None, page = None):
    mylist = ChangedNotification.query

    if filter:
        mylist = ChangedNotification.query.filter(ChangedNotification.user_role.__eq__(UserRole[filter]))
    if page:
        mylist = mylist.order_by(ChangedNotification.id.desc())
        page = int(page)
        page_size = app.config['CN_PAGE_SIZE']
        start = (page-1)*page_size
        mylist = mylist[start: start+page_size]
        return mylist
    return mylist.order_by(ChangedNotification.id.desc())