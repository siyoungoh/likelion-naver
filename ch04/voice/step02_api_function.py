# -*- coding: utf-8 -*-
from pathlib import Path
import requests

# API 인증 정보
client_id = "내 client_id"
client_secret = "내 client_secret"

# 변환할 message
# text = "도쿄올림픽 인상적 활약 1위는 女 배구 김연경. 2020 도쿄올림픽에서 한국 대표팀 중 가장 인상적인 활약을 펼친 선수로 여자 배구의 김연경이 1위를 차지했다.한국갤럽이 13일 발표한 '한국인이 본 도쿄올림픽' 여론 조사 결과 김연경은 전체 응답자의 63%로부터 가장 인상적인 활약을 펼친 선수로 지목돼 이 부문 1위에 올랐다"
text = "안녕하세요, 반갑구만 반가워요!"

file_path = 'tts'
file_name = 'hello02.mp3'

# ====함수 설계====
# tts
# 기능 : clova voice api 사용해서 텍스트를 음성 mp3 로 바꿈
# input(param) : client_id, client_secret, text, file_path, file_name
# output(return) : API 사용 실행 결과


def tts(client_id, client_secret, text, file_path, file_name):
    result = ''

    # =========B. Request=========
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    data = {"speaker": "nara", "volume": 0, "speed": 0,
            "pitch": 0, "format": "mp3", "text": text, }
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "X-NCP-APIGW-API-KEY-ID": client_id,
               "X-NCP-APIGW-API-KEY": client_secret, }

    r = requests.post(url, headers=headers, data=data)

    # =========C. Response=========
    # 응답결과 저장할 파일 경로 path 설정하기
    dir_parts = [file_path, file_name]
    path = Path.cwd().joinpath(*dir_parts)

    if(r.status_code == requests.codes.ok):
        print("------TTS mp3 저장 시작------")
        with open(path, 'wb') as f:
            f.write(r.content)
        result = f"TTS mp3 저장 완료 : {path}"
    else:
        result = f"Error: {r.status_code} / {r.content.decode('utf-8')}"

    return result


# API 실행 결과 확인하기
result_msg = tts(client_id, client_secret, text, file_path, file_name)
print(result_msg)

# 매일매일 뉴스 요약 오디오북
# 특정일자의 뉴스 요약 데이터 -> 오디오 파일
# 특정일자 뉴스 요약 데이터 조회
# 1000자 단위로 합치기(1000자 이내만 요청 가능)
# 오디오 파일
