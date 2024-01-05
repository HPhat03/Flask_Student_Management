import math
from datetime import date

import cloudinary.uploader
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import  current_user, login_user, login_required, logout_user
from Project import app, login, dao, utils, db
from Project.models import UserRole, Grade, Class, Students_Classes
from Project.forms import LoginForm, AddUserForm
from Project.decorator import role_only

@login.user_loader
def user_load(user_id):
    return dao.load_user(user_id)

@app.route("/")
def index():

    if current_user.is_authenticated:
        return redirect(url_for("auth"))

    return redirect(url_for("login"))

@app.route("/login", methods = ["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    msg = ""
    if request.method == "POST" and form.is_submitted():
        username = form.username.data
        password = form.password.data
        type = form.userType.data
        user = utils.check_user(username, password, type)
        if user and session.get('role'):
            login_user(user)
            return redirect(url_for("index"))
        msg = "Đăng nhập thất bại"
    return render_template("login.html", msg = msg, form = form)
@app.route("/home/")
@login_required
def auth():
    filter = request.args.get("filter")
    page = request.args.get("page")
    page = page if page else 1
    changed = dao.load_changed_notification(filter=filter, page=page)

    total = dao.load_changed_notifications_count()
    tags = utils.pageTags(total, page)
    return render_template("menu.html", tags = tags, notifications=changed)
@app.route('/nhanvien/quan_ly_sinh_vien')
@login_required
@role_only('NHANVIEN')
def student_management():

    kw = request.args.get('kw')
    grade = request.args.get('grade')
    page = request.args.get("page")
    page = page if page else 1
    students = dao.load_students_all(grade=grade, kw=kw, page=page)
    total = dao.load_students_count()
    tags = utils.pageTags(total, page)
    return render_template('nhanvien/StudentManagement.html', stuList = students, tags = tags)

@app.route('/nhanvien/them_hoc_sinh')
@login_required
@role_only('NHANVIEN')
def add_student():
    form = AddUserForm()
    # session['pending_users'] = None
    session_pending = session.get('pending_users')
    if session_pending is None:
        session_pending = {}
        session_pending['msg'] = {}
        session_pending['total'] = 0
        session['pending_users'] = session_pending
    users_pending = []
    for c in session['pending_users'].values():
        if c != session['pending_users']['msg'] and c!= session['pending_users']['total']:
            users_pending.append(c)
    msg = session_pending['msg']
    amount = session_pending['total']
    return render_template('nhanvien/AddStudent.html', form = form, users_pending = users_pending, msg = msg, amount= amount)
@app.route('/nhanvien/quan_ly_lop_hoc')
@login_required
@role_only('NHANVIEN')
def class_management():
    kw = request.args.get('kw')
    grade = request.args.get('grade')
    page = request.args.get("page")
    page = page if page else 1
    classes = dao.load_classes_all(grade=grade, kw=kw, page=page)
    total = dao.load_classes_count()

    tags = utils.pageTags(total, page)
    return render_template('nhanvien/ClassesManagement.html', clsList= classes, tags=tags)

@app.route('/nhanvien/them_lop_hoc', methods = ['GET', 'POST'])
@login_required
@role_only('NHANVIEN')
def add_classes():
    msg = None
    if request.method == "POST":
        grade = request.form.get('grade')
        class_size = dao.load_principles_name('CLASS_MAX').data
        amount = request.form.get('amount')
        students = dao.load_non_class_students(grade)
        year = dao.get_latest_semester().year
        try:
            if Grade[grade] == Grade.K10:
                current_classes = dao.load_classes_all(grade = grade, year=year)
                if len(current_classes) != 0:
                    utils.add_students_to_classes(students=students, classes=current_classes, max = class_size)
                if len(students) > 0:
                    class_amount = math.ceil(len(students) / class_size)
                    counter = dao.load_classes_count(year)
                    classes = []
                    for i in range(class_amount):
                        name = f"{Grade[grade].value}A{"{:02}".format(counter+i+1)}"
                        tempClass = Class(name= name, amount = class_size,
                                          grade = Grade[grade], year = year)
                        db.session.add(tempClass)
                        db.session.commit()
                        classes.append(tempClass)
                    utils.commit_changes(f"tạo {class_amount} lớp")
                    utils.add_students_to_classes(students=students, classes=classes, max=class_size)
            else:
                for s in students:
                    old_class = dao.get_the_latest_class_of_student(s[0].id).name
                    index_class = old_class[-2:]
                    name = str(Grade[grade].value)
                    match Grade[grade]:
                        case Grade.K11:
                            name += "B"
                        case Grade.K12:
                            name += "C"
                    name += index_class
                    now_class = dao.load_class(name=name)
                    if now_class:
                        temp = Students_Classes(class_id = now_class.id, student_id = s[0].id)
                        db.session.add(temp)
                        db.session.commit()
                    else:
                        tempClass = Class(name = name,amount = class_size, grade = Grade[grade], year = year)
                        db.session.add(tempClass)
                        db.session.commit()
                        utils.commit_changes("tạo 1 lớp")
                        temp = Students_Classes(class_id = tempClass.id, student_id = s[0].id)
                        db.session.add(temp)
                        db.session.commit()
        except Exception as exc:
            msg = {
                'status' : "failed",
                'message' : exc
            }
        else:
            utils.commit_changes(f"phân lớp cho {amount} sinh viên")
            msg = {
                'status': "success",
                'message': "Tạo thành công"
            }
    return render_template('nhanvien/AddClasses.html', Grade = Grade, msg = msg)
@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/user/<user_id>")
@login_required
def info(user_id):
    user = dao.load_user(user_id)
    isHocSinh = False
    for r in user.roles:
        if r.role == UserRole.HOCSINH:
            isHocSinh = True
            break
    return render_template('user_detail.html', user = user, UserRole = UserRole, isHocSinh = isHocSinh)

@app.context_processor
def common_things():
    missions = []
    msg = ""
    if current_user.is_authenticated:
        role = session.get('role')
        match role:
            case 'NHANVIEN':
                msg = "Xin chào nhân viên %s" % current_user.name
                missions = [
                    {'name': 'Quản lý sinh viên',
                     'link': "/nhanvien/quan_ly_sinh_vien"},
                    {'name': 'Quản lý lớp',
                     'link': '/nhanvien/quan_ly_lop_hoc'},
                    {'name': 'Quy định chung',
                     'link': '#'}
                ]
            case 'ADMIN':
                msg = "Xin chào quản trị %s" % current_user.name
                missions = [
                    {'name': 'Quản lý môn học',
                     'link': '#'},
                    {'name': 'Thống kê báo cáo',
                     'link': '#'},
                    {'name': 'Quản lý quy định',
                     'link': '#'}
                ]
            case 'GIAOVIEN':
                msg = "Xin chào giáo viên %s" % current_user.name
                missions = [
                    {'name': 'Lớp',
                     'link': '#'},
                    {'name': 'Quản lý Điểm',
                     'link': '#'},
                    {'name': 'Quy định chung',
                     'link': '#'}
                ]
    return {
        'missions': missions,
        'msg' : msg
    }

#API
@app.route('/api/user_pending', methods = ["POST"])
@login_required
def pending():
    list = session.get('pending_users')
    age_start = dao.load_principles_name("AGE_START")
    age_end = dao.load_principles_name("AGE_END")

    name = request.form.get('name')
    gender = int(request.form.get('gender'))
    image = request.files.get('image')
    birthdate = request.form.get('birthdate')
    address = request.form.get('address')
    email = request.form.get('email')
    phone = request.form.get('phone')
    grade = request.form.get('grade')
    birthyear = int(birthdate[:4])
    birthmonth = int(birthdate[5:7])
    birthday = int(birthdate[8:10])
    acceptable = True
    error = ""


    age = date.today().year - birthyear
    if age < int(age_start.data) or age > int(age_end.data):
        acceptable = False
        error = "Số tuổi không đúng quy định"

    for i in range(1, list['total']+1):
        if list[str(i)]['name'] == name:
            acceptable = False
            error = "Người dùng đã được thêm vào hàng chờ"
    if utils.check_user_by_name(name):
        acceptable = False
        error = "Tên người dùng đã tồn tại"



    if not acceptable:
        list['msg'] = {
            'status': "failed",
            'message': error
        }
    else:
        if image:
            res = cloudinary.uploader.upload(image)
            image = res['secure_url']
        else:
            image = "https://res.cloudinary.com/dzm6ikgbo/image/upload/v1703999894/okrajh0yr69c5fmo3swn.png"
        list[str(list["total"]+1)] = {
            'id': list["total"]+1,
            'name': name,
            'gender': gender,
            'image': image,
            'birthdate': f'{birthday}-{birthmonth}-{birthyear}',
            'address': address,
            'email': email,
            'phone': phone,
            'grade': grade
        }
        list['msg'] = {
            'status': "success",
            'message': "Người dùng được thêm vào hàng chờ"
        }
    list['total'] = len(list)-2
    session['pending_users'] = list
    return redirect(url_for("add_student"))
@app.route('/api/user_pending/<id>', methods = ["DELETE"])

def pending_del(id):
    users_pending = session.get('pending_users')
    if users_pending and id in users_pending:
        image = users_pending[id]['image'].split("/")
        public_id = image[-1][:-4]
        cloudinary.uploader.destroy(public_id)
        users_pending['total'] -= 1
        del users_pending[id]
    session['pending_users'] = users_pending
    return jsonify(users_pending)
@app.route('/api/validate_user/<id>', methods = ["POST"])
def validate_user(id):
    users_pending = session.get('pending_users')
    if users_pending and id in users_pending:
        msg = utils.objectRegister(users_pending[id])
        if msg and msg['status']=='success':
            utils.commit_changes("Thêm 1 học sinh")
            users_pending['total'] -= 1
            del users_pending[id]
        session['pending_users'] = users_pending
    return jsonify(msg)
@app.route('/api/validate_user', methods = ["POST"])
def validate_all():
    user = []
    count = 0
    overview = {
        "status" : "success",
        "failed" : [],
        "success" : []
    }
    session_pending = session.get('pending_users')
    for pu in session['pending_users'].values():
        if pu != session['pending_users']['total'] and pu!= session['pending_users']['msg']:
            user.append(pu)
    if user == []:
        overview = {"status": "failed", "message":"Danh sách rỗng!"}
        return jsonify(overview)    
    for u in user:
        msg = utils.objectRegister(u)
        if msg and msg['status']=='success':
            overview['success'].append(u['id'])
            count += 1
            del session_pending[str(u['id'])]
            session_pending['total'] -= 1
        else:
            overview['failed'].append(u['name'])
    utils.commit_changes(f"thêm {count} học sinh")
    session['pending_users'] = session_pending
    return jsonify(overview)

@app.route('/api/non_class_student/<grade>')
def get_non_class(grade):

    students = dao.load_non_class_students(grade)
    list = []
    for s in students:
        temp = {
            'id': s[0].id,
            'name': s[0].name,
            'grade': s[1].grade.value,
            'semester': f"Học kì {s[1].semester.semester} năm {s[1].semester.year}"
        }
        list.append(temp)
    return jsonify(list)
if __name__ == "__main__":
    app.run()