# SQLAlchemy

Flask에는 Database를 쉽게 다루도록 확장이 존재합니다. 이 중 가장 유명한 SQLAlchemy에 대해서 설명합니다.

*  ORM(Object Relational Mapping)로 상위 레벨 오브젝트-기반 오퍼레이션을 데이터베이스 명령어로 변경하도록 한다.

ORM덕분에 파이썬의 SQLAlchemy을 다룰줄만 알면 서로 다른 문법을 가진 데이터베이스 모두를 컨트롤 할 수 있게됩니다.



* database URL

| 데이터베이스 엔진 | URL                                           |
| ----------------- | --------------------------------------------- |
| MySQL             | mysql://username:password@hostname/database   |
| Postgre           | postgre://username:password@hostname/database |
| SQLite(리눅스)    | sqlite:////absolute/path/to/database          |
| SQLite(윈도우)    | sqlite:///c:/absolute/path/to/database        |



* 일반적인 SQLAlchemy 쿼리 필터

| 옵션        | 설명                                                         |
| ----------- | ------------------------------------------------------------ |
| filter()    | 원래 쿼리에 추가 필터를 더한 새로운 쿼리를 리턴한다.        |
| filter_by() | 원래 쿼리에 추가된 동일한 필터를 더한 새로운 쿼리를 리턴한다. |
| limit()     | 원래 쿼리의 결과 수를 주어진 수만큼 제한한다.                |
| offset()    | 원래 쿼리의 결과의 리스트에 옵셋을 적용하는 새로운 쿼리를 리턴한다. |
| order_by()  | 원래 쿼리의 결과를 정렬한다.                                 |
| group_by()  | 원래 쿼리의 결과를 그룹화한다.                               |



* 일반적인 SQLAlchemy 쿼리 실행자

| 옵션           | 설명                                                         |
| -------------- | ------------------------------------------------------------ |
| all()          | 쿼리의 결과를 모두 리스트로 리턴                             |
| first()        | 쿼리의 첫 번째 결과를 리턴하거나 결과가 없다면 None을 리턴   |
| first_or_404() | 쿼리의 첫 번째 결과를 리턴하거나 결과가 없다면 404 에러를 전송 |
| get()          | 주어진 주요키에 매칭하는 행을 리턴하거나 결과가 없다면 None을 리턴 |
| get_or_404()   | 주어진 주요키에 매칭하는 행을 리턴하거나 결과가 없다면 404 에러를 전송 |
| count()        | 쿼리의 결과 카운트 리턴ㄴ                                    |
| paginate()     | 결과의 특정 영역을 포함하는 Pagination 오브젝트 리턴         |



## 1. 기본 사용법

1. db 객체 생성

```python
from flask_sqlalchmey import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False #True로 설정시 각 리퀘스트 끝에 데이터베이스의 견경을 자동 커밋한다.
app.config['SECRET_KEY'] = 'hard to guess string'

db = SQLAlchemy(app)
```



2. 데이터베이스 모델 작성

```python
class Role(db.Model):
    __tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    user = db.relationship('User',backref='role' lazy='dynamic')
    
    def __repr__(self):
        return '<Role %r>' %roles.username
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
		return '<User %r>' %self.username
```



3. 데이터베이스 테이블 생성

```python
from hello import db,Role, User

db.create_all() #db 생성

admin_role = Role(name='Admin')
mod_role = Role(name='Moderate')
user_role = Role(name='User')

user_john = User(username='john', role=admin_role)
user_susan = User(username='susan', role=user_role)
user_david = User(username='david', role=user_role)

db.session.add_all([admin_role,mod_role,user_role,user_john,user_susan,user_david])
db.session.commit()
```


4. 관계
```python
class Role(db.Model):
    users = db.relationship('User', backref='role')

class User(db.Model):
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
```
db.relationship의 경우 외래키로는 어떤 열을 사용할지 결정할 수 없는 상황이 발생할 수 있다. 예를 들어 User 모델이 Role 외래키로 정의된 두 개의 열을 갖는다면, SQLAlchemy는 두 개 중 어떤 것을 사용할지 알지 못한다. 이런 경우  db.relationship()에 옵션을 사용하면 된다. 

일반적인 설정 옵션
| 옵션 이름 | 설명                          |
|-----------|------------------------------|
|backref    |백 레퍼런스 추가               |
|primaryjoin|두 모델 사이의 join 조건을 설정 |
|lazy|관계된 아이템이 로드되는 방식을 설정한다. select(첫번째 액세스시 아이템 로드), immediate(오브젝트 로드시 아이템 로드), joined(조인으로 즉시 로드), subquery(서브쿼리로 즉시 로드), noload(절대 로드되지 않음), dynamic(아이템이 아니라 쿼리가 로드됨)|
|uselist|False로 설정하면 리스트 대신 스칼라를 사용한다|
|order_by|아이템 사용되는 순서 결정|
|secondary|다대다 관계에서 관계 테이블의 이름 설정|
|secondaryjoin|SQLAlchemy가 결정하지 못할 때 두 번째 조인 설정|


5. 쿼리 실행

```python
User.query.all()
#[<User 'susan'>, <User 'david'>, <User 'john'>]

User.query.filter_by(role=user_role).all()
#[<User 'susan'>, <User 'david'>]

user_role.user.filter_by(name='susan'),first()
# <User 'susan'>
```
 filter_by와 같은 필터는 쿼리 오브젝트(user.query)에서 호출되며 새로 정의된 쿼리를 리턴한다.
 다중 필터는 설정한 만큼 순차적으로 호출하여 쿼리를 반환한다.


5. 행 수정 및 삭제

```python
#수정
admin_role.name = 'Administrator'
db.session.add(admin_role)
db.session.commit()

#삭제
db.session.delete(mod_role)
db.session.commit()
```



## 2.파이썬 쉘 통합

쉘 세션이 시작될 때마다 데이터베이스 인스턴스와 모델을 임포트하는 거은 상당히 귀찮다.

이를 피하기위해 Flask-Script의 쉘 커맨드는 특정 오브젝트를 자동으로 임포트하게 설정할 수 있다.



* 쉘 컨텍스트 추가	

```python
from flask_script import manager, Shell

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__=='__main__':
	manager.run()
```



## 3. Flask-Migrate

Flask-SQLAlchemy는 데이터베이스 테이블이 존재하지 않을 떄만 데이터베이스 테이블을 생성한다.

따라서 테이블을 업데이트하는 유일한 방법은 이전의 테이블을 삭제해야한다.

더 좋은 해결책은 데이터베이스 마이그레이션 프레임워크를 사용하는 것이다.

이는 데이터베이스 스키마의 변경을 추적하여 변경 사항을 데이터베이스에 적용한다.

Flask-Migrate확장은 Flask-Script 커맨드를 통해 모든 오퍼레이션을 제공하기 위해 Flask-Script와 통합한다.

 

```python
from flask_migrate import Migrate, MigrateCommand
migrate = Migrate(app,db)

manager.add_command('db', MigrateCommand)
#Flask-Migrate는 Flask-Script의 manager 오브젝트에 연결되어있는 MigrateCommand 클래스를 보여준다.
#이 예제에서 커맨드는 db를 사용한다

>>>python hello.py db init
#데이터베이스 마이그레이션이 유지되기 전에 먼저 init 서브커맨드를 사용하여 마이그레이션 저장소를 생성해야 된다

>>>python hello.py db migrate -m "initial migration"
#자동 마이그레이션 스크립트 생성

>>>python hello.py db updata
#데이터베이스 업데이트	
```





