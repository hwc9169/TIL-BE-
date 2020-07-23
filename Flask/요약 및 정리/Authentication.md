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

