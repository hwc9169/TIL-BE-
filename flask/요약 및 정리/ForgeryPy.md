# ForgeryPy
ForgeryPy란 애플리케이션을 테스트할 때 가짜 데이터를 생성해주는 자동 솔루션이다. 예를 들어 블로그 애플리케이션을 제작할 때, 테스트(페이지네이션과 같은 것들을) 해보기위해 일일이 손으로 블로그들을 게시하는 것이 아니라. ForgeryPy로 자동화 할 수 있다.


참고 서적 : https://github.com/tomekwojcik/ForgeryPy
## Example usage 
```python
import forgery_py

print(forgery_py.address.street_address())  #4538 Shopko Junction 도로명 주소

print(forgery_py.basic.hex_color()) #3F0A59 16진수 컬러

print(forgery_py.currency.description()) #Slovenia Tolars 화폐

print(forgery_py.date.date()) # datetime.date(2012, 7, 27)

print(forgery_py.internet.email_address()) # brian@zazio.mil

print(forgery_py.lorem_ipsum.title()) # Pretium nam rhoncus ultrices! 블로그 제목

print(forgery_py.name.full_name()) # Mary Peters 풀 네임
```

## 디렉토리 구조
- forgery
    - address.py
        - street_name() (도로명 이름)
        - street_number() (도로명 번호)
        - street_suffix() (도로명의 접미어)
        - street_address() (도로명 주소)
        - city() (도시 이름)
        - state() (주 이름)
        - state_abbrev() (간략화한 주 이름)
        - zip_code() (zip 코드)
        - phone() (전화 번호)
        - country() (국가)
        - continent() (대륙)
    - basic.py (기본)
        - hex_color() (16진수 색깔 코드)
        - hex_color_short() (짧은 색깔 코드)
        - text(length, at_least, at_most, lowercase, uppercase, digits, spaces, punctuation) (본문)
    - currency.py (화폐)
        - description() (화폐에 대한 설명 ex.United Kingdom Pounds )
        - code() (화폐 코드 ex.GBP)
    - date.py
        - day_of_week(abbr) (요일 정보)
        - day(month_length) (몇일 정보)
        - month(abbr, numerical) (몇달 정보)
        - year(past, min_delta, max_delta) (몇년도)
        - date(past, min_delta, max_delta) (날짜 정보)
    - internet.py
        - user_name(with_num) (유저 이름)
        - top_level_domain() (최상위 도메인 ex. .com, .kr)
        - domain_name() (도메인 이름)
        - email_address(user) (이메일)
        - cctld() (국가 TLD 코드)
        - ip_v4() (아이피 정보)
    - lorem_ipsum.py
        - word() (단어)
        - words(quantity, as_list) (단어들)
        - title(words_quantity) (제목)
        - sentence() (문장)
        - sentences() (문장들)
        - paragraph(**kwargs) (문단)
        - paragraphs(**kwargs) (문단들)
    - name.py
        - first_name() (이름)
        - last_name() (성)
        - full_name() (성 + 이름)
        - male_first_name() (남자 이름)
        - femail_first_name() (여자 이름)
        - company_name() (회사 이름)
        - job_title() (직급)
        - job_title_suffix()
        - title() (ex. Mr., Ms.)
        - location() (건물 이름)
        - industry() (산업)
    - personal.py
        - gender() (성별)
        - abbreviated_gender() (줄인 성별)
        - shirt_size() (셔츠 사이즈)
        - race() (인종)
        - language() (언어)
