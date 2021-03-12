# Classview
flask는 장고처럼 클래스 기반 뷰를 제공하는데 클래스기반 뷰는 HTTP 메소드에 따른 처리 코드를 작성할 때 편리하다는 장점이있다.
또한 다중상속과 같은 객체지향의 특징을 활용해서 코드의 재사용과 개발 생산성을 높여준다.

플라스크에서 클래스기반 뷰 사용햐기 위해서는 다음의 규칙이 지켜져야한다.

- flask.view.View 클래스를 상속한다.
- dispatch_request() 메소드를 작성한다.(실질적인 view 함수가 된다.)

```python
from flask.view import View
from flask import render_template
class ListView(View):
    def get_template_name():
        return NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self, name):
        context = {'objects': self.get_objects()}
        return self.render_template(context)

class UserView(ListView):
    def get_template_name(self):
        return 'user.html'
    
    def get_objects(self):
        return User.query.all()

app.add_url_rule('/users/<name>', view_func=UserView.as_view('users'))
```

# 메소드 기반 뷰
메소드 기반 뷰는 RESTful API에서 매우 유용한 기능이므로 익숙해질 필요가 있다.
HTTP 메소드 별로 클래스의 메소드를 실행한다.
```python
from flask.view import MethodView
class UserView(MethodView):
    def get(self, user_id):
        if user_id == None:
            ...
        else:
            ...

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

user_api = UserView.as_view('user_api') 
app.add_url_rule('/users/', defaults={'user_id': None}, view_func=user_api, methods=['GET',])
app.add_url_rule('/users/', view_func=user_api, methods=['POST',])
app.add_url_rule('/users/<int:user_id>', view_func=user_api, methods=['GET', 'PUT', 'DELETE'])

```
