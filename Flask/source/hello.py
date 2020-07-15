from flask import Flask,make_response,render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Email
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy


class NameForm(Form):
    name = StringField('Name', validators=[Required()])
    email = StringField('Email', validators=[Email(),Required()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql://root:skyhelp9169@127.0.0.1/dpm'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
#암호화설정
app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/control/<user>')
def control(user):
    return render_template('control.html',user=user,comments=["wtf","sex","That is great!"])

@app.route('/index', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')

        session['name'] = form.name.data
        form.name.data = ''
        session['email'] = form.email.data
        form.name.email = ''
        return redirect(url_for('index'))
    return render_template('index.html',form = form, name = session.get('name'), email = session.get('email'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.errorhandler(404)
def Not_Found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
   # manager.run()
    app.run(debug=True)
