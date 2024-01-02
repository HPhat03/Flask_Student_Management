import hashlib
from Project.models import User, UserRole, Employee, Admin, UserRoles, Student, UserContact, LoaiTTLL, ChangedNotification
from flask import session
from Project import db,dao
from flask_login import current_user


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
def check_user_by_name(name):
    return User.query.filter(User.name.__eq__(name)).first()

def student_registered(name, gender, address, birthdate, username, password, **kwargs):
    password = hashlib.md5(str(password).encode('utf-8')).hexdigest()
    user = User(name = name,
                gender = gender,
                address = address,
                birthdate = birthdate,
                image = kwargs.get('image'),
                username = username,
                password = password)
    db.session.add(user)
    db.session.commit()
    print(user.id)
    role = UserRoles(user_id = user.id, role = UserRole.HOCSINH)
    semester_id = dao.get_latest_semester().id
    print(semester_id)
    hocsinh_info = Student(user_id = user.id, semester_id = semester_id)
    if kwargs.get("email"):
        email = UserContact(user_id = user.id, contactType = LoaiTTLL.EMAIL, contactData = kwargs.get('email'))
        db.session.add(email)
    if kwargs.get("phone"):
        phone = UserContact(user_id = user.id, contactType = LoaiTTLL.DTCANHAN, contactData = kwargs.get('phone'))
        db.session.add(phone)
    db.session.add_all([role, hocsinh_info])
    db.session.commit()

def commit_changes(content):
    user_id = current_user.id
    user_role = session.get('role')
    change = ChangedNotification(user_id = user_id, user_role = UserRole[user_role], content = content)
    db.session.add(change)
    db.session.commit()
def objectRegister(obj):
    name = obj['name']
    gender = obj['gender']
    address = obj['address']
    birthdate = obj['birthdate']
    image = obj['image']
    email = obj['email']
    phone = obj['phone']

    temp = remove_accents(name).lower().split(" ")
    username = ""
    password = ""
    for i in range(len(temp)):
        if i < len(temp) - 1:
            username += temp[i][0]
        else:
            username += temp[i]
        password += temp[i]

    msg = {}
    try:
        student_registered(name=name, gender=gender,
                                 address=address, birthdate=birthdate, image=image,
                                 username=username, password=password, email=email,
                                 phone=phone)
    except Exception as ex:
        msg = {"status": "failed", "message": f"Hệ thống lỗi: {ex}"}
    else:
        msg = {"status": "success", "message": f"Thêm thành công"}
    return msg

s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
def remove_accents(input_str):
	s = ""
	for c in input_str:
		if c in s1:
			s += s0[s1.index(c)]
		else:
			s += c
	return s