# Unittest
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

setUp() 메소드와 tearDown() 메소드는 unittest.TestCase 메소드를 오버라이딩한 것으로 각각은 테스트를 시작하기 전, 시작한 후에 실행된다. 테스트를 실행하면 순서는 다음과 같다

1. setUp()
2. test_app_exists()
3. tearDown()
4. setUp()
5. test_app_is_testing()
6. tearDown()