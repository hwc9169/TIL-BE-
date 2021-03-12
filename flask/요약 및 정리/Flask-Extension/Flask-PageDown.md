# Flask-PageDown

플라스크 페이지 다운 확장은 Flask-WTF 폼을 사용하여 페이지다운(자바스크립트로 구현된 클라이언트 측 Markdown-to-HTML 변환기)을 통합한 플라스크의 페이지다운 래퍼다. 즉 Flask-PageDown 확장은 자바스크립트의 Markdown-to-HTML 변환기를 Flask에서 사용할 수 있도록 래퍼된 라이브러리다.

## Flask-PageDown 사용법
\_\_init\_\_.py
```python
import flask_pagedown import PageDown

pagedown = Pagedown(app)

...
from flask_wtf import FlaskForm
from flask_pagedown import PageDownField

class PostForm(FlaskForm):
    body = PageDownField("What's on your mind? ", validate=[Required()])
    submit = SubmitField('Submit')

```
index.html
```html
{% block scripts %}
{{super()}}
{{pagedown.include_pagedown()}}
{% endblock %}
```

## 서버에서의 마크다운 처리
마크다운 소스와 함께 생성된 HTML 프리뷰를 같이 서버에 전송하는 것은 보안의 위험이 있기 때문에 서버 측에서 마크다운과 파이썬 Markdown-to-HTML 변환기를 사용하여 HTML로 변환하여야한다. bleach 라이브러리를 사용하면 특정 태그, 속성만 사용하도록 HTML 코드를 필터링 할 수 있다. 게시물이 포스트 될 때마다, 마크다운 소스를 HTML 코드로 변환하여 저장하면 매번 랜더링할 때마다 HTML로 변환하는 작업을 하지 않아도 된다. 

```python
from markdown import markdown
import bleach

class Post(db.Model):
    # ...
    body_html = db.Column(db.Text)
    # ...
    @staticmethod
    def markdown_to_html(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'h1', 'h2', 'h3']
        taget.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags = allowed_tags, strip=True))

db.event.listen(Post.body, 'set', Post.markdown_to_html)
```

markdown_to_html 함수는 body의 SQLAlchemy의 "set" 이벤트 리스너로 등록된다. 이것은 body 필드가 새로 설정되면 자동으로 markdown_to_html 함수가 호출된다는 의미다. 이 함수는 body에 마크다운 소스를 HTML로 변환하여 body_html 필드에 저장한다.

변환 작업은 세 단계에 걸쳐 이루어진다. 
1. markdown 함수가 HTML로 초기 변환 작업을 한다. 
2. 그 결과는 clean에 전달되어 태그를 필터링한다. 
3. 마지막 linkify() 함수는  \<a\> 링크 안에 플레인 텍스트로 작성된 URL을 변환한다.

마지막 과정은 공식적으로는 마크다운 스펙에 자동 링크 생성이 존재하지 않기 때문에 이 작업이 필요한 것이다.  

최종적으로 HTML로 변형된 게시물을 렌더링하는 코드로 마무리한다.
```html
<div class="post-body">
    {% if post.body_html %}
        {{ post.body_html | safe }}
    {% else %}
        {{ post.body }}
<div>
```

jinja2는 보안을 위해서 모든 템플릿 변수를 빠져나가도록 하는데,"safe"는 HTML body를 렌더링할 때 HTML 태그를 빠져나가지 않도록 한다. HTML은 서버에서 생성되었기 때문에, 렌더링시 안전하다.