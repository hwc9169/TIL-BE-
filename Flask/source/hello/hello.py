from flask import Flask,make_response,render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Email
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail,Message
import os

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    # Message(title, sender, recipient)

    msg.body = 'NEW USER'#render_template(template + '.txt', **kwargs)
    #msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)

class NameForm(Form):
    name = StringField('Name', validators=[Required()])
    email = StringField('Email', validators=[Email(),Required()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string' #암호화설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hwc9169@gmailc.com'
app.config['MAIL_PASSWORD'] = '12345678'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'flasky@example.com'
app.config['FLASKY_ADMIN'] = 'hwc9169@gmail.com'

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
migrate = Migrate(app,db)
mail = Mail(app)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand) #Flask-Migrate는 Flask-Script의 manager 오브젝트에 MigrateCommand를 연결하였다. 여기서 커맨드는 db를 사용한다


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    user = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ ='users'
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(100), index=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' %self.username


@app.route('/control/<user>')
def control(user):
    return render_template('control.html',user=user,comments=["wtf","sex","That is great!"])

@app.route('/index', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)

        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known',False))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.errorhandler(404)
def Not_Found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
    print(app.config['FLASKY_ADMIN'])
    #manager.run()
    app.run(debug=True)
