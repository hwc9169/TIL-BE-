## 6. Flask_Moment 확장

웹 애플리케이션에서 날짜와 시간을 처리할 때 사용자가 전 세계에서 사용한다면 서로 다른 시간대를 사용하기 때문에 처리가 복잡해진다. 서버는 각 사용자의 위치와 무관한 일정한 시간 단위인 협정세계시(Coordinated Universal Time, UTC) 를 사용한다. 그러나 사용자는 UTC로 표현된 시간이 이해하기 힘들기 때문에 자신의 거주 위치에 맞는 지역 시간으로 표현하여야 한다. Flask_Moment 확장은 브라우저에서 시간과 날짜를 렌더링하도록 하는 moment.js와 Jinja2 템플릿이 통합된 플라스크 애플리케이션용 확장이다. 

Flask-Moment 초기화

```python
form flask_moment import Moment
moment = Moment(app)
```

Flask-Moment는 moment.js 외에도 jquery.js가 필요하다. 이 두 라이브러리는 HTML 문서 어디에 위치해도 상관없다. 확장으로 제공되는 헬퍼 함수를 통해 사용될 수도 있다. 이 헬퍼 함수는 콘텐트 딜리버리 네트워크(Content Delivery Network, CDN)에서 위의 두 라이브러리의 테스트된 버전을  참조한다. 부트스트랩은 이미 jquery.js를 포함하고 있기 때문에, moment.js만 추가하면 된다. 

moment.js 라이브러리 임포트

```html
{% block scrips %}
{{ super() }}
{{ moment.include_moment()}}
{% endblock %}
```



타임스탬프를 사용하기 위해 Flask-Moment는  moment 클래스를 생성한다.(이는 템플릿에서도 사용 가능하다.)  그렇다면 예제를 바로 살펴봅시다.

flask-moment 사용 예제, hello.py: datetime 변수 추가

```python
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())
```

flask-moment 사용 예제, templates/index.html: Flask-Moment를 이용한 타임스탬프 랜더링

```html
{% extends "base.html" %}
{% block page_content %}
	<p>The local Date and time is {{ moment(current_time).format('LLL') }}.</p>
	<p>That was {{ moment(current_time).fromNow(refresh=True) }}</p>
{% endblock %}
```

format('LLL') 포맷은 클라이언트 컴퓨터에 설정된 시간대와 위치에 따라 날짜와 시간을 랜더링하고,
fromNow() 랜더링 스타일은 상대 타임스탬프를 랜더링하고 넘겨진 시간에 따라 자동을 리프레시한다. 




