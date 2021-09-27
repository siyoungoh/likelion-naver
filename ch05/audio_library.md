# HTML 페이지에 사용할 audio 플레이 JS library 설정
(현재 문서 버전 2021-09-27)
- 원본 repository : https://github.com/voerro/calamansi-js
- **버그가 개선된 최신 버전 사용을 위해 원본 repository 접속해 사용하기 권장**
- 위 repository를 Download 해서 사용

## Object storage 업로드
1. Object storage 에 asset 폴더 생성
- https://console.ncloud.com
3. asset 폴더 안에 다운로드 받은 repo 폴더 안 dist/calamasi.min.css 와 dist/calamasi.min.js 업로드
  ```md
  asset
  ㄴ calamasi.min.css
  ㄴ calamasi.min.js
  ```
3. 수업에서 사용하는 skin인 dist/skins/calamansi-compact 를 아래와 같은 구조로 추가 업로드 
  ```md
  asset
  ㄴ calamasi.min.css
  ㄴ calamasi.min.js
  ㄴ skins
    ㄴ fonts
    ㄴ skin.css
    ㄴ skin.js
    ㄴ skin.html
  ```
  - 단, skin.css 파일은 하단 내용으로 변경 후에 업로드
4. skin.css 파일의 277번째 줄부터 내용 아래처럼 변경
- 실제 해당 파일의 object storage 주소로 변경해야함. 
- 원본 파일의 `fonts` 로 적혀있는 부분을 `https://kr.object.ncloudstorage.com/내버킷명/asset/fonts` 로 변경
```css
@font-face {
  font-family: 'calamansi-skin--calamansi-compact--glyphter';
  src: url('https://kr.object.ncloudstorage.com/내버킷명/asset/fonts/Glyphter.eot');
  src: url('https://kr.object.ncloudstorage.com/내버킷명/asset/fonts/Glyphter.eot?#iefix') format('embedded-opentype'),
       url('https://kr.object.ncloudstorage.com/내버킷명/asset/fonts/Glyphter.woff') format('woff'),
       url('https://kr.object.ncloudstorage.com/내버킷명/asset/fonts/Glyphter.ttf') format('truetype'),
       url('https://kr.object.ncloudstorage.com/내버킷명/asset/fonts/Glyphter.svg#Glyphter') format('svg');
  font-weight: normal;
  font-style: normal;
}
```
5. skin.css `3.` 에 언급된 위치에 업로드
6. asset 폴더 공개 설정
- 주의. 새롭게 파일이 추가될 때마다 공개 설정을 해주어야 새로운 파일도 공개 적용이 됨. 
