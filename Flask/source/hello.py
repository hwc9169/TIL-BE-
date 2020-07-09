from flask import Flask,make_response,render_template
from flask import request
from flask import redirect
from flask import abort
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
#암호화설정
app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/control/<user>')
def control(user):
    return render_template('control.html',user=user,comments=["wtf","sex","That is great!"])

@app.route('/index')
def index():
    return render_template('index.html',time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.errorhandler(404)
def Not_Found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
   # manager.run()
    app.run(debug=True)


