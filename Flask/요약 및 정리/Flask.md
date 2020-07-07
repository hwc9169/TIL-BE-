# Flask

"플라스크 웹 개발" 이라는 책을 읽고 내용을 정리 및 요약한 글 입니다.



## Object

뷰 함수에서는 사용 가능한 오브젝트를 생성해야 한다.

1. 리퀘스트 오브젝트(request object)

> 리퀘스트 오브젝트는 HTTP 리퀘스트를 캡슐화한다



## Context

뷰 함수가 필요하지 않은 인수를 갖는 것을 피하기 위해 임시적으로 오브젝트를 액세스할 수 있도록 한다.

밑은 각 컨텍스트에서 사용되는 변수들이다.

* 어플리케이션 컨텍스트

current_app : 활성화된 애플리케이션을 위한 애플리케이션 인스턴스

g : 리퀘스트를 처리하는 동안 애플리케이션이 임시 스토리지를 사용할 수 있는 오브젝트이다.  이 변수는 각 리퀘스트에 따라 리셋된다.



* 리퀘스트 컨텍스트

request : 클라이언트가 송신한 HTTP request를 캡슐화하는 리퀘스트 오브젝트

session : 애플리케이션이 리퀘스트 사이의 'remembered' 값들을 저장하는데 사용하는 딕셔너리



## Request Hook

리퀘스트를 처리하기 전후에 실행되는 코드다. 예를 들어 리퀘스트의 시작 부분에서 데이터베이스와 커넥션을 생성하거나 사용자를 인증해야 하는 경우가 있다. (GO의 미들웨어 개념과 유사한 것 같다)

리퀘스트 후크는 데코레이터를 사용하여 구현하는데 다음은 플라스크에서 제공하는 4개의 후크다.

* before_first_request :첫 번쨰 리퀘스트가 처리되기 전에 실행한다.
* before_request : 각 리퀘스트가 처리되기 전에 실행한다.
* after_request : 각 리퀘스트가 처리된 후에 실행한다.(예외가 발생하면 실행 되지 않는다)
* teardown_request : 각 리퀘스트가 처리된 후에 실행한다.(예외가 발생해도 실행된다.)

리퀘스트 후크 함수와 뷰 함수 사이에 데이터를 공유하기 위한 패턴은 g 컨텍스트 전역 변수를 사용하면 된다.

예를 들어, before_request 핸들러는 데이터베이스에서 사용자 정보를 로드하여 g.user에 저장한다.



## Request / Response

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



## Redirect

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



## abort

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



















