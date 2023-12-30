import enum

from Project import app, db
from sqlalchemy import Column, Integer,String,Boolean, ForeignKey, DateTime, Enum, Text, Float, Date
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from wtforms.fields import StringField, SubmitField, PasswordField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, ValidationError
from datetime import datetime
#FORM
class LoginForm(FlaskForm):
    userType = SelectField("Đăng nhập theo: ", choices=[("NHANVIEN", "Nhân viên"), ("ADMIN", "Người quản trị"), ("GIAOVIEN", "Giáo viên")])
    username = StringField(validators=[InputRequired(), Length(min=1, max=15)], render_kw={"placeholder": "Tên đăng nhập"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Mật khẩu"})
    submit = SubmitField("Đăng nhập")
#ENUM
class UserRole(enum.Enum):
    HOCSINH = 0,
    NHANVIEN = 1,
    GIAOVIEN = 2,
    ADMIN = 3

class LoaiTTLL(enum.Enum):
    EMAIL = 0,
    DTCANHAN = 1
class Grade(enum.Enum):
    K10 = 0,
    K11 = 1,
    K12 = 2
class ScoreType(enum.Enum):
    MINS15 = 0,
    MINS45 = 1,
    FINAL = 2
#DATABASE ORM
class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default= True)

class User(BaseModel, UserMixin):
    name = Column(String(50), nullable= False)
    gender = Column(Boolean)
    address = Column(Text)
    birthdate = Column(String(10))
    username = Column(String(20), nullable= False, unique=True)
    password = Column(String(100), nullable=False)
    image = Column(String(100))

    students = relationship("Student", backref="info", lazy=True)
    employees = relationship('Employee', backref="info", lazy= True)
    contacts = relationship('UserContact', backref = "user", lazy=True)

    roles = relationship("UserRoles", backref="user_info", lazy=True)
    admins = relationship("Admin", backref="info", lazy=True)
    teachers = relationship("Teacher", backref="info", lazy=True)
    changes = relationship("ChangedNotification", backref="user_detail", lazy=True)

class UserContact(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    contactType = Column(Enum(LoaiTTLL))
    contactData = Column(String(30))

class ActorBase(db.Model):
    __abstract__ = True

    started_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)
class Employee(ActorBase):
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True, nullable= False, unique= True)


class UserRoles(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable= False)
    role = Column(Enum(UserRole))

class Admin(ActorBase):
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True,unique=True, nullable=False)

class Teacher(ActorBase):
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True, unique=True, nullable=False)
    vanBang = Column(Text)

    classes = relationship("Class", backref="teacher_detail", lazy=True)
    subjects = relationship("Teachers_Subjects", backref="teacher_detail", lazy=True)
    scores = relationship("Score", backref="teacher_detail", lazy=True)
class Semester(db.Model):
    id = Column(String(3), primary_key=True, nullable=False)
    semester = Column(Integer, nullable=False)
    year = Column(String(9), nullable=False)

    classes = relationship("Class", backref="semester", lazy=True)
    students = relationship("Student", backref="semester", lazy=True)
    scores = relationship("Score", backref="semester", lazy=True)
class Class(BaseModel):
    name = Column(String(5), nullable=False)
    amount = Column(Integer, default=0)
    grade = Column(Enum(Grade), nullable=False)
    semester_id = Column(String(3), ForeignKey(Semester.id), nullable=False)
    teacher_id = Column(Integer, ForeignKey(Teacher.user_id))

    students = relationship("Students_Classes", backref="class_detail", lazy=True)

class Student(ActorBase):
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True, unique=True, nullable=False)
    grade = Column(Enum(Grade), nullable=False)
    semester_id = Column(String(3), ForeignKey(Semester.id), nullable=False)


    classes = relationship("Students_Classes", backref="student_detail", lazy=True)
    scores = relationship("Score", backref="student_detail", lazy=True)
class Students_Classes(db.Model):
    id = Column(Integer, primary_key=True, nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    student_id = Column(Integer, ForeignKey(Student.user_id), nullable=False)

class Subject(BaseModel):
    name = Column(String(20), nullable=False)
    grade = Column(Enum(Grade), nullable=False)

    teachers = relationship("Teachers_Subjects", backref="subject_detail", lazy=True)
    scores = relationship("Score", backref="subject_detail", lazy=True)
class Teachers_Subjects(db.Model):
    teacher_id = Column(Integer, ForeignKey(Teacher.user_id), primary_key=True, nullable=False)
    subject_id = Column(Integer,ForeignKey(Subject.id), primary_key=True, nullable=False)

class Score(BaseModel):
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)
    student_id = Column(Integer, ForeignKey(Student.user_id), nullable=False)
    semester_id = Column(String(3), ForeignKey(Semester.id), nullable=False)
    teacher_id = Column(Integer, ForeignKey(Teacher.user_id), nullable=False)

    details = relationship("ScoreDetails", backref="info", lazy=True)
class ScoreDetails(BaseModel):
    score_id = Column(Integer, ForeignKey(Score.id), nullable=False)
    score_type = Column(Enum(ScoreType), nullable=False)
    score = Column(Float)

class Principle(BaseModel):
    type = Column(String(20), nullable=False, unique=True)
    data = Column(Float)
    description = Column(Text)

class ChangedNotification(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id))
    user_role = Column(Enum(UserRole), nullable=False)
    content = Column(Text)
if __name__ == "__main__":
    from Project import  app
    with app.app_context():
        db.create_all()
        import hashlib
        u1 = User(name = "Mai Hoàng Phát", gender = True, address = "Nha Trang", birthdate = "08-11-2003",
                  username = "mhphat", password = hashlib.md5("123456".encode("utf-8")).hexdigest())
        u2 = User(name="Nguyễn Văn A", gender=True, address="TP. Hồ Chí Minh",
                  birthdate='10-11-2003',
                  username="nva", password=hashlib.md5('123456'.encode("utf-8")).hexdigest())
        u3 = User(name="Trần Văn B", gender=True, address="TP. Hồ Chí Minh",
                  birthdate='25-08-2003',
                  username="tvb", password=hashlib.md5("123456".encode("utf-8")).hexdigest())


        nv1 = UserRoles(user_id = 1, role = UserRole.NHANVIEN)
        nv2 = UserRoles(user_id= 2, role = UserRole.NHANVIEN)
        ad1 = UserRoles(user_id = 2, role = UserRole.ADMIN)
        gv1 = UserRoles(user_id = 3, role = UserRole.GIAOVIEN)

        no1 = ChangedNotification(user_id = 1, user_role = UserRole.NHANVIEN, content = "thay đổi giao diện front end" )
        no2 = ChangedNotification(user_id=1, user_role=UserRole.NHANVIEN, content="thay đổi models")
        no3 = ChangedNotification(user_id=1, user_role=UserRole.NHANVIEN, content="thay đổi templates")
        db.session.add_all([no1, no2, no3])
        db.session.commit()