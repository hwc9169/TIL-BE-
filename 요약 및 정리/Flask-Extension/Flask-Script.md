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

  