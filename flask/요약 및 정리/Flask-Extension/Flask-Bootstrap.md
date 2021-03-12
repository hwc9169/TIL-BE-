## 2. Flask-Bootstrap 확장

bootstrap은 트위터에서 제공하는 오픈 소스 프레임워크이며 매력적인 웹 페이지를 생성할 수 있도록 사용자 인터페이스 컴포넌트를 제공한다.

부트스트랩과 어플리케이션을 통합하는 가장 확실한 방법은 템플릿에 모든 변경 사항들을 만들어 두는 것이다.

더 간단한 방법은 Flask-Bootstrap이라는 Flask확장을 사용한다.

```python
from flask_bootstrap import Bootstrap
```

> Flask-Bootstrap의 base 템플릿을 상속한 예제

```html
{% extends "bootstrap/base.html" %}
{% block title %} Flasky {% endblock %}
{% block navbar %}
<div class="navbar navbar-inverse" role="navigation">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle"
                    data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">Flasky</a>
        </div>
        <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li><a href="/">Home</a></li>
            </ul>
        </div>
    </div>
</div>
{% block content %}
<div class="container">
    <div class="page-header">
        <h1>Hello, {{name}}!</h1>
    </div>
</div>
{% endblock %}
```

 Flask-Bootstrap의 베이스 템플릿 블록
 
| 블록이름       | 설명                                     |
| ------------- | -----------------------------------------|
| doc   | 전체 HTML 문서                               |
| html_attribs | \<html\> 태그 안의 속성들            |
| html | \<html\> 태그의 콘텐츠                      |
| head   | \<head\> 태그의 콘텐츠                   |
| title   | \<title\> 태그의 콘텐츠           |
| metas   | \<meta\> 태그의 콘텐츠                      |
| styles   |CSS(캐스케이딩 스타일시트) 정의            |
| body_attribs   | \<body\> 태그 안의 속성들         |
| body   | \<body\> 태그의 콘텐츠                     |
| navbar   | 사용자 정의 내비게이션 바              |
| content   | 사용자 정의 페이지 콘텐츠                 |
| scripts   | 문서 아랫부분의 자바스크립트 선언          |   
