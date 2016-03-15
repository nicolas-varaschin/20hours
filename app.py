from wtforms import Form, BooleanField, TextField, PasswordField, validators
from flask import Flask, render_template, request,Response, jsonify,redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
import random
from os import environ
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '<replace with a secret key>'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    tasks = relationship("Task")

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.username'))
    name = db.Column(db.String)
    time = db.Column(db.Integer)

    def to_json(self):
      return {'name':self.name, 'time': self.time}

from sqlalchemy import create_engine
engine = create_engine('sqlite:///app.db')
from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)


class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.Required(),
    ])


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


@app.route('/', methods=['GET',"POST"])
def index():
   form = LoginForm(request.form)
   if form.validate():
      if session().query(User).get(form.data['username']):
        return redirect(url_for('tasks',user=form.data['username']))
   return render_template('index.html', form=form)

@app.route('/register', methods=['GET',"POST"])
def register():
   form = RegistrationForm(request.form)
   if form.validate():
      if session().query(User).get(form.data['username']):
        return 'Existing'
      user = User(username=form.data['username'], password=form.data['password'])
      s = session()
      s.add(user)
      s.commit()
      return redirect(url_for('index'))
   return render_template('register.html', form=form)

@app.route('/tasks', methods=['GET'])
def tasks():
   return render_template('tasks.html', user=request.args['user'])

@app.route('/task/<user>/<name>', methods=['DELETE','POST'])
def task(user, name):
  s = session()
  if request.method == "DELETE":
    u = s.query(User).get(user)
    for task in u.tasks:
      if task.name == name:
        u.tasks.remove(task)
        s.commit()
        break
  if request.method == "POST":
    task = Task(name=name, time=23*60*60*1000)
    user = s.query(User).get(user)
    user.tasks.append(task)
    s.add(task)
    s.add(user)
    s.commit()
  return ''

@app.route('/task_edit/<user>/<name>/<new_name>/<time>', methods=['PUT'])
def task_new_name(user, name, new_name,time):
  if request.method == "PUT":
    s = session()
    user = s.query(User).get(user)
    for task in user.tasks:
      if task.name == name:
        task.name = new_name
        task.time = time
        s.add(task)
        s.commit()
        break
  return ''

@app.route('/task/<user>/<name>/<time>', methods=['PUT'])
def task_put(user, name, time):
  if request.method == "PUT":
    s = session()
    user = s.query(User).get(user)
    for task in user.tasks:
      if task.name == name:
        task.time = time
        s.add(task)
        s.commit()
        break
  return ''


@app.route('/user/<name>', methods=['GET'])
def query_user(name):
    user = session().query(User).get(name)
    if user:
      return jsonify({'username':user.username, 'tasks': [x.to_json() for x in user.tasks]})
    return ''

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False,port=int(environ.get('PORT',5000)),host='0.0.0.0'    )

