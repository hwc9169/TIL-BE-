from flask import Blueprint

main = Blueprint('main', __name__ ) # 첫번쨰 인수 : 블루프린트 이름, 두번쨰 인수 : 블루프린트가 위치할 모듈, 패키지
from . import views ,errors


