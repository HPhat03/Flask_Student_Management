import json
import math
from datetime import datetime, date

import cloudinary.uploader
from flask import Flask, request, render_template, redirect, url_for, request, session, jsonify
from flask_login import  current_user, login_user, login_required, logout_user
from Project import app, login, dao, utils
from Project.models import UserRole, Grade
from Project.forms import LoginForm, AddUserForm

from decorator import role_only
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
    pages = math.ceil(total/app.config['CN_PAGE_SIZE'])
    page = int(page)
    if page == 1:
        tags = {'start': 1,'end': pages if 3>pages else 3}
    elif page == pages:
        tags = {'start': page-2, 'end': page}
    else:
        tags = {'start': page-1,'end' : page if page+1 > pages else page+1}
    return render_template("menu.html", tags = tags, notifications=changed)
@app.route('/nhanvien/quan_ly_sinh_vien')
@login_required
# @role_only(UserRole.NHANVIEN)
def student_management():

    kw = request.args.get('kw')
    grade = request.args.get('grade')
    page = request.args.get("page")
    page = page if page else 1
    students = dao.load_students_all(grade=grade, kw=kw)
    total = dao.load_students_count()
    pages = math.ceil(total / app.config['CN_PAGE_SIZE'])
    page = int(page)
    if page == 1:
        tags = {'start': 1, 'end': pages if 3 > pages else 3}
    elif page == pages:
        tags = {'start': page - 2, 'end': page}
    else:
        tags = {'start': page - 1, 'end': page if page + 1 > pages else page + 1}
    return render_template('nhanvien/StudentManagement.html', stuList = students, tags = tags)

@app.route('/nhanvien/them_hoc_sinh', methods = ["GET", "POST"])
@login_required
# @role_only(UserRole.NHANVIEN)
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
    print(session_pending)
    for c in session['pending_users'].values():
        if c != session['pending_users']['msg'] and c!= session['pending_users']['total']:
            users_pending.append(c)
    msg = session_pending['msg']
    amount = session_pending['total']
    return render_template('nhanvien/AddStudent.html', form = form, users_pending = users_pending, msg = msg, amount= amount)
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
    print(isHocSinh)
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
                     'link': '#'},
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

#API TESTING
@app.route("/api/users", methods = ['GET', 'POST'])
def getuser():
    test = dao.load_user_all()
    list = []
    for t in test:
        temp = {
            "id": t.id,
            "name": t.name,
            "username": t.username,
            "password": t.password,
            "user_role": UserRole(t.user_role).name
        }
        list.append(temp)
    return jsonify(list)


@app.route('/api/user_pending', methods = ["POST"])
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
            'phone': phone
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
    print(users_pending[id])
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
        name = users_pending[id]['name']
        gender = users_pending[id]['gender']
        address = users_pending[id]['address']
        birthdate = users_pending[id]['birthdate']
        image = users_pending[id]['image']
        email = users_pending[id]['email']
        phone = users_pending[id]['phone']

        temp = utils.remove_accents(name).lower().split(" ")
        username = ""
        password = ""
        for i in range(len(temp)):
            if i < len(temp)-1:
                username += temp[i][0]
            else:
                username += temp[i]
            password += temp[i]

        msg = {}
        try:
            utils.student_registered(name = name, gender = gender,
                                     address = address, birthdate=birthdate, image=image,
                                     username = username, password=password, email = email,
                                     phone = phone)
        except Exception as ex:
            msg = {"status": "failed", "message" : f"Hệ thống lỗi: {ex}"}
        else:
            msg = {"status": "success", "message": f"Thêm thành công"}
            utils.commit_changes("Thêm 1 học sinh")
            users_pending['total'] -= 1
            del users_pending[id]
        session['pending_users'] = users_pending
        print(username, password, gender, address, birthdate, email, phone)
    return jsonify(msg)
if __name__ == "__main__":
    app.run()