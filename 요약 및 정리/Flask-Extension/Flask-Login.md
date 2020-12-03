# 사용자 인증

## 1. 플라스크의 인증 확장

인증 확장

* Flask-Login : 로그인한 사용자를 위한 사용자 세션 관리
* Werkzeug : 패스워드 해싱과 검증
* itsdangerous : 암호화된 보안 토큰 생성과 검증



일반적인 목적의 확장

* Flask-Mail : 인증 관련 이메일 전송
* Flask-Bootstrap : HTML 템플릿
* Flask_WTF : 웹 폼

Flask-Login 확장은 구현해야할 4가지 메소드가 있다. 필요한 메소드를 정리해보았다.
| 메소드 | 설명|
|--------|-----|
|is_authenticated()|사용자가 인증되었다면 True를 아니면 False를 리턴|
|is_active()|사용자에게 로그인이 허용된다면 True 그렇지 않다면 불가능한 계정을 위해 값이 사용됬다는 의미로 False를 리턴|
|is_anonymous()| 일반적인 사용자에게 False 리턴|
|get_id()|사용자의 고유 인식자 리턴(유니코드 문자열로 인코딩됨)|

다행스럽게더 이 네 개의 메소드는 모델 클래스에서 메소드로 직접 구현할 필요없다. Flask-Login은 기본 구현된 UserMixin을 제공한다.

```python
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(64), primary_key=True)
    #...
```

flask-login 초기화
```python
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    #...
    login_manager.init_app(app)
    #...
```

LoginManager 인스턴스의 session_protection은 None, 'basic', 'strong' 이렇게 세 단계가 있다. 'strong'으로 설정하면 클라이언트의 IP와 브라우저의 에이전트가 변경될 때마다 로그아웃시킨다. login_view 속성은 로그인 페이지의 엔드 포인트를 설정한다. 로그인 라우트가 auth 블루프린트에 있다면 블루 프린트 앞에 'auth.'이라는 접두어가 필요하다.

마지막으로 Flask-Login은 사용자와 주어진 인식자를 로드하는 콜백 함수를 셋업하게 된다.

```python
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

### 라우트 보호
login_required 데코레이터를 사용하면 인증된 사용자만 액세스되도록 할 수 있다.
```python
from flask-login import login_required

@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'
```
인증되지 않은 사용자가 액세스된다면 Flask-Login은 사용자에게 로그인 페이지를 보여준다.

## 2. 패스워드 보안

데이터베이스에 사용자 패스워드를 저장할 때 중요한 점은 패스워드 자체를 저장하는 것이 아니라 해싱한 값을 저장하는 것 입니다.

그렇다면 우리는 패스워드를 쉽게 해싱하도록 해주는 Werkzeug 확장을 알아 보도록 해보겠습니다.



### 1. Werkzeug을 이용한 패스워드 해싱

Werkzeug 보안 모듈을 사용하면 보안 패스워드 해싱을 편하게 구현할 수 있습니다.

두 개의 함수는 각각 등록과 검증으로 사용합니다.

* generate_password_hash(password, method=pbkdf2:sha1, salt_length=8) 



* check_password_hash(hash, password) :  True가 리턴되면 패스워드가 올바르다는 의미입니다.

app/models.py : User모델에서 패스워드 해싱

```python
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.model):
    # ...
    password_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
       
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
```



__password()__ 메소드는 password라는 쓰기 전용 속성을 통해 구현됩니다. 이 속성이 설정되면 setter 메소드는 Werkzeug의 generate_password_hash() 함수를 호출하게 되고 이 결과를 self.password_hash() 필드에 작성합니다. 만약 password 속성을 읽으려고 하면 에러를 리턴하고 원래의 패스워드는 다시 해시로 복구되지 않습니다.

__verify_password()__ 메소드는 패스워드를 취하여 그 패스워드를 Werkzeug의 check_password_hash() 함수로 넘깁니다. 이 메소드가 True를 리턴하면, 패스워드가 올바르다는 뜻 입니다.


