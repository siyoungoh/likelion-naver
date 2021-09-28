## 기본 명령어

- ssh 로 서버 접속하기

```bash
ssh 사용자명@ip주소 -p 포트번호
```

```bash
ssh root@12.345.12.64 -p 1024
```

- Enter password 가 나오면 비밀번호 입력하기

- root 유저의 비밀번호 변경하기

```bash
passwd root
```

- new password 가 나오면 비밀번호 입력하기

- 폴더 이동하기
  - Change Directory 약자

```bash
cd 폴더명
```

- 상위 폴더 이동하기

```bash
cd ..
```

- home 폴더 이동하기

```bash
cd ~
```

## mongodb 비밀번호 변경하기

- 데이터베이스는 admin, 기존 사용자명은 sample, 비밀번호 1234, 권한(role)은 root 라고 가정
- 이미 유저, 비밀번호가 걸려있기 때문에 mongo 에 접근할 때 생성된 비번으로 접속해야함이미 만들어둔 user 는 root 권한을 가지고 있어요.

1. user가 sample 인걸로 접속하기

```bash
mongo -u sample
```

2. Enter password: 가 나오면 비밀번호인 1234 입력하기

- 글자를 타이핑해도 화면에는 보이지 않아요.

3. mongo shell 에 접속되었으면 화면 앞부분이 > 이렇게 바뀌어요.user : change, pwd 를 strongpwd 로 바꾸는 코드

```bash
use admin;
db.createUser({user:"change", pwd: "strongpwd", roles:["root"]})
```

4. 기존에 있던 user:test 삭제해주기

```bash
 db.dropUser("sample")
```

## Python 파일 실행하기

- 파이썬 버전 확인하기

```bash
python3 --version
```

- 파일명 실행하기

```bash
python 파일명
```

- 예. app.py 실행하기

```bash
python app.py
```

## 가상환경 설정

1. 설치파일 모음집 업데이트하기

```bash
sudo apt-get update
```

2. 가상환경 설정을 위한 ubuntu 에 tool 설치 `python3-venv` 설치하기

```bash
sudo apt-get install python3-venv
```

3. myenv 로 가상환경 폴더 만들기

```bash
python3 -m venv ./myenv
```

4. 가상환경 구동시키기

```bash
. myenv/bin/activate
```

5. 가상환경 끄기

```bash
deactivate
```

6. 패키지 설치하기

- 가상환경이 구동되어있는 상태에서 아래 명령어 입력하기

```bash
pip install pymongo beautifulsoup4 requests flask pytz
pip install boto3==1.6.19
```

## 백그라운드로 실행시키기

```bash
nohup 명령어 &
```

```bash
nohup python app.py &
```

## 현재 실행되고 있는 프로세스 확인하기

- ProceSs

```bash
ps -ef
```

- 그 중에서 python 이라는 키워드가 있는 것만 보여주기

```bash
ps -ef | grep python
```

- 프로세스 번호 확인해서 특정 프로세스 종료시키기

```bash
kill -9 pid값
```

## NCP Object Storage 설정
- 참고 : [ncloud CLI 사용법 - Object Storage](https://cli.ncloud-docs.com/docs/guide-objectstorage) / [AWS CLI 사용방법 - S3 API put bucket CORS](https://docs.aws.amazon.com/cli/latest/reference/s3api/put-bucket-cors.html)
1. 사용 tool AWS CLI 설치하기
  ```bash
  pip install awscli==1.15.85
  ```
2. Bucket 관련 접속 설정
  ```bash
  aws configure
  ```
  - 아래와 같은 화면이 뜨면 각각에 Object storage 의 API 인증 정보 입력 - 계정 인증 API 값
  ```bash
  - AWS Access Key ID [****************leLy]: ACCESS_KEY_ID
  - AWS Secret Access Key [None]: SECRET_KEY
  - Default region name [None]: [Enter]
  - Default output format [None]: [Enter]
  ```
3. 제대로 연결되어서 버킷 리스트 조회되는지 확인
  ```bash
  aws --endpoint-url=https://kr.object.ncloudstorage.com s3 ls
  ```
4. CORS 파일(예. cors.json) 업로드 와 설정
  - 서버에 있는 설정 파일 cors.json 사용한다고 가정 (사전에 Filezilla 처럼 FTP 등을 통해 설정파일 업데이트)
    - [cors.json](heyvolleyballnews/asset/cors.json) 파일 다운로드 또는 하단 내용으로 cors.json 파일 
    ```json
    {"CORSRules": [
        {
            "AllowedHeaders": [
                "*"
            ],
            "AllowedMethods": [
                "HEAD",
                "GET"
            ],
            "AllowedOrigins": [
                "*"
            ],
            "MaxAgeSeconds": 3000
        }
        ]
    }
    ```
  - cors.json 파일 설정을 버킷에 적용
  ```bash
  aws --endpoint-url=https://kr.object.ncloudstorage.com s3api put-bucket-cors --bucket 내버킷이름 --cors-configuration file://cors.json
  ```
5. 적용 확인
  ```bash
  aws --endpoint-url=https://kr.object.ncloudstorage.com s3api get-bucket-cors --bucket 내버킷이름
  ```
  
