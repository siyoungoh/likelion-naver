# -*- coding: utf-8 -*-
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz
from pathlib import Path
import requests

# API 인증 정보
client_id = "내 client_id"
client_secret = "내 client_secret"

my_ip = '내 public ip'
db_name = 'likelion'
collection_name = 'navernews'
# collection_name = 'navernews_copy'
username = 'likelion'
password = 'wearethefuture'

client = MongoClient(host=my_ip, port=27017,
                     username=username, password=password)
db = client[db_name]
collection = db[collection_name]

file_path = 'mp3_folder'

# =====Date function=======


def cal_datetime(before_date, timezone='Asia/Seoul'):
    '''
    현재 일자에서 before_date 만큼 이전의 일자를 UTC 시간으로 변환하여 반환
    :param before_date: 이전일자
    :param timezone: 타임존
    :return: UTC 해당일의 시작시간(date_st)과 끝 시간(date_end)
    :rtype: dict of datetime object
    :Example:
    2021-09-13 KST 에 get_date(1) 실행시,
    return은 {'date_st': datetype object 형태의 '2021-09-11 15:00:00+00:00'), 'date_end': datetype object 형태의 '2021-09-12 14:59:59.999999+00:00'}
    '''
    today = pytz.timezone(timezone).localize(datetime.now())
    target_date = today - timedelta(days=before_date)

    # 같은 일자 same date 의 00:00:00 로 변경 후, UTC 시간으로 바꿈
    start = target_date.replace(hour=0, minute=0, second=0,
                                microsecond=0).astimezone(pytz.UTC)

    # 같은 일자 same date 의 23:59:59 로 변경 후, UTC 시간으로 바꿈
    end = target_date.replace(
        hour=23, minute=59, second=59, microsecond=999999).astimezone(pytz.UTC)

    return {'date_st': start, 'date_end': end}


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


# 이전 특정일자 정보 가져오기
target_date = cal_datetime(2)
# 연-월-일 문자열 형태로 반환
target_date_str = target_date['date_st'].strftime("%Y-%m-%d")
# print(target_date_str)

# =====Read from DB=======

# item 갯수 확인
date_cnt_items = collection.count_documents({
    'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}})
print(date_cnt_items)

page_num = (date_cnt_items // 4) + 1
# print(page_num)

# 4개씩 데이터 가져오기
for i in range(page_num):
    # file_name = f'{i+1}.mp3'
    # 파일에 날짜 정보까지 추가하기
    file_name = f'{target_date_str}_{i+1}.mp3'

    skip_num = i * 4
    print(f'======{i}번째 진행. {skip_num}번째 이후부터======')
    limit_items = list(collection.find(
        {'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}}, {'_id': False}).skip(skip_num).limit(4))

    summary_contents = ''
    # 각 item summary 글자수 확인용 리스트 - voice API 최대 1000자 제한
    for item in limit_items:
        # 999자까지만 출력
        summary_contents = (f'{i+1}번째 뉴스 묶음.' +
                            '다음 뉴스.'.join(item['summary'] for item in limit_items))[:999]

    # TODO: voice 변환하기
    print(f'======{len(summary_contents)}======')
    # print(summary_contents)
    # tts(client_id=client_id, client_secret=client_secret,
    #     text=summary_contents, file_path=file_path, file_name=file_name)

    # 만들어지지 않는 데이터가 있다? -> tts 실행결과 파악하기
    # tts 로 만들기
    result = tts(client_id=client_id, client_secret=client_secret,
                 text=summary_contents, file_path=file_path, file_name=file_name)
    print(result)
