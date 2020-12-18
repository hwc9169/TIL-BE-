# Test
구지 귀찮게 코드량을 더 늘리는 유닛 테스트를 해야 하는 이유는 세 가지가 있다.
1. 유닛 테스트는 새로운 기능을 구현했을 때 새로운 코드가 원하는 대로 동작하는 것을 확인하는데 사용된다.
2. 자동화된 테스트는 오히려 수동으로하는 것 보다 시간과 노력을 절약해 준다.
3. 새로운 기능으로 인해 애플리케이션의 동작이 달라질 수 있다. 모든 유닛 테스트는 기존 코드가 회귀되지 않음을 보장한다. 다른 말로 하면, 유닛 테스트가 성공했다는 말은 새 변경 사항이 기존 코드에 영향을 주지 않는다는 말이다. ㅊ 

## Unittest
unittest는 플라스크를 테스트하기위해 사용되는 라이브러리다. unittest를 사용할 때는 unittest.TestCase를 상속하는 클래스를 만들어야한다. 그리고 각 메소드는 'test_'로 시작되어야한다.

```python
from app import create_app, db
from flask import current_app
import unittest

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app =create_app('testing')
        self.app_context = self.app.app_context()  
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
```

setUp() 메소드와 tearDown() 메소드는 unittest.TestCase 메소드를 오버라이딩한 것으로 각각은 테스트를 시작하기 전, 시작한 후에 실행된다. 테스트를 실행하면 순서는 다음과 같다.

1. setUp()
2. test_app_exists()
3. tearDown()
4. setUp()
5. test_app_is_testing()
6. tearDown()

manage.py를 이용하여 테스트하는 코드다. 테스트 코드를 탐색은 TestLoader().discover()에 구현되어 있다. 또한 실행은 TextTestRunner 객체의 run() 메서드를 사용하면 된다.

- unittest에 포함된 주요 개념
    - TestCase: unittest 프레임 워크의 테스트 기본 단위
    - Fixture: 
        - 테스트 함수 전과 후에 실행
        - 테스트 전에 테스트 환경을 체크
        - 테스트 전에 데이터베이스 테이블을 만들거나, 테스트 후 리소스 정리하는데 사용
    - assertion:
        - unittest가 테스트 통과 여부를 결정
        - bool, 객체, 예외 등 다양한 점검 가능
        - assertion이 실패하면 테스트 함수가 실해

### unittest 모듈 사용
- unittest.TestCase 클래스를 상속
- test_ 로 시작하는 메소드는 모두 테스트 메솓
- test_run() 메소드는 실행 여부만 판별
- unittest.main()로 테스트 수행

``` python 
@manager.command
def test():
    """Run the unit test"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__=='__main__':
    manager.run()   
```

## 코드 커버리지 리포트
Test Suite(테스트 스위트란 테스트 케이스들을 하나로 묶어 두는 것)를 가지는 것은 중요하지만, 그것이 어떻게 사용할 때 유용한지 혹은 악용될 소지가 없는지 알아야 한다. 코드 커버리지 툴은 유닛 테스트가 애플리케이션을 얼마나 커버할 수 있는지 측정해준다. 즉 애플리케이션 코드의 테스트되지 않은 부분을 알려준다. 
이 툴은 커맨드 라인 스크립트로 동작한다. 그러나 프로그래밍해서 시작할 수도 있다. manage.py 런처 스크립트 안에 통합 커버리지 메트릭스를 얻어보자

```python
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage 
    COV = coverage.coverage(branch=True, include='app/*)
    COV.start()

#...

@manager.command
def test(coverage=False);
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable]+sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV;
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file;//%s/index.html' % covdir)
        COV.erase()
```

여기서 coverage.coverage() 함수는 커버리지 엔진을 시작한다. branch=True 옵션은 브랜치 커버리지 분석을 가능하게 한다. 또한 실행 코드 라인을 추적하기 위해 True, False를 갖는 모든 조건을 실행할지의 여부를 체크한다. include 옵션은 커버리지 분석 범위를 제한한다.include 옵션이 없으면 가상 환경에 설치된 모든 확장이 커버리지 리포트에 포함된다. 다음 명령어를 실행하여 반환되는 리포트를 보자
```python manage.py test --coverage```

## 플라스크 테스트 클라이언트 
### 웹 애플리케이션 테스트
데이터베이스 모델에 비해 다른 부분들은 쉽게 테스트할 수 없다. 뷰 함수, 폼, 템플릿에 적용 가능한 향상된 테스트 정책을 알아보자.
애플리케이션 코드는 애플리케이션의 환경과 매우 의존적이다. 예를 들어 뷰 함수는 request나 session, g와 같이 플라스크 컨텍스트를 전역적으로 액세스해야한다.
또한 POST 리퀘스트는 폼 데이터와 사용자 로그인이 필요하다. 즉 뷰 함수는 리퀘스트의 컨텍스트와 실행 중인 애플리케이션 내에서만 동작한다는 것이다. 
이에 대비하여 플라스크는 테스트 클라이언트를 제공한다. 테스트 클라이언트는 웹 서버에서 실행중인 애플리케이션의 환경을 그대로 복사하여 테스트 할 수 있도록 한다. 테스틑 클라이언트는 리퀘스트를 전송할 수도 있다.뷰 함수는 테스트 클라이언트의 리퀘스트를 수신하고 적절한 뷰를 라우트한 후에 응답을 한다. 뷰 함수의 응답은 테스트로 전달되고 그 값이 올바른지 체크할 수 있다.
```python
class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push():
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)    

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('Stranger' in response.get_data(as_text=True))
```

테스트 케이스에 추가된 self.client 인스턴스 변수는 플라크스 테스트 칼라이언트 오브젝트다. 이 오브젝트는 user_cookies 옵션을 활성화한 상태로 생성될 때, 브라우저처럼 쿠키를 사용하여 리퀘스트 간의 컨텍스트를 기억할 수 있다. 이 옵션은 사용자 세션을 가능하게하여 로그인 로그아웃에서 필요하다.

위의 test_home_page() 예제를 보자. 테스트 클라이언트의 get() 메소드의 리턴값은 뷰 함수의 Response 오브젝트다. 테스트의 성공 여부를 알기 위해서 response.get_data()를 통해 본문에 Stranger가 있는지 검사한다. 여기서 중요한 점은 get_data()는 기본값으로 바이트 배열을 리턴하는데 as_text 옵션을 True 하면 유니코드 문자열을 받을 수 있다. 

post() 메소드의 경우는 Flask-WTF를 사용한 폼인 경우 CSRF 토큰을 함께 보내야하므로 설정에서 CSRF 보호를 비활성화로 해 두는 것이 좋다.
```python
class TestingConfig(config):
    #...
    WTF_CSRF_ENABLED = False
 ```

### 웹 서비스 테스트
위에서 실행한 테스트는 웹 애플리케이션을 위한 테스트 코드다. 웹 서비스, 즉 RESTful API를 위한 테스트도 예제를 통해 익숙해 보자.
여기서 중요한 것은 API는 쿠키를 사용하지 않기 대문에 쿠키를 지원할 필요 없고, get_api_headers() 메소드를 통해 인증 자격과, MIME 타입 즉, 헤더 정보를 받을 수 있다. POST를 통해 데이터를 전송할 때는 json.dumps()로 인코딩 응답 받은 JSON은 json.loads()를 통해 디코딩하여야 한다.
``` python
class APITestCase(unittest.TestCase):
    def setUp(self): 
        self.app = create_app('testing')
        self.app_context=  self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        def get_api_header(self, username, password):
            return {
                'Authorization': 'Basic' b64encode((username+':'+password)).decode('utf-8'),
                'Accept': 'application/json'
                'Content-Type': 'application/json'
            }

        def test_posts(self):
             r = Role.query.filter_by(name='User').first()
            self.assertIsNotNone(r)
            u = User(email='john@example.com', password='cat', confirmed=True,
                    role=r)
            db.session.add(u)
            db.session.commit()

            response = self.client.post('/api/v1.0/posts', 
                headers= self.get_api_header('john@example.com', 'cat'),
                data=json.dumps({'body': ''}))
            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/v1.0/posts', 
                headers= self.get_api_header('john@example.com', 'cat'),
                data=json.dumps({'body': 'blog *post*'}))
            self.assertEqual(response.status_code, 201)
            url = response.headers.get('Location')
            self.assertIsNotNone(url)

            response = self.client.get(url,
                headers=self.get_api_header('john@example.com', 'cat'))
            self.assertEqual(response.status_code, 200)
            json_response = json.loads(response.get_data(as_text=True))
            self.assertEqual('http://localhost'+json_response.get('url'), url)
            self.assertEqual('blog *post*', json_response.get('body'))

            json_post = json_response

            response = self.client.get('/api/v1.0/user/{}/posts'.format(u.id), 
                headers=self.get_api_header('john@example.com', 'cat'))
            self.assertEqual(response.status_code, 200)
            json_response = json.loads(response.get_data(as_text=True))
            self.assertIsNotNone(json_response.get('posts'))
            self.assertEqual(json_response.get('count', 0), 1)
            self.assertEqual(json_response.get('posts')[0], json_post)
```

### 셀레니움을 이용한 엔드-투-엔드 테스트
플라스크 테스트 클라이언트는 애플리케이션을 전부 에뮬레이트하기엔 한계가 있다. 애플리케이션에 자바스크립트 코드가 있다면 플라스크 테스트 클라이언트로는 테스트할 수 없다. 왜냐하면 자바스크립트는 v8 엔진을 통해 컴파일 되기 때문이다.(대표적으로 Chrome, Node.js) 이러한 문제점을 해결하기 위해서는 실제 웹 브라우저를 사용하여 테스트하여야 한다. 셀레니움을 사용하여 테스트하려면 테스트 작업이 애플리케이션이 HTTP 리퀘스트를 리스닝(listening) 중인 웹 서버에서 실행되어야 한다. 셀레니움을 이용한 테스트의 간단한 흐름은 메인 스레드가 테스트를 실행하고 백그라운드 스레드에서 애플리케이션을 실행한다. 그리고 셀레니움이 웹 브라우저를 런칭하고 애플리케이션과 브라우저를 연결한다. 이 테스트가 끝나면 플라스크 서버를 수동을 중단해 주어야 되는데, HTTP 리퀘스트를 전송하는 방법만이 유일하다. (소스 코드는 github 참조 https://github.com/miguelgrinberg/flasky)


## HTTPie
웹 서비스를 테스트하기 위해서는 HTTP 클라이언트를 사용해야 한다. 커맨드에서 웹 서비스를 테스트할 때 자주 사용하는 클라이언트는 curl, HTTPie가 있다.
HTTPie가 더 간결하고 이해하기 쉽다한다. HTTPie나 curl는 경험상 편리한 도구는 아닌 듯 했다. 이러한 도구는 그때 그때 알아보는 것이 좋을 것 같다.



# 마지막 테스트를 하기에 앞서서...
테스트는 코드를 짜는 일 만큼이나 중요한 일이니 필수적이다고 말할 수 있다. 여기서 코드를 작성할 떄 중요한 점은 애플리케이션 컨텍스트 밖에서 실행되는(예를 들어 데이터베이스 모델) 부분들은 반드시 실행되어야 한다. 셀레니움 같은 엔드-투-엔드 테스트는 애플리케이션 컨텍스트가 필요한 테스트만 사용하자. 
또한 가능한 비즈니스 로직은 데이터베이스 모델에 넣고 다른 클래스는 컨텍스트와 독립적으로 구성하는게 좋다. 그래야 테스트하기 쉽다. 뷰 함수 코드는 리퀘스트를 받으면 애플리케이션 로직을 캡슐하는 다른 클래스나 함수에서 호출하는 정도의 간단한게 좋다. 

여기서 내게 중요하다고 느낀 부분은 바로
1. 가능한 비즈니스 로직은 데이터베이스 모델에 넣는다.
2. 뷰 함수는 애플리케이션 로직을 호출하는 수준의 간단한 인터페이스 정도로 하는 것이 좋다.







