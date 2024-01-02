from Project.models import User, ChangedNotification, UserRole, Student, Principle, Semester, Grade
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

def load_changed_notifications_count():
    return ChangedNotification.query.count()

def load_students_all(grade = None, page = None, kw = None):
    students = Student.query
    if grade:
        students = students.filter(Student.grade.__eq__(Grade[grade]))
    if page:
        students = students.all()
        page = int(page)
        page_size = app.config['CN_PAGE_SIZE']
        start = (page-1)*page_size
        students = students[start: start+page_size]
        return students
    return students.all()
def load_students_count():
    return Student.query.count()

def load_priciples_all():
    return Principle.query.all()
def load_principles_name(name):
    return Principle.query.filter(Principle.type.__eq__(name)).first()

def get_latest_semester():
    return Semester.query.order_by(Semester.id.desc()).first()