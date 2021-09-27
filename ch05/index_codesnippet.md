# index.html 파일 안 추가해야하는 code 조각
## calamansi (audio player JS library) 설정
- `<head>` 부분
```html
<!-- calamasi css -->
<link rel="stylesheet" href="https://kr.object.ncloudstorage.com/likelion-naver/asset/calamansi.min.css">
```
- `<body>` 부분
```html
<!-- Audio player -->
<div id="calamansi-player-1">
    Loading player...
</div>

<!-- calamansi default js -->
<script src="https://kr.object.ncloudstorage.com/likelion-naver/asset/calamansi.min.js"></script>
```

- `Javascript 부분`
```javascript
// 오디오 파일 가져오기
const audio_url = '/api/audios';
fetch(audio_url, init)
    .then(res => {
        if (res.status === 200) {
            return res.json()
        } else {
            console.error(`HTTP error! status: ${res.status}`)
        }
    })
    .then(jsonData => {
        // console.log(jsonData);

        new Calamansi(document.querySelector('#calamansi-player-1'), {
            skin: 'https://kr.object.ncloudstorage.com/내버킷명/asset/skins',
            playlists: {
                'News': jsonData['audio_list']
            },
            defaultAlbumCover: 'https://kr.object.ncloudstorage.com/내버킷명/asset/skins/default-album-cover.png',
        });
    })
    .catch(err => {
        console.log(err)
    })
```

## og tag 설정
```html
<meta property="og:title" content="Hey Volleyball News" />
<meta property="og:description" content="매일 업데이트되는 큐레이션된 배구뉴스와 음성 오디오북" />
<meta property="og:image" content="https://images.unsplash.com/photo-1588492069485-d05b56b2831d?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1051&q=80" />
```

## favicon 설정
- 참고.favicon 만들기 : https://www.favicon-generator.org/
```html
<link rel="shortcut icon" href="https://kr.object.ncloudstorage.com/내버킷명/asset/favicon.ico" type="image/x-icon">
```
