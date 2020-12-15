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

### 코드 커버리지 리포트 획득
Test Suite를 가지는 것은 중요하지만, 그것이 어떻게 사용할 때 유용한지 혹은 악용될 소지가 없는지 알아야 한다. 코드 커버리지 툴은 유닛 테스트가 애플리케이션을 얼마나 커버할 수 있는지 측정해준다. 즉 애플리케이션 코드의 테스트되지 않은 부분을 알려준다. 
이 툴은 커맨드 라인 스크립트로 동작한다. 그러나 프로그래밍해서 시작할 수도 있다. manage.py 런처 스크립트 안에 통합 커버리지 메트릭스를 얻어보자

```python
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage 
    COV = coverage.coverage(branchh=True, include='app/*)
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

## HTTPie
웹 서비스를 테스트하기 위해서는 HTTP 클라이언트를 사용해야 한다. 커맨드에서 웹 서비스를 테스트할 때 자주 사용하는 클라이언트는 curl, HTTPie가 있다.
HTTPie가 더 간결하고 이해하기 쉽다한다. HTTPie나 curl는 경험상 편리한 도구는 아닌 듯 했다. 이러한 도구는 그때 그때 알아보는 것이 좋을 것 같다.











