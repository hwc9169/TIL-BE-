from flask import Flask,make_response,render_template, session, redirect, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Email
from flask_wtf import Form

class NameForm(Form):
    name = StringField('Name', validators=[Required()])
    email = StringField('Email', validators=[Email(),Required()])
    submit = SubmitField('Submit')

app = Flask(__name__)
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
        session['name'] = form.name.data
        session['email'] = form.email.data
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
