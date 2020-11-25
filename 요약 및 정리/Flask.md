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
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',form = form, name = session.get('name'))

```



### 메시지 렌더링하기

flash()를 호출하는 것만으로는 메시지를 출력하기에 충분하지 않다. 애플리케이션에서 사용되는 템플릿은 이러한 메세지를 렌더링해야 한다. 플라스크는 get_flashed_messages() 함수를 이용하여 템플릿에서 메시지를 추출하고 렌더링하도록 한다.

```python
#base.html
{% block content %}
<div class="container">
    {% for message in get_flashed_messages() %}
        <div class="alert alert-warning">
            <button type="button" class="close" data-dismiss="alert">&times;</button>
            {{ message }}
        </div>
    {% endfor %}
    {% block page_content %}{% endblock %}
</div>
{% endblock %}

```

## 10. 블루 프린트
애플리케이션 인스턴스를 팩토리 함수로 생성하면, 전역 변수가 아니기 때문에 app.route() 데코레이터를 쉽게 정의할 수 없다. 이러한 문제는 Blueprints를 사용하면 된다. 블루프린트는 app과 같은 기능을 가지고 있다. 그리고 블루프린트는 애플리케이션에 등록할 수 있는데, 등록될 때까지 휴면 상태다. 전역 변수로 정의된 블루프린트를 하나의 스크립트로된 애플리케이션과 거의 같은 방법으로 사용된다.

애플리케이션과 비슷하게, 블루프린트는 하나의 파일에 정의될 수도 있고 패키지를 사용하여 구조화할 수도 있다. 호환성을 높이려면 애플리케이션 패키지 내부에 서브 패키지가 블루프린트를 호스트하도록 생성하면 된다. 아래는 블루프린트를 생성하는 예제다

```python
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views. erros
```

Blueprint 클래스의 생성자는 두 개의 인수를 필요로 한다. 하나는 블루프린트 이름이고 다른 하나는 블루프린트가 위치한 모듈이나 패키지다. \_\_name\_\_ 변수를 사용하면 대부분의 경우 잘 작동한다.

라우트는 다른 스크립트에 정의한 후(app/main/views.py) 이 모듈들을 임포트하여 블루프린트와 연결하면된다. 원형의존성을 피하기 위해 모듈을 app/\_\_init__/py 아랫부분에 임포트해야 한다. views.py와 errors.py는 메인 블루프린트를 임포트해야 되기 때문이다. 