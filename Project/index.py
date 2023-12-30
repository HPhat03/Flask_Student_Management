import json

from flask import Flask, request, render_template, redirect, url_for, request, session, jsonify
from flask_login import  current_user, login_user, login_required, logout_user
from Project import app, login, dao, utils
from Project.models import UserRole, LoginForm

@login.user_loader
def user_load(user_id):
    return dao.load_user(user_id)

@app.route("/")
def index():

    if current_user.is_authenticated:
        role = session.get('role')
        match role:
            case 'NHANVIEN':
                return redirect(url_for('nhan_vien'))
            case 'ADMIN':
                return redirect(url_for('admin'))
            case'GIAOVIEN':
                return redirect(url_for('giao_vien'))
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
@app.route("/index/")
@login_required
def auth():
    return "Hello %s" % current_user.name
@app.route("/nhanvien/")
@login_required
def nhan_vien():
    message = "Xin chào nhân viên %s." % current_user.name
    return  render_template("menu.html", msg = message)
@app.route("/admin/")
@login_required
def admin():
    message = "Xin chào admin %s." % current_user.name
    return render_template("menu.html", msg=message)
@app.route("/giaovien/")
@login_required
def giao_vien():
    message = "Xin chào giáo viên %s." % current_user.name
    return render_template("menu.html", msg=message)
@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.context_processor
def common_things():
    missions = []
    role = session.get('role')
    match role:
        case 'NHANVIEN':
            missions = [
                {'name': 'Quản lý sinh viên',
                 'link': '#'},
                {'name': 'Quản lý lớp',
                 'link': '#'},
                {'name': 'Quy định chung',
                 'link': '#'}
            ]
        case 'ADMIN':
            missions = [
                {'name': 'Quản lý môn học',
                 'link': '#'},
                {'name': 'Thống kê báo cáo',
                 'link': '#'},
                {'name': 'Quản lý quy định',
                 'link': '#'}
            ]
        case 'GIAOVIEN':
            missions = [
                {'name': 'Lớp',
                 'link': '#'},
                {'name': 'Quản lý Điểm',
                 'link': '#'},
                {'name': 'Quy định chung',
                 'link': '#'}
            ]
    return {
        'missions': missions
    }

#API TESTING
@app.route("/api/users", methods = ['GET'])
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


@app.route('/api/test')
def testapi():
    return render_template('test.html')

@app.route('/api/changed_notification', methods = ['GET'])
def getChNo():
    notifications = dao.load_changed_notification()
    myNote = []
    for n in notifications:
        temp = {
            'actor': n.user_detail.name,
            'role': str(n.user_role),
            'content': n.content,
            'time': n.created_date
        }
        myNote.append(temp)
    return jsonify(myNote)

if __name__ == "__main__":
    app.run()