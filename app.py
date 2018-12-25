from flask import Flask, render_template, jsonify, make_response, request
# from flask.ext.restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json


app = Flask(__name__)
# api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:byn2316@localhost:3306/flask'
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
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    number = db.Column(db.String(10), nullable=False)
    age = db.Column(db.String(5), nullable=False)
    clas = number = db.Column(db.String(10), nullable=False)
    def __repr__(self):
        return '%r' % self.username

# users = [
#     {
#     'id': 1,
#     'name': 'baoyuan',
#     'age': 21
#     }, {
#     'id': 2,
#     'name': 'yenan',
#     'age': 21
#     }
# ]

# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User, Role=Role)

# @app.route('/users', methods=['GET'])
# def get_users():
#     users = User.query.all()
#     print(users)
#     resp = Response(users, mimetype="list")
#     return resp


@app.route('/users', methods=['POST'])
def add_users():
    username = request.form['username']
    number = request.form['number']
    password = request.form['password']
    id = Admin.query.filter(Admin.number == number).first()
    if id:
        return 'loged'
    else:
        user = Admin(number = number, password = password)
        db.session.add(user)
        db.session.commit()
        res = make_response('ok')
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res


# @app.route('/user/<name>')
# def user(name):
#     return render_template('user.html',name=name)
# class UserApi(Resource):
#     def get(self, number):
#         pass
#
#     def put(self, number):
#         pass
#
#     def delete(self, id):
#         pass
#
# api.add_resource(UserApi, '/users/<int: number>', endpoint = 'user')
