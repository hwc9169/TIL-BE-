# WSGI 그리고 Flask

WSGI란 ```Web Server와 Web Application간의 HTTP 통신을 위한 명세(쉽게 말해 규칙)``` 입니다.

그렇다면 Web Server와 Web Application 그리고 WSGI, uwsgi 관계에 대해 알아보겠습니다.

기본적으로 웹 애플리케이션은 HTTP 형식의 요청과 응답을 주고받는 형식입니다. 요청은 1차적으로 Web Server(nginx나 Apache가 양대산맥을 이루고 있다. 이미지나 html과 같은 정적파일을 다룬다.)를 통해 처리되는데 

이 중에 서버사이트에서 처리가 필요한 경우 uwsgi라는 데몬(백그라운드에서 실행되는 프로그램)이 이 처리를 담당합니다.

uwsgi는 Application Container로써 적재한 Web Application을 실행 시켜주는 역할만 합니다. 그렇다고 모든 Web Application을 uwsgi에 적재할 수 있는 것이아니라 uwsgi가 실행할 수 있도록 명세를 따라야 합니다. 그리고 우린 이러한 명세를 WSGI라고 합니다. 정리하면 uwsgi는 WSGI명세를 따른 Application만을 실행 시켜주는 컨테이너 입니다.

간단히 WSGI를 설명하면 Python 표준으로 HTTP를 통해 요청을 받아 응답하는 Application에 대한 명세이고 이러한 명세를 만족하는 클래스나 함수(\_\_call\_\_()를 호출할 수 있는)객체를 WSGI 애플리케이션이라고 합니다.






훨씬 잘 설명한 블로그들 (출처) https://spoqa.github.io/2011/12/24/about-spoqa-server-stack.html

https://spoqa.github.io/2012/01/16/wsgi-and-flask.html


