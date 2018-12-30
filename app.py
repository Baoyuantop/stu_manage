from flask import Flask, render_template, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:******@localhost:3306/flask?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

migrate = Migrate(app,db)



class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer,primary_key=True)
    number = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    def __repr__(self):
        return self.number, self.password

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    age = db.Column(db.String(5), nullable=False)
    clas = db.Column(db.String(10), nullable=False)


# 注册管理员
@app.route('/users', methods=['POST'])
def add_users():
    user = request.get_json()
    username = user['username']
    number = user['number']
    password = user['password']
    id = Admin.query.filter(Admin.number == number).first()
    if id:
        response = make_response('logged')
        return response
    else:
        user = Admin(number = number, password = password)
        db.session.add(user)
        db.session.commit()
        response = make_response('ok')
        return response

# 管理员登陆
@app.route('/login', methods=['POST'])
def user_login():
    user = request.get_json()
    number = user['number']
    password = user['password']
    passwd = db.session.query(Admin.password).filter_by(number=number).first()
    print(passwd[0])
    print(password)
    if password == passwd[0]:
        response = make_response('true')
        response.set_cookie(number)
        return response
    else:
        response = make_response('false')
        return response
# 增加学生
@app.route('/add', methods=['POST'])
def user_add():
    user = request.get_json()
    username = user['name']
    number = user['number']
    age = user['age']
    clas = user['clas']
    id = User.query.filter(User.number == number).first()
    if id:
        response = make_response('had')
        return response
    else:
        user = User(username=username, number=number, age=age, clas=clas)
        db.session.add(user)
        db.session.commit()
        response = make_response('ok')
        return response
# 读取学生列表
@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()
    student = []
    for user in users:
        json_dist = {
            "name": user.username,
            "number": user.number,
            "age": user.age,
            "clas": user.clas
        }
        student.append(json_dist)
    return jsonify(student)
# 编辑学生信息
@app.route('/user/edit', methods=['POST'])
def edit_user():
    stu = request.get_json()
    stu_old = User.query.filter(User.number == stu['number']).first()
    stu_old.username = stu['name']
    stu_old.number = stu['number']
    stu_old.age = stu['age']
    stu_old.clas = stu['clas']
    db.session.commit()
    response = make_response('ok')
    return response
# 删除学生
@app.route('/user/del', methods=['POST'])
def del_user():
    stu = request.get_json()
    student = User.query.filter(User.number == stu['number']).first()
    db.session.delete(student)
    db.session.commit()
    response = make_response('ok')
    return response
