from Project.models import User, ChangedNotification, UserRole, Student, Principle, Semester, Class, Grade, \
    Students_Classes, TeachingPlan, Subject, Teacher, Teachers_Subjects, Score, ScoreDetails
from Project import app, db
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
    students = db.session.query(Student).join(User)
    if grade:
        students = students.filter(Student.grade.__eq__(Grade[grade]))
    if kw:
        students = students.filter(User.name.icontains(kw))
    if page:
        students = students.order_by(User.first_name.asc())
        page = int(page)
        page_size = app.config['CN_PAGE_SIZE']
        start = (page-1)*page_size
        students = students[start: start+page_size]
        return students
    return students.order_by(User.first_name.asc())
def load_students_count(id_class = None):
    counter = Student.query
    if id_class:
        counter = Students_Classes.query.filter(Students_Classes.class_id.__eq__(id_class))
    return counter.count()


def load_non_class_students(grade, kw = None, year = None):

    grade = Grade[grade]
    year = get_latest_semester().year if year == None else year
    class_students = (db.session.query(Student.user_id)
                .join(Students_Classes)
                .join(Class)
                .filter(Student.grade.__eq__(Class.grade),
                        Class.year.__eq__(year)))
    non_class_students = db.session.query(Student).join(User).join(Semester).filter(Student.user_id.not_in(class_students),
                                                                           Semester.year.__eq__(year),
                                                                           Student.grade.__eq__(grade))
    if kw:
        non_class_students = non_class_students.filter(User.name.icontains(kw))
    return non_class_students.order_by(User.first_name).all()

def load_priciples_all():
    return Principle.query.all()
def load_principles_name(name):
    return Principle.query.filter(Principle.type.__eq__(name)).first()

def get_latest_semester():
    return Semester.query.order_by(Semester.id.desc()).first()

def get_semester(year = None):
    semester = Semester.query
    if year:
        semester = semester.filter(Semester.year.__eq__(year))
    return semester.all()
def load_semester_by_id(id):
    return Semester.query.filter(Semester.id.__eq__(id)).first()
def load_years_of_semester():
    return db.session.query(Semester.year).distinct().all()

def load_classes_all(grade = None, kw = None, page = None, year = None):
    classes = Class.query
    if grade:
        classes = classes.filter(Student.grade.__eq__(Grade[grade]))
    if kw:
        classes = classes.filter(Class.name.icontains(kw))
    if year:
        classes = classes.filter(Class.year.__eq__(year))
    if page:
        classes = classes.all()
        page = int(page)
        page_size = app.config['CN_PAGE_SIZE']
        start = (page-1)*page_size
        classes = classes[start: start+page_size]
        return classes
    return classes.all()
def load_classes_count(year = None):
    counter = Class.query
    if year:
        counter = counter.filter(Class.year.__eq__(year))
    return counter.count()


def get_the_latest_class_of_student(student_id):
    return (db.session.query(Class)
            .join(Students_Classes)
            .filter(Students_Classes.student_id.__eq__(student_id))
            .order_by(Students_Classes.id.desc())
            .first())
def load_class(id = None, name = None):
    if id:
        return Class.query.filter(Class.id.__eq__(id)).first()
    if name:
        return Class.query.filter(Class.name.__eq__(name)).first()
    return None
def load_non_homeroom_teacher(year):
    myIDList = db.session.query(Teacher.user_id).join(Class).filter(Class.year.__eq__(year))
    myList = db.session.query(Teacher).filter(Teacher.user_id.not_in(myIDList)).all()
    return myList
def load_class_of_teacher(id, semester = None, grade = None, year = None):
    myclass = db.session.query(Class).join(TeachingPlan).filter(TeachingPlan.teacher_id==id)
    if semester:
        semester = load_semester_by_id(semester)
        myclass = myclass.filter(Class.year.__eq__(semester.year))
    if year:
        myclass = myclass.filter(Class.year.__eq__(year))
    if grade:
        myclass = myclass.filter(Class.grade.__eq__(Grade[grade]))
    return myclass.all()
def load_subject_planned_teacher(id, class_id = None):
    subjects = db.session.query(Subject).join(TeachingPlan).filter(TeachingPlan.teacher_id == id,TeachingPlan.class_id == class_id).all()
    return subjects

def load_teachers_of_subject(id):
    return db.session.query(Teacher).join(Teachers_Subjects).filter(Teachers_Subjects.subject_id.__eq__(id)).all()

def load_subject_all(grade = None, non_plan = False, class_id=None):
    subjects = Subject.query
    if grade:
        subjects = subjects.filter(Subject.grade.__eq__(grade))
    if non_plan:
        alr_subjects = db.session.query(Subject.id).join(TeachingPlan).filter(TeachingPlan.class_id.__eq__(class_id))
        subjects = subjects.filter(Subject.id.not_in(alr_subjects))
    return subjects.all()

def load_teaching_plan(teacher_id, class_id = None, subject_id = None):
    myPlan = TeachingPlan.query.filter(TeachingPlan.teacher_id.__eq__(teacher_id))
    if class_id:
        myPlan = myPlan.filter(TeachingPlan.class_id.__eq__(class_id))

    if subject_id:
        myPlan = myPlan.filter(TeachingPlan.subject_id.__eq__(subject_id))

    return myPlan.all()
def load_teachers_subjects():
    return Teachers_Subjects.query.all()

def load_score_of_student(teaching_plan_id, student_id, semester):
    return Score.query.filter(Score.plan_id.__eq__(teaching_plan_id),
                              Score.student_id.__eq__(student_id),
                              Score.semester_id.__eq__(semester)).first()

