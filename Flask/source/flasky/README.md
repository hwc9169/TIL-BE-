# 대규모 애플리케이션 구조

앞서 구현했던 하나의 스크립트 hello.py를 여러 모듈로 분할한 작업을 설명한 글 입니다.

## 01. 프로젝트 구조

| - flasky

​	| - app/

​		| - templates/

​		| - static/

​		| - main/

​			| - __ init __.py

​			| - errors.py

​			| - forms.py

​			| - views.py

​		| - __ init __.py

​		| - email.py

​		| - models.py

​	| - migrations/

​	| - tests/

​		| - __ init __.py

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



### 1. 애플리케이션 팩토리

애플리케이션을 테스트할 때 여러 테스트 환경을 설정할 필요가 있습니다. 이때 애플리케이션 인스턴스가 이미 생성되어 있다면 동적으로 설정 변경을 적용할 방법이 없다는 문제가 있습니다.

이 문제에 대한 해결책으로 애플리케이션을 팩토리 함수에서 생성하도록 합니다. 이 팩토리 함수는 스크립트에서 호출 되어 여러 애플리케이션 인스턴스를 다양한 환경에서 실행할 수 있게 됩니다.



app/__ init __.py

```python
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from Flask.source.flasky.config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
```

팩토리 함수이름은 create_app이고 인수로는 설정할 이름을 받습니다. 그리고 app.config 설정 오브젝트에서 사용 가능한 from_object() 메소드를 사용하여 설정값을 임포트한 후 init_app() 메소드로 초기화 합니다.

### 2. 블루프린트

런타임에 애플리케이션을 생성하면 app.route() 데코레이터는 팩토리 함수 create_app()이 실행된 이후에만 존재할 수 있습니다. 따라서 이전에 사용하던 방식은 너무 늦습니다.

플라스크에서는 블루프린트를 사용하여 더 나은 해결책을 제공한다. 블루프린트는 블루프린트와 관련된 라우트를 휴면 시켰다가 애플리케이션과 연결이 되면 라우트를 깨웁니다.

app/main/__ init __.py

```python
from flask import Blueprint

main = Blueprint('main', __name__)
from . import views, errors
```



블루프린트는 Blueprint 클래스의 오브젝트를 인스턴스화하여 생성합니다. 이 클래스는 두 개의 인수를 사용하는데, 하나는 블루프린트의 이름이고, 다른 하나는 블루 프린트가 위치하게 될 모듈이나 패키지입니다.

애플리케이션과 마찬가지로 __ name __ 변수를 사용하면 대부분의 경우 정상 작동됩니다. 이제 설정된 블루 프린트를 애플리케이션 인스턴스에 적용하겠습니다.



__블루프린트 등록__ :  app/__ init __.py

```python
def create_app(config_name):
    # ...
    
    from .main import main as blueprint
    app.register_blueprint(main_blueprint)
    
    return app
```



애플리케이션의 라우트는 app/main/views.py에 저장되고 에러 핸들러는 app/main/errors.py에 저장된다. 이 모듈들을 임포트하여 블루프린트에 연결시킵니다. 원형 의존성을 피하기 위해 모듈들을 app.__ init __.py의 아랫부분에 임포트 해야 한다는 점이 중요합니다. views.py와 errors.py는 메인 블루프린트를 임포트해야 하기 때문입니다.

app/main/errors.py

```python
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```



app/main/views.py

```python
from datetime import datetime
from flask import render_template
from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET','POST'])
def index():
    form = NameForm
    if form.validate_on_submit():
       	user = User.query.filter_by(username=form.name.data).first()
        if user is None:
			user = User(username=form.name.data)
        	db.session.add(user)
        	session['known'] = False
    	else:
        	session['known'] = True
    	session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known',False),
                           current_time=datatime.utcnow())
```

블루프린트 내에서 뷰 함수를 작성할 떄는 두가지 차이점이 있습니다.

* 라우트 데코레이터가 블루프린트로부터 온다(ex main.route)
* 블루프린트의 차이점은 플라스크가 블루프린트로부터 온 모든 종단점에 네임스페이스를 적용한다는 점입니다. 따라서 url_for()의 인자로 'main.index'가 오게 되는데 블루프린트 이름이 생략되어도 괜찮습니다.



## 04. 스크립트 런칭

manage.py 파일은 애플리케이션을 시작할 떄 사용됩니다.

```python
from .app import create_app, db
from .app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, Migrate

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
```



## 05. Requirements  파일

requirements.txt 파일은 애플리케이션의 정확한 버전 넘버를 포함한 모든 패키지 의존성을 기록합니다.

이것은 가상 환경의 경우 컴퓨터에서 다시 생성해야 하기 때문에 중요합니다. 



requirements 파일 생성

```python
pip freeze > requirements.txt
```



가상 환경을 requirement 파일에 따라 완벽히 복사하고 싶을 때는 새로운 가상 환경을 생성하고 다음과 같은 커맨드를 사용하면 됩니다.

```python
pip install -r requirements.txt
```

 

## 06. 유닛 테스트

unittest를 이용하여 두 개의 간단한 테스트를 정의해 보겠습니다.

```python
import unittest
from flask import current_app
from ..app import db,create_app

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context().pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
```

__setUp()__ 메소드는 각 애플리케이션 인스턴스에 대해 테스트 환경을 생성하게 됩니다. 먼저 테스트를 위해 설정된 애플리케이션을 생성하고 그 컨텍스트를 활성화 한다. 이 과정은 일반적인 리퀘스트처럼 테스트가 current_app을 액세서 하도록 해 줍니다.

__tearDown__() 메소드는 생성된 인스턴스를 삭제 합니다.

__test_app_exists()__ 메소드는 애플리케이션 인스턴스가 존재하는지를 확인 합니다.

__test_app_is_testing()__ 메소드는 애플리케이션이 테스트 설정 내에서 실행되는지를 확인한다.



유닛 테스트를 설정 했다면 이를 실행하기 위해 커스텀 커맨드를 manage.py 스크립트에 추가해야 합니다.

```python
@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
```



## 07. 데이터베이스 셋업

재구조화한 애플리케이션은 서로 다른 여러 가지 데이터베이스를 사용합니다.(디폴트 URL은 SQLite입니다.)

SQLite 데이터베이스 파일이름은 설정마다 각각다른데, 데이터베이스의 각 테이블은 새로운 데이터베이스를 위해 생성되어야 합니다.  Flask-Migrate를 사용하여 마이그레이션을 유지하도록 작업할 때 한개의 커맨드를 사용하여 데이터베이스 테이블을 최신 버전으로 생성하거나 업그레이드 할 수 있습니다.

```
python manage.py db upgrade
```

