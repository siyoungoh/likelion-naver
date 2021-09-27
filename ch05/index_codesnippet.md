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
