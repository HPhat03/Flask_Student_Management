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
    return  ''''<h1>Hello nhan vien %s<h1>
                <a href="/logout/">Đăng xuất</a>''' % current_user.name
@app.route("/admin/")
@login_required
def admin():
    return  ''''<h1>Hello admin %s<h1>
                <a href="/logout/">Đăng xuất</a>''' % current_user.name
@app.route("/giaovien/")
@login_required
def giao_vien():
    return  ''''<h1>Hello giao vien %s<h1>
                <a href="/logout/">Đăng xuất</a>''' % current_user.name
@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("index"))


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

if __name__ == "__main__":
    app.run()