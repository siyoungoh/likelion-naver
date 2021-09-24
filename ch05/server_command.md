## 기본 명령어

- 비밀번호 변경하기

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
