# 대규모 애플리케이션 

대규모 애플리케이션을 글로 설명한 글 입니다.

## 01. 프로젝트 구조

| - flasky

​	| - app/

​		| - templates/

​		| - static/

​		| - main/

​			| - __init__.py

​			| - errors.py

​			| - forms.py

​			| - views.py

​		| - __init__.py

​		| - email.py

​		| - models.py

​	| - migrations/

​	| - tests/

​		| - __init__.py

​		| - test*.py

​	| - venv/

​	| - requirements.txt

​	| - config.py

​	| - manage.py



* 플라스크 애플리케이션은 일반적으로 app이라는 패키지 안에 존재한다.
* migrations 폴더는 데이터베이스 마이그레이션 스크립트를 포함한다.
* 유닛 테스트는 tests 패키지에 작성된다.
* venv 폴더는 파이썬 가상 환경을 포함한다.



네 개의 새로운 파일

* requirements.txt는 패키지 의존성을 리스트하여 서로 다른 컴퓨터에서 인식할 수 있는 가상 환경을 재생성하기 편리하다.
* config.py는 설정값을 저장한다.
* manage.py는 애플리케이션과 다른 애플리케이션의 태스크를 실행한다.





## 02. 설정 옵션

hello.py에서 사용된 딕셔너리 형태의 설정 대신에 설정 클래스의 계층 구조 형태가 사용될 수 있다.



- config.py

```python
import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@xample.com>'
    FLASKY_ADMIN = os.environ.get("FLASKY_ADMIN")

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USER_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                                'data.sqlite')
config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}


```



## 03. 애플리케이션 패키지

애플리케이션 패키지는 애플리케이션의 코드, 템플릿, 정적 파일이 위치하는 곳이다.

보통 간단하게 app이라고 하지만 필요한 경우 애플리케이션의 특성에 맞는 이름으로 생성할 수 있다.

templates와 static 폴더는 애플리케이션 패키지의 일부로 app 안으로 이동하게 된다.

데이터베이스 모델과 이메일 역시 패키지 안에 존재한다. 모듈은 각각 app/models.py, app/email.py

라는 이름이다.