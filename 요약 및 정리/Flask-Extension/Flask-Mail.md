## 5. Flask-Mail 확장

Flask-Mali 확장자는 smtplib를 래퍼하여 플라스크에서 쉽게 사용되도록 통합되어 있다.

파이썬 표준 라이브러리에서 제공하는 smtplib 패키지는 플라스크 애플리케이션에서 이메일을 전송하는 데 사용된다. (Simple Mail Transfer Protocol, SMTP , 메일 전송 프로토콜)



SMTP서버 설정키

| 키            | 기본값    | 설MAI                                  |
| ------------- | --------- | -------------------------------------- |
| MAIL_HOSTNAME | localhost | 호스트 이름 혹은 이메일 서버의  IP주소 |
| MAIL_PORT     | 25        | 이메일 서버의 포트                     |
| MAIL_USE_TLS  | False     | 전송 레이어 보안(TLS)의 보안 활성화    |
| MAIL_UEE_SSL  | False     | 보안 소켓 레이어(SSL)의 보안 활성화    |
| MAIL_USERNAME | None      | 메일 계정의 사용자이름                 |
| MAIL_PASSWORD | None      | 메일 계정의 패스워드                   |

* 설정을 하지않고 서버에 연결하면 localhost의 25번 포트에 사용자 인증 없이 이메일을 전송한다.



외부 SMTP서버 연결

```python
import os
​```
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
```



Flask-Mail 초기화  및 이메일 전송

```python
from flask_mail import Mail
​```

mail = Mail(app)

from flask_mail import Message

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    #Message(title, sender, recipient)
    
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    mail.send(msg)
```

