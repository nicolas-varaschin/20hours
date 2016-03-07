from wtforms import Form, BooleanField, TextField, PasswordField, validators
from flask import Flask, render_template, request,Response, jsonify,redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
import random
from os import environ

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '<replace with a secret key>'    

db = SQLAlchemy(app)
#///
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
        return redirect(url_for('tasks'))
   return render_template('index.html', form=form)

@app.route('/register', methods=['GET',"POST"])
def register():
   form = RegistrationForm(request.form)
   if form.validate():
        return redirect(url_for('index'))
   return render_template('register.html', form=form)

@app.route('/tasks', methods=['GET'])
def tasks():
   return "ok"



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False,port=int(environ.get('PORT',5000)),host='0.0.0.0'    )

