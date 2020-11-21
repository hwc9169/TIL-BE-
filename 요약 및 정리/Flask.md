# 01. Flask

"플라스크 웹 개발" 이라는 책을 읽고 내용을 정리 및 요약한 글 입니다.



## 1. Object

뷰 함수에서는 사용 가능한 오브젝트를 생성해야 한다.

1. 리퀘스트 오브젝트(request object)

> 리퀘스트 오브젝트는 HTTP 리퀘스트를 캡슐화한다



## 2. Context

뷰 함수가 필요하지 않은 인수를 갖는 것을 피하기 위해 임시적으로 오브젝트를 액세스할 수 있도록 한다.

밑은 각 컨텍스트에서 사용되는 변수들이다.

* 어플리케이션 컨텍스트

current_app : 활성화된 애플리케이션을 위한 애플리케이션 인스턴스

g : 리퀘스트를 처리하는 동안 애플리케이션이 임시 스토리지를 사용할 수 있는 오브젝트이다.  이 변수는 각 리퀘스트에 따라 리셋된다.



* 리퀘스트 컨텍스트

request : 클라이언트가 송신한 HTTP request를 캡슐화하는 리퀘스트 오브젝트

session : 애플리케이션이 리퀘스트 사이의 'remembered' 값들을 저장하는데 사용하는 딕셔너리



## 3. Request Hook

리퀘스트를 처리하기 전후에 실행되는 코드다. 예를 들어 리퀘스트의 시작 부분에서 데이터베이스와 커넥션을 생성하거나 사용자를 인증해야 하는 경우가 있다. (GO의 미들웨어 개념과 유사한 것 같다)

리퀘스트 후크는 데코레이터를 사용하여 구현하는데 다음은 플라스크에서 제공하는 4개의 후크다.

* before_first_request :첫 번쨰 리퀘스트가 처리되기 전에 실행한다.
* before_request : 각 리퀘스트가 처리되기 전에 실행한다.
* after_request : 각 리퀘스트가 처리된 후에 실행한다.(예외가 발생하면 실행 되지 않는다)
* teardown_request : 각 리퀘스트가 처리된 후에 실행한다.(예외가 발생해도 실행된다.)

리퀘스트 후크 함수와 뷰 함수 사이에 데이터를 공유하기 위한 패턴은 g 컨텍스트 전역 변수를 사용하면 된다.

예를 들어, before_request 핸들러는 데이터베이스에서 사용자 정보를 로드하여 g.user에 저장한다.



## 4. Request / Response

router를 통해 Request의 URL을 받아 이에 적절한 뷰 함수에 연결 하여야한다.

이는 파이썬의 데코레이터로 구현 가능하다.

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'
@app.route('user/<name>')
	return  '<h1>Hello, %s!</h1>'%name
```

위의 코드를 보면 return 값으로 문자열을 주었다. 이는 불안정한 코드이며, 쿠키 값과 같은 response 헤더를 설정하기 힘들다.

그래서 response객체를 이용하는 것이 현명하다.  make_response() 함수는 response 객체를 반환한다.

아래는 response객체를 이용하여 쿠키 값을 설정했다.

```python
from flask import Flask
from flask import make_response
app = Flask(__name__)

@app.route('/')
def index():
    response = make_response('<h1>This document carries aa cookie!</h1>')
    response.set_cookie('answer','42')
    return response
    
```



## 5. Redirect

리다이렉트 타입의 응답의 특징은 다음과 같다.

* 페이지 도큐먼트를 포함하지 않는다
* 새로운 페이지를 로드하는 새 URL을 브라우저에 전달한다
* 302 응답 상태 코드와 Location 헤더에 리다이렉트할 URL을 사용하여 리다이렉트 상태를 알린다

리다이렉트는 Response 오브젝트로도 생성되기도 하지만 주로 redirect() 헬퍼 함수를 사용한다

```python
from flask import redirect

@app.route('/')
def index():
    rdt = redirect('http://naver.com')
    return rdt
```



## 6. abort

다른 특별한 응답은 abort 함수가 사용되는 경우다.

이 함수는 에러 핸들링을 위해 사용된다.

```python
from flask import abort

@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
   	if not user:
        abort(404)
        return '<h1>Hello, %s!' %user.name
```



## 7. Template / Render

템플릿은 리퀘스트에서 인식 가능한 동적 파트에 대한 변수들을 포함한 응답 텍스트 파일이다.

변수들을 실제 값으로 바꾸는 프로세스와 최종 응답 문자열을 리턴하는 프로세스를 렌더링이라 한다.

플라스크는 Jinja2라는 강력한 템플릿 엔진을 사용한다.

* hello.py

```python
from flask import Flask, render_template

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)
```

* user.html

  ```html
  <h1>
      Hello, {{name}}!
  </h1>
  ```

### 템플릿 제어 구조

Jinja2는 몇 가지 제어 문자를 제공한다 이 제어 문자는 템플릿의 흐름을 변경하는 데 사용된다.

* if 문

  ```html
  {% if user %}
  	Hello, {{name}}!
  {% else %}
  	Hello, Stranger!
  {% endif %}
  ```

* for 문

  ```html
  <ul>
  	{% for comment in comments %}
  		<li>{{comment}}</li>
      {% endfor %}
  </ul>	
  ```

  

* macro

  함수와 비슷한 기능을 한다.

  ```html
  {% macro render_comment(comment) %}
  	<li>comment</li>
  {% endmacro %}
  ```

  

* import macro

  매크로를 재사용하기 위해서는 독립적인 파일에 저장해 두고 필요할 떄 템플릿에 임포트한다.

  ```html
  {% import 'macro.html' as macro %}
  <ul>
  	{% for comment in comments %}
  		{{macro.render_comment(comment)}}
  	{% endfor %}
  </Ul>
  ```

  

* include macro

  여러 위치에 반복되는 템플릿 코드는 별도의 파일에 저장하고 필요할 때 인클루드하여 반복을 피한다.

  ```html
  {% include 'common.html' %}
  ```



* template 상속

  파이썬의 클래스 상속과 비슷하며 import와 include와 같이 코드 재사용의 강력한 기능을 제공한다

  > base 템플릿을 정의했다.
  
  ```html
<html>
  <head>
      {% block head %}
      <title>{% block title %}{% endblock %} - My Application</title>
      {% endblock %}
  </head>
  <body>
      {% block body %}
      {% endblock %}
  </body>
  </html>
  ```
  



## 8. Error 처리

플라스크에서는 에러에 대하여 커스텀 핸들러를 제공한다.

일반적인 라우터와 마찬가지로 템플릿에 기반을 둔 커스텀 에러 페이지를 정의한다.



```python
#클라이언트가 없는 경로를 요청함

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

#처리하지 못하는 예외 발생
@app.errorhandler(500):
def internal_server_error(e):
	return render_template('505.html'),505
```



## 9. 메시지 보내기

로그인에 실패했을 때의 경우 비밀번호가 틀렸다는 메시지를 사용자에게 보낼 필요가 있다. 

이와 같이 메시지를 보내고 싶을 때 flask에는 flash() 함수를 사용하면 된다.

```python
@app.route('/index', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash("You have changed your name")
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html',form = form, name = session.get('name'), email = session.get('email'))

```



### 메시지 렌더링하기

flash()를 호출하는 것만으로는 메시지를 출력하기에 충분하지 않다. 애플리케이션에서 사용되는 템플릿은 이러한 메세지를 렌더링해야 한다. 플라스크는 get_flashed_messages() 함수를 이용하여 템플릿에서 메시지를 추출하고 렌더링하도록 한다.

```python
#base.html
{% block content %}

```


# 02. Flask 확장

플라스크는 확장할 수 있도록 설계되었다. 데이터베이스 사용자 인증 등과 같은 기능을 확장 가능하다.

플라스크를 위해 특별히 개발된 확장은 flask_<네임스페이스>에 나타나 있다.



## 1. Flask-Script 확장

Flask-Script는 플라스크 애플리케이션에 커맨드 라인 parser를 추가하는 플라스크 확장이다. 일반적인 목적의 옵션으로 패키징되며 커스텀 커맨드도 제공한다.

Manager는 클래스이다. Manager 클래스를 익스포트 하는데 이것은 flask_script에서 임포트된다.

```python
from flask_script import Manager
from flask import Flask

app = Flask(__name__)
manager = Manager(app)

if __name__=='__main__':
    manager.run()
```



Manager의 메인 클래스의 인스턴스는 어플리케이션 인스턴스(app)를 생성자에 인수로 넘김으로 초기화된다.

그리고 생성된 오브젝트는 각 확장에 따라 적절하게 사용된다.

이 경우 서버 스타트업은 manager.run()을 통해 라우트되며 커맨드 라인은 파싱된다.



또 유용한 기능으로는 스크립트에 자동으로 임포트 하도록 할 수 있다는 점이다. 

```python
def make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command('shell', Shell(make_context=make_shell_context))
```



* shell : 애플리케이션의 컨텍스트에서 파이썬 쉘 세션을 시작한다

* runserver : 웹 서버를 실행한다

  ```
  python hello.py runserver	
  ```

  



## 2. Flask-Bootstrap 확장

bootstrap은 트위터에서 제공하는 오픈 소스 프레임워크이며 매력적인 웹 페이지를 생성할 수 있도록 사용자 인터페이스 컴포넌트를 제공한다.

부트스트랩과 어플리케이션을 통합하는 가장 확실한 방법은 템플릿에 모든 변경 사항들을 만들어 두는 것이다.

더 간단한 방법은 Flask-Bootstrap이라는 Flask확장을 사용한다.

```python
from flask_bootstrap import Bootstrap
```

> Flask-Bootstrap의 base 템플릿을 상속한 예제

```html

{% extends "bootstrap/base.html" %}
{% block title %} Flasky {% endblock %}
{% block navbar %}
<div class="navbar navbar-inverse" role="navigation">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle"
            data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">Flasky</a>
        </div>
        <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li><a href="/">Home</a></li>
            </ul>
        </div>
    </div>
</div>
{% block content %}
<div class="container">
    <div class="page-header">
        <h1>Hello, {{name}}!</h1>
    </div>
</div>
{% endblock %}
```



## 3. Flask-WTF

플라스크는 폼을 처리하기 위해서 Flask-WTF 확장을 사용하여 처리한다.

Flask-WTF를 사용할 때 각 웹 폼은 Form 클래스로부터 상속한 클래스에 의해  표현된다.

이 클래스는 폼에 있는 필드의 리스트를 정의하는데 이는 각각 오브젝트로 표현된다.

각 오브젝트는 하나 이상의 검증자가 있어서 사용자가 서브밋한 입력값이 올바른지 체크할 수 있다. 



```python
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')
```



WTForms에서 지원하는 표준 HTML 필드의 리스트 

| 필드타입      | 설명                                      |
| ------------- | ----------------------------------------- |
| StringField   | 텍스트 필드                               |
| TextAreaField | 다중 라인 텍스트 필드                     |
| PasswordField | 패스워드 텍스트 필드                      |
| Hiddenfield   | 숨겨진 텍스트 필드                        |
| DateField     | 주어진 포맷에서 datetime.date 값을 받는다 |
| BooleanField  | True와 False 값을 갖는 체크박스           |
| FileField     | 파일 업로드 필드                          |
| SubmitField   | 폼 서브미션 버튼                          |
| IntegerField  | 정수값을 받는 텍스트 필드                 |



| 검증자      | 설명                                                         |
| ----------- | ------------------------------------------------------------ |
| Email       | 이메일 주소를 검증                                           |
| EqualTo     | 두 필드의 값을 비교, 확인하기 위해 패스워드를 두번 입력하도록 할때 유용 |
| Length      | 문자열의 길이 검증                                           |
| NumberRange | 입력한 값이 숫자와 알파벳 범위인지를 검증                    |
| Optional    | 필드에서 빈 입력을 허용하고, 추가한 검증자를 건너뛴다        |
| Required    | 필드에서 빈 입력을 허용하지 않는다                           |
| URL         | URL을 검증                                                   |
| Regexp      | 정규표현식에 대한 입력을 검증                                |


### 크로스-사이트 리퀘스트 위조(CSRF) 보호

기본적으로 Flask-WTF는 크로스 사이트 리퀘스트 위조(CSRF) 공격으로부터 모든 폼을 보호한다.
CSRF 공격은 악의적 웹사이트에서 희생자가 로그인한 다른 웹사이트로 리퀘스트를 전송할 때 일어난다.
CSRF 보호를 구현하기위해 Flask-WTF는 암호화 키로 토큰을 생성하여 리퀘스트 인증을 검증하는 데 사용한다. 
아래 예제는 암호화 키를 설정하는 방법이다.

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
```



추가적으로 중요한 개념이 있는데 app.config 딕셔너리는 프레임워크나 확장 또는 애플리케이션 자체에서 사용된다. app.config 딕셔너리는 설정 변수들을 저장하는 공간이다. 설정 변수들은 딕셔너리 문법에 따라 app.config 오브젝트에 추가된다. 심지어 app.config(설정 오브젝트)는 파일이나 환경에서 설정값을 불러오는 메소드도 가지고 있다.

## 4. Flask-SQLAlchemy

Flask-SQLAlchemy는 플라스크 애플리케이션 안에 있는 SQLAlchemy의 사용을 간단하게 하는 플라스크 확장이다. SQLAlchemy는 여러 데이터베이스 백엔드를 지원하는 강력한 관계형 데이터베이스 프레임워크다.



> SQLAlchemy에 관한 사항은 내용이 많은 지라 'Flask-Database' 게시물에 따로 작성해 두었다. 



## 5. Flask-Mail 확장

Flask-Mali 확장자는 smtplib를 래퍼하여 플라스크에서 쉽게 사용되도록 통합되어 있다.

파이썬 표준 라이브러리에서 제공하는 smtplib 패키지는 플라스크 애플리케이션에서 이메일을 전송하는 데 사용된다. (Simple Mail Transfer Protocol, SMTP , 메일 전송 프로토콜)



SMTP서버 설정키

| 키            | 기본값    | 설MAI                                  |
| ------------- | --------- | -------------------------------------- |
| MAIL_HOSTNAME | localhost | 호스트 이름 혹은 이메일 서버의  IP주소 |
| MAIL_PORT     | 25        | 이메일 서버의 포트                     |
| MAIL_USE_TLS  | False     | 전송 레이어 보안(TLS)의 보안 활성화    |
| MAIL_UEE_SSL  | False     | 보안 소켓 레이어(SSL)의 보안 활성화    |
| MAIL_USERNAME | None      | 메일 계정의 사용자이름                 |
| MAIL_PASSWORD | None      | 메일 계정의 패스워드                   |

* 설정을 하지않고 서버에 연결하면 localhost의 25번 포트에 사용자 인증 없이 이메일을 전송한다.



외부 SMTP서버 연결

```python
import os
​```
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
```



Flask-Mail 초기화  및 이메일 전송

```python
from flask_mail import Mail
​```

mail = Mail(app)

from flask_mail import Message

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    #Message(title, sender, recipient)
    
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    mail.send(msg)
```



## 6. Flask_Moment 확장

웹 애플리케이션에서 날짜와 시간을 처리할 때 사용자가 전 세계에서 사용한다면 서로 다른 시간대를 사용하기 때문에 처리가 복잡해진다. 서버는 각 사용자의 위치와 무관한 일정한 시간 단위인 협정세계시(Coordinated Universal Time, UTC) 를 사용한다. 그러나 사용자는 UTC로 표현된 시간이 이해하기 힘들기 때문에 자신의 거주 위치에 맞는 지역 시간으로 표현하여야 한다. Flask_Moment 확장은 브라우저에서 시간과 날짜를 렌더링하도록 하는 moment.js와 Jinja2 템플릿이 통합된 플라스크 애플리케이션용 확장이다. 

Flask-Moment 초기화

```python
form flask_moment import Moment
moment = Moment(app)
```

Flask-Moment는 moment.js 외에도 jquery.js가 필요하다. 이 두 라이브러리는 HTML 문서 어디에 위치해도 상관없다. 확장으로 제공되는 헬퍼 함수를 통해 사용될 수도 있다. 이 헬퍼 함수는 콘텐트 딜리버리 네트워크(Content Delivery Network, CDN)에서 위의 두 라이브러리의 테스트된 버전을  참조한다. 부트스트랩은 이미 jquery.js를 포함하고 있기 때문에, moment.js만 추가하면 된다. 

moment.js 라이브러리 임포트

```html
{% block scrips %}
{{ super() }}
{{ moment.include_moment()}}
{% endblock %}
```



타임스탬프를 사용하기 위해 Flask-Moment는  moment 클래스를 생성한다.(이는 템플릿에서도 사용 가능하다.)  그렇다면 예제를 바로 살펴봅시다.

flask-moment 사용 예제, hello.py: datetime 변수 추가

```python
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())
```

flask-moment 사용 예제, templates/index.html: Flask-Moment를 이용한 타임스탬프 랜더링

```html
{% extends "base.html" %}
{% block page_content %}
	<p>The local Date and time is {{ moment(current_time).format('LLL') }}.</p>
	<p>That was {{ moment(current_time).fromNow(refresh=True) }}</p>
{% endblock %}
```

format('LLL') 포맷은 클라이언트 컴퓨터에 설정된 시간대와 위치에 따라 날짜와 시간을 랜더링하고,
fromNow() 랜더링 스타일은 상대 타임스탬프를 랜더링하고 넘겨진 시간에 따라 자동을 리프레시한다. 





