# -*- coding: utf-8 -*-
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz
from pathlib import Path
import requests
import boto3

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

# object storage 용 정보
# 계정 API 인증 정보 -
api_info = {'access_key': '내 계정 access_key',
            'secret_key': '내 계정 secret_key'}
local_info = {'local_folder': 'mp3_folder', 'local_file': 'default.mp3'}
bucket_info = {'bucket_name': '내 버킷 이름',
               'upload_folder': 'news', 'upload_file': 'default.mp3'}

file_path = local_info['local_folder']


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
    result = {'status': 'ok', 'msg': 'default'}

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
        result['msg'] = f"TTS mp3 저장 완료 : {path}"

    else:
        result['status'] = r.status_code
        result['msg'] = r.content.decode('utf-8')

    return result


def upload_storage(api_info, local_info, bucket_info):
    """
    object storage 에 파일 업로드 (ACL:public-read 로 설정)
    :param: dict api_info / key: access_key, secret_key
    :param: dict local_info / key: local_folder, local_file
    :param: dict bucket_info / key: bucket_name, upload_folder, upload_file
    """
    service_name = 's3'
    endpoint_url = 'https://kr.object.ncloudstorage.com'
    region_name = 'kr-standard'

    s3 = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=api_info['access_key'],
                      aws_secret_access_key=api_info['secret_key'])

    dir_parts = [local_info['local_folder'], local_info['local_file']]
    local_path = str(Path.cwd().joinpath(*dir_parts))
    # print(type(local_path), local_path)

    # object storage 에 업로드할 파일 정보
    upload_path = f'{bucket_info["upload_folder"]}/{bucket_info["upload_file"]}'

    s3.upload_file(local_path, bucket_info['bucket_name'], upload_path,
                   ExtraArgs={'ACL': 'public-read'})


# 이전 특정일자 정보 가져오기
target_date = cal_datetime(2)
# 연-월-일 문자열 형태로 반환
target_date_str = target_date['date_st'].strftime("%Y-%m-%d")

# =====Read from DB=======

# item 갯수 확인
date_cnt_items = collection.count_documents({
    'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}})
print(date_cnt_items)

page_num = (date_cnt_items // 4) + 1

# 4개씩 데이터 가져오기
for i in range(page_num):
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
    # tts 로 만들기
    result = tts(client_id=client_id, client_secret=client_secret,
                 text=summary_contents, file_path=file_path, file_name=file_name)

    # 파일 경로 설정
    local_info['local_file'] = file_name
    bucket_info['upload_file'] = file_name
    bucket_info['upload_folder'] = target_date_str

    if result['status'] == 'ok':
        upload_storage(api_info=api_info, local_info=local_info,
                       bucket_info=bucket_info)
