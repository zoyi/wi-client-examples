# Sessions API client example (Python)

본 예제는 특정 샵, 날짜 하루 동안의 모든 세션 데이터를 가져와서 csv 파일에 저장합니다.

## 준비물

* [pyenv](https://github.com/pyenv/pyenv#homebrew-on-mac-os-x)
* [pipenv](https://github.com/pypa/pipenv)

## 실행 방법

.env 파일을 작성합니다. 경로는 PROJECT_ROOT/.env여야 합니다.

```
X_USER_EMAIL="user@email.com"
X_USER_TOKEN="asdfasdfdasdfasdfdsf"
```

다음과 같이 실행합니다.

```sh
$ pipenv install
$ pipenv shell
$ python session.py [매장 아이디] [세션 날짜 YYYY-MM-DD 포맷]
```

자체 테스트 결과 평균 api 응답 소요 시간(200개씩 세션을 불러올 경우)은 0.1초입니다.

## 소스코드 임포트

session.py 내의 csv_dump_sessions 함수를 import 하여 사용하실 수도 있습니다.

## Pipenv를 사용하지 않는 경우

.env 파일을 알아서 불러와주지 않으므로 [python-dotenv](https://github.com/theskumar/python-dotenv) 등을 사용하거나

```sh
$ export X_USER_EMAIL="user@email.com"
$ export X_USER_TOKEN="asdfasdfdasdfasdfdsf"
```

와 같이 환경 변수를 등록해주어야 합니다.