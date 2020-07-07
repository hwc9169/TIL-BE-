from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort

app = Flask(__name__)

@app.route('/')
def index():
    redirec = redirect('http://naver.com')
    return redirec
'''
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello %s!</h1>' % name
'''

@app.route('/user/<id>')
def get_user(id):
    if id == "howon":
        abort(404)
    return '<h1>Hello, %s!' %id

if __name__ == '__main__':
    app.run(debug=True)
