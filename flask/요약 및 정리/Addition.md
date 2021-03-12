# Addition

추가적인 정보들을 정리해보았다. 

## 느린 데이터베이스 쿼리 로깅
```python
from flask_sqlalchemy import get_debug_queries

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config('FLASKY_SLOW_DB_QUERY_TIME'):
            current_app.logger.warning('Slow query: {}\nParameters: {}\nDuration: {:.6f}\nContext: {}\n'.format(query.statement, query.parameters, query.duration, query.context))
    return response
```
get_debug_queries() 함수는 기본적으로 디버그 모드에서만 가능한데, 안타깝게도 데이터베이스 성능 문제는 개발 중에는 거의 나타나지 않는다. 그렇기 때문에 제품화 단계에서 사용하는 것이 유용한데, 아래는 제품화 모드에서 데이터베이스 쿼리 성능을 볼 수 있도록 하는 설정이다.
```python
class Config:
    SQLALCHEMY_RECORD_QUERIES = True 
    FLASKY_DB_QUERY_TIMEOUT = 0.5 # 느린 쿼리의 기준값을 0.5로 설정
```

## 소스 코드 프로파일링
소스 코드 프로파일러는 애플리케이션의 가장 느린 부분을 찾는데 유용하다. 프로파일러는 실행중인 애플리케이션을 지속적으로 모니터링하고 호출되는 함수의 실행 시간을 기록한다. 또한 가장 느린 함수에 대해서 정보를 제공한다. 프로파일링은 계속 모니터링을 해야하기 때문에 배포할 때는 성능 저하로 사용되지 않는다. 즉 제품화 환경에서는 권장되지 않는다

```python
@manager.command
def profile(length=25, profile_dir=None):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)

    app.run()
```
python manage.py profile 명령어를 실행하면 콘솔에서 리퀘스트에 대한 프로파일러 통계를 보여준다. length 옵션은 가장 느린 함수를 갯수만큼 반환한다는 의미고, profile_dir 옵션은 프로파일 데이터를 디렉토리에 call graph를 포함하는 자세한 정보를 저장한다는 의미다. 

## 배포
애플리케이션이 제품화되어 서버에 설치될 때에는 데이터베이스 테이블을 생성하고 업데이트 해주어야 한다. 
따라서 간단한 커맨드로 데이터베이스를 생성 및 배포시 필요한 작업들을 수행할 수 있도록 한다.
```python
@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import Role, User

    upgrade()
    Role.insert_roles()
    User.add_self_follows()
```
### 제품화 과정 중의 에러 로깅
애플리케이션이 디버그 모드에서 실행될 때 Werkzeug의 인터랙티브 디버거는 에러가 발생할 때마다 스택 트레이스(stack trace)가 웹 페이지 나타나는데 제품화 배포에서는 사용할 수 없다. 그래서 우리는 그 에러를 로그 파일에 작성할 필요가 있다. 파이썬의 logger.Logger 클래스의 인스턴스를 애플리케이션 인스턴스의 app.logger에 붙인다. 이 로거는 디버그 모드에선 콘솔로, 제품화 모드에서는 추가한 로그로 저장한다. 심지어 이메일로 로그를 전달할 수도 있다.

```python
class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app):
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost = (cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr = cls.FLASKY_MAIL_SENDER,
            toaddr = [cls.FLASKY_ADMIN]
            subject = cls.FLASKY_MAIL_SUBJECT_PREFIX+ ' Application Error',
            credentials= credentials,
            secure = secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
```

python logger에 대해선 나중에 더 공부해보아야겠다.
