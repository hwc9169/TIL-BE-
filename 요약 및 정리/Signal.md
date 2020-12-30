# Signal
시그널은 플라스크의 내부 코드 중간에 정의한 함수를 실행할 수 있도록 한다. 사실 플라스크의 내부 동작을 감지하는 방식은 두가지가 있습니다.
1. 시그널
2. 내장 데코레이터(before_request, after_request, teardown_request)

하지만 내장 데코레이터와 다르게 시그널의 종류는 다양하다. 또한 시그널을 통해 실행되는 함수에서 데이터를 수정하면 안됩니다. 대신 데이터를 수정하고 싶을 땐 내부 데코레이터를 사용하면 됩니다. 마지막으로 여러 시그널 처리 함수가 연결되었을 때 실행 순서는 무작위입니다. 순서 보장을 원하는 경우 내장 데코레이터를 사용하면 된다.

## Blinker 설치
시그널을 사용하기 위해서는 먼저 Blinker를 설치해야 한다. 
```
pip install blinker
```

## Signal 객체  
신호를 주고 받기 위해서는 Signal 객체를 생성하고 Signal 객체의 send() 메서드를 통해 신호를 보낼 수 있으며, connect() 메서드로 신호를 받는 함수를 연결할 수 있다.
send() 첫번째 인자인 sender는 시그널을 일으킨 주체자의 정보를 나타낸다. sender는 시그널 감지 함수의  첫번째 매개변수고 이를 통해 특정 sender인 경우만 신호를 처리할 수 있다. 

```python
from blinker import Signal
from blinker import signal

sig = Signal() # 이름 없는 시그널
hi_sig = signal('hi-sig')

def hi(sender):
    print("Hi ", sender)

sig.connect(hi)
sig.send('John')
sig.send('Tom')
```
## 플라스크 내장 시그널
플라스크에는 기본으로 내장된 시그널이 존재한다. (예를 들어 request_started, request_finished, template_rendered)
request_started 시그널을 통해  HTTP 요청이 발생하는 경우 "Request received"를 출력 해보자.(참고로 내장 시그널은 Flask 객체가 sender가 된다.)

```python
from flask import request_started

def when_request_started(sender):
    print('Request1 received! Sender: ', sender)

@request_started.connect_via(app)
def when_request_started2(sender):
    print('Request2 received! Sender: ', sender)

request_starated.connect(when_request_started)
```
