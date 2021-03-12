## 3. Flask-WTF

플라스크는 폼을 처리하기 위해서 Flask-WTF 확장을 사용하여 처리한다.

Flask-WTF를 사용할 때 각 웹 폼은 Form 클래스로부터 상속한 클래스에 의해  표현된다.

이 클래스는 폼에 있는 필드의 리스트를 정의하는데 이는 각각 오브젝트로 표현된다.

각 오브젝트는 하나 이상의 검증자가 있어서 사용자가 서브밋한 입력값이 올바른지 체크할 수 있다. 



```python
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')
```



WTForms에서 지원하는 표준 HTML 필드의 리스트 

| 필드타입      | 설명                                      |
| ------------- | ----------------------------------------- |
| StringField   | 텍스트 필드                               |
| TextAreaField | 다중 라인 텍스트 필드                     |
| PasswordField | 패스워드 텍스트 필드                      |
| Hiddenfield   | 숨겨진 텍스트 필드                        |
| DateField     | 주어진 포맷에서 datetime.date 값을 받는다 |
| BooleanField  | True와 False 값을 갖는 체크박스           |
| FileField     | 파일 업로드 필드                          |
| SubmitField   | 폼 서브미션 버튼                          |
| IntegerField  | 정수값을 받는 텍스트 필드                 |



| 검증자      | 설명                                                         |
| ----------- | ------------------------------------------------------------ |
| Email       | 이메일 주소를 검증                                           |
| EqualTo     | 두 필드의 값을 비교, 확인하기 위해 패스워드를 두번 입력하도록 할때 유용 |
| Length      | 문자열의 길이 검증                                           |
| NumberRange | 입력한 값이 숫자와 알파벳 범위인지를 검증                    |
| Optional    | 필드에서 빈 입력을 허용하고, 추가한 검증자를 건너뛴다        |
| Required    | 필드에서 빈 입력을 허용하지 않는다                           |
| URL         | URL을 검증                                                   |
| Regexp      | 정규표현식에 대한 입력을 검증                                |


### 크로스-사이트 리퀘스트 위조(CSRF) 보호

기본적으로 Flask-WTF는 크로스 사이트 리퀘스트 위조(CSRF) 공격으로부터 모든 폼을 보호한다.
CSRF 공격은 악의적 웹사이트에서 희생자가 로그인한 다른 웹사이트로 리퀘스트를 전송할 때 일어난다.
CSRF 보호를 구현하기위해 Flask-WTF는 암호화 키로 토큰을 생성하여 리퀘스트 인증을 검증하는 데 사용한다. 
아래 예제는 암호화 키를 설정하는 방법이다.

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
```



추가적으로 중요한 개념이 있는데 app.config 딕셔너리는 프레임워크나 확장 또는 애플리케이션 자체에서 사용된다. app.config 딕셔너리는 설정 변수들을 저장하는 공간이다. 설정 변수들은 딕셔너리 문법에 따라 app.config 오브젝트에 추가된다. 심지어 app.config(설정 오브젝트)는 파일이나 환경에서 설정값을 불러오는 메소드도 가지고 있다.



# 02. 사용자 세선

폼을 통해 서브밋하고 브라우저에서 새로고침을 누르면 브라우저에서 경고 메시지를 띄운다. 이러한 현상은 브라우저에서 페이지를 새로고침을 하면 가장 마지막에 보낸 리퀘스트를 반복하게 되는데, 폼 데이터를 갖는 POST 리퀘스트일 때, 폼 서브미션을 두 번하게 되는 문제가 생긴다. 이는 Post 리퀘스트에 대한 응답을 redirect로 하면 마지막에 사용자가 보낸 리퀘스트는 GET이 된다.(redirect는 항상 GET 리퀘스트만 발생시킨다.) 이러한 기법을 Post/Redirect/Get pattern이라 한다.

이러한 기법을 사용하려면 사용자 세션을 사용하여야한다. 왜냐하면 post 데이터가 리다이렉트 되면서 지워지기 때문이다.

> 사용자 세션은 클라이언트 측 쿠키에 저장된다. 이 세션은 설정 변수인 SECRET_KEY로 암호화되어 있다. 쿠키가 임의로 변경되면 세션은 무효화된다.

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))
```

