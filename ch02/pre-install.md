## 1. Chrome 설정
- Chrome 설치 download link https://www.google.com/intl/ko/chrome/
- Chrome 확장 프로그램 설치 JSON View https://chrome.google.com/webstore/detail/jsonview/chklaanhfefbnpoihckbnefhakgolnmc?hl=en
  - Chrome으로 위 url 접속 후, 파란색 버튼 클릭해 설치 (`Chrome에 추가` 또는 `Install from Chrome` 버튼)
  - 상세 설치방법 참고 : https://support.google.com/chrome_webstore/answer/2664769?hl=ko

## 2. Python 설치
- Python 3.8.10 설치파일 다운로드 링크 : https://www.python.org/downloads/release/python-3810/
  - 만약 이미 Python 3.7 버전 이상이 설치되어있으면 재설치 하지 않아도 됨.
  - Files  항목에서 내 컴퓨터 종류에 해당되는 파일 다운로드 (Version 항목에 있는 이름 클릭)
- Windows 사용자 설치 파일 종류 
  - Windows 64bit(비트) 사용일 경우 : Windows installer (64-bit) 설치
  - Windows 32bit(비트) 사용일 경우 : Windows installer (32-bit) 설치
  - 참고 : 내 컴퓨터가 32비트인지 64bit 확인하기 - [Windows 도움말 : 컴퓨터가 32비트 버전과 64비트 버전의 Windows 중 어떤 버전을 실행하는지 확인하려면 어떻게 하나요?](https://support.microsoft.com/ko-kr/windows/32%EB%B9%84%ED%8A%B8-%EB%B0%8F-64%EB%B9%84%ED%8A%B8-windows-%EC%A7%88%EB%AC%B8%EA%B3%BC-%EB%8C%80%EB%8B%B5-c6ca9541-8dce-4d48-0415-94a3faa2e13d)
- Mac 사용자 설치파일 종류 
  - Mac (macOS 10.9 이상) : macOS 64-bit Intel installer
  - Mac (M1 사용자) : macOS 64-bit universal2 installer
  - 참고 : 내 컴퓨터가 M1 인지 확인하는 방법 - [choesin.com - Mac에서 Intel 또는 Apple Silicon 프로세서를 사용하는지 확인하는 방법](http://choesin.com/mac%EC%97%90%EC%84%9C-intel-%EB%98%90%EB%8A%94-apple-silicon-%ED%94%84%EB%A1%9C%EC%84%B8%EC%84%9C%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%98%EB%8A%94%EC%A7%80-%ED%99%95%EC%9D%B8%ED%95%98%EB%8A%94-%EB%B0%A9)
  
## 3. Visual Studio Code 설치 / 상세 사용법
- 설치 파일 다운로드 링크 : https://code.visualstudio.com/?wt.mc_id=vscom_downloads 
  - Download 버튼을 눌러 내 컴퓨터에 맞는 버전 다운로드 후 설치 
- 생활코딩 - Visual Studio Code 사용법 : https://youtu.be/K8qVH8V0VvY
- 생활코딩 - Visual Studio Code에서 Python 사용방법:  https://youtu.be/K8qVH8V0VvY?t=1128

### 확장 설치
- Visual Studio Code 를 더 편하게 사용하기 위한 확장 플러그인. 수업에서는 해당 플러그인이 설치되어있다는 가정 하에 설명합니다. 
- 하단 설치 링크 또는 확장 플러그인명을 검색해 확장 설치. 설치 후 Visual Studio Code 껐다가 다시 켜기

#### 한국어로 설정 바꾸어주기
- Korean Language Pack for Visual Studio Code - 게시자: Microsoft (링크: https://marketplace.visualstudio.com/items?itemName=MS-CEINTL.vscode-language-pack-ko)

#### Front-end 화면을 위한 플러그인
- Bracket Pair Colorizer 2 (링크: https://marketplace.visualstudio.com/items?itemName=CoenraadS.bracket-pair-colorizer-2)
- Live Server - 게시자: Ritwick Dey (링크: https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
- Auto Import - 게시자: steoates (링크: https://marketplace.visualstudio.com/items?itemName=steoates.autoimport)
- ESLint - 게시자: Dirk Baeumer (링크: https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- JavaScript (ES6) code snippets - 게시자: charalampos karypidis (링크: https://marketplace.visualstudio.com/items?itemName=xabikos.JavaScriptSnippets)

#### Python 사용을 위한 플러그인
- Python - 게시자: Microsoft (링크: https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- Kite AutoComplete AI Code (링크: https://marketplace.visualstudio.com/items?itemName=kiteco.kite)
- Python Indent - 게시자: Kevin Rose (링크: https://marketplace.visualstudio.com/items?itemName=KevinRose.vsc-python-indent)

### 환경 설정 - 파일 저장시 자동 파일 정렬
- 맥북 사용시 ctrl 대신 cmd 를 사용해주세요. 
- 환경설정으로 들어가기 : ctrl + shift + p 를 눌러 뜨는 검색창에 '설정' 입력 후 `기본 설정~` 항목이 뜨면 엔터를 눌러서 들어감. 
- format on save 검색 후 체크박스 체크
  ![](https://firebasestorage.googleapis.com/v0/b/firescript-577a2.appspot.com/o/imgs%2Fapp%2Fohahohah%2F7t1ntxntIg.png?alt=media&token=0c93af37-8136-4e6d-b1d1-d68ca76b3e23)
- 만약 setting.json 으로 뜬다면 해당 창에서 ctrl + F 를 눌러 검색하기 창을 띄운후 auto 라고 검색
  - `editor.formatOnSave" 의 값을 true 로 변경 후 저장하기(ctrl + s)
  ![](https://firebasestorage.googleapis.com/v0/b/firescript-577a2.appspot.com/o/imgs%2Fapp%2Fohahohah%2FvddJDwKnRi.png?alt=media&token=c0198416-8ca0-4ea0-bf5b-e70a71df5ac6) 

## 4. Robo3T 설치하기 
- Mongodb 에 저장된 내용을 확인하고, 간단한 수정을 할 수 있는 프로그램. 이렇게 DB의 내용을 보거나 간단한 CRUD 를 할 수 있는 프로그램을 DB Client 라고 함. 
- 설치 프로그램 다운로드 링크 : https://robomongo.org/download 에서 Download Robo3T 클릭
- Winodws 7,8 의 경우, 4.2 버전을 다운로드하세요. Dowload link : https://docs.mongodb.com/manual/administration/production-notes/#prod-notes-supported-platforms

## 5. [Windows 사용자만] Git bash 설치
- 이미 Git 설치가 되어있다면 `Git bash` 라는 프로그램이 설치되어있습니다. 
- 만약 Git 설치가 되어있지 않다면 아래 다운로드 링크에서 설치하면 됩니다. 설치 옵션은 변경하지 말고 모두 Next 버튼을 눌러 설치해주세요. 
- 링크 https://git-scm.com/downloads

## 6. 사이트 회원가입하기
- https://www.ncloud.com/ 에 가입 후, 수업 크레딧 받기까지 되어있으면 됩니다. 
- 아래 사이트에 이미 가입되어있는 상태라면, 기존 계정을 사용하면 됩니다. 
- 공공데이터포털 https://www.data.go.kr/ 에 회원가입해주세요.
- https://naver.com/ 에 회원가입해주세요. 
