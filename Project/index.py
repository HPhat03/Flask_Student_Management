import json

from flask import Flask, request, render_template, redirect, url_for, request, flash, jsonify
from flask_login import  current_user, login_user, login_required, logout_user
from Project import app, login, dao, untils, models

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
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = untils.check_user(username, password)
        if user:
            login_user(user = user)
            return  redirect(url_for('auth'))
        else:
            msg = "Sai thong tin"
    return render_template("login.html", msg = msg)
@app.route("/index/")
# @login_required
def auth():
    return "Hello %s" % current_user.name

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("index"))

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
            "user_role": models.UserRole(t.user_role).name
        }
        list.append(temp)
    return jsonify(list)


@app.route('/api/test')
def testapi():
    return render_template('test.html')

if __name__ == "__main__":
    app.run()