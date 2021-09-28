# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
from pathlib import Path
import json
from pymongo import MongoClient
import pytz
import requests
import boto3


with open('config_voice.json', 'r') as f:
    config = json.load(f)
voice_storage_info = config['VOICE_API']
db_info = config['DB']
local_info = config['LOCAL']
bucket_info = config['BUCKET']
storage_info = config['STORAGE']
before_date = config['BEFORE_DATE']

file_folder = local_info['local_folder']
client = MongoClient(host=db_info['my_ip'], port=27017,
                     username=db_info['username'], password=db_info['password'])
db = client[db_info['db_name']]
collection = db[db_info['collection_name']]


def cal_datetime_utc(before_date, timezone='Asia/Seoul'):
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


def cal_datetime_kst(before_date, timezone='Asia/Seoul'):
    '''
    현재 일자에서 before_date 만큼 이전의 일자를 일자+시작시간/끝시간으로 변환하여 반환
    :param before_date: 이전일자
    :param timezone: 타임존
    :return: 해당일의 시작시간(date_st)과 끝 시간(date_end)
    :rtype: dict of datetime object
    '''
    today = pytz.timezone(timezone).localize(datetime.now())
    target_date = today - timedelta(days=before_date)

    # 같은 일자 same date 의 00:00:00 로 변경
    start = target_date.replace(hour=0, minute=0, second=0,
                                microsecond=0)

    # 같은 일자 same date 의 23:59:59 로 변경
    end = target_date.replace(
        hour=23, minute=59, second=59, microsecond=999999)

    return {'date_st': start, 'date_end': end}


def remove_file(file_folder, file_name):
    """
    파일 삭제
    :param: file_folder: 파일 폴더
    :param: file_name: 파일 이름
    :result: 처리 결과 메시지
    """
    result = ''

    dir_parts = [file_folder, file_name]
    path = Path.cwd().joinpath(*dir_parts)
    # 파일이 존재하면 삭제
    try:
        if os.path.isfile(path):
            os.remove(path)
            result = f'{path} 파일이 삭제되었습니다.'
        else:
            result = f'Error: {path} 를 찾을 수 없습니다.'
    except OSError as e:
        result = f'Error: {e.filename} - {e.strerror}.'

    return result


def tts(client_id, client_secret, text, file_folder, file_name):
    """
    CLOVA VOICE API 사용해 텍스트를 음성파일로 변환
    :param: client_id: 인증 정보
    :param: client_secret: 인증 정보
    :param: text: 변환할 텍스트
    :param: file_folder: 저장할 파일 폴더
    :param: file_name: 저장할 파일 이름
    """
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
    dir_parts = [file_folder, file_name]
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


def upload_storage(storage_info, local_info, bucket_info):
    """
    object storage 에 파일 업로드 (ACL:public-read 로 설정)
    :param: dict storage_info / key: access_key, secret_key
    :param: dict local_info / key: local_folder, local_file
    :param: dict bucket_info / key: bucket_name, upload_folder, upload_file
    """
    service_name = 's3'
    endpoint_url = 'https://kr.object.ncloudstorage.com'
    region_name = 'kr-standard'

    s3 = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=storage_info['access_key'],
                      aws_secret_access_key=storage_info['secret_key'])

    dir_parts = [local_info['local_folder'], local_info['local_file']]
    local_path = str(Path.cwd().joinpath(*dir_parts))
    # print(type(local_path), local_path)

    # object storage 에 업로드할 파일 정보
    upload_path = f'{bucket_info["upload_folder"]}/{bucket_info["upload_file"]}'

    s3.upload_file(local_path, bucket_info['bucket_name'], upload_path,
                   ExtraArgs={'ACL': 'public-read'})


# 이전 특정일자(UTC) 정보 가져오기
target_date = cal_datetime_utc(before_date)
# 폴더명을 위해 KST 연-월-일 문자열 형태로 반환
kst_target_date = cal_datetime_kst(before_date)['date_st'].strftime("%Y-%m-%d")

# =====Read from News DB=======

# item 갯수 확인
date_cnt_items = collection.count_documents({
    'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}})
# print(date_cnt_items)

# Voice API 글자수 1000자 제한때문에 4개씩 summary 데이터를 묶어서 음성 변환
# Pagenation - 4로 데이터가 나누어 떨어지지 않을 경우, 나머지 데이터를 가져오기 위해서 1을 더해서 그 다음 페이지까지 가져오도록 작업
page_num = (date_cnt_items // 4) + (0 if date_cnt_items % 4 == 0 else 1)
# print(page_num)

for i in range(page_num):
    file_name = f'{kst_target_date}_{i+1}.mp3'

    skip_num = i * 4
    print(f'======{i}번째 진행. {skip_num}번째 이후부터======')
    # 특정 일자의 뉴스 데이터 이른 시간순(sort('date',1)으로 4개씩 가져오기
    limit_items = list(collection.find(
        {'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}}, {'_id': False}).sort('date', 1).skip(skip_num).limit(4))

    # =====TEST : limit_items 데이터 확인 ======
    # print(
    #     f"{limit_items[0]['pubDate']} / {limit_items[0]['date']}")
    # print(limit_items[0]['summary'])
    # print(
    #     f"{limit_items[len(limit_items)-1]['pubDate']} / {limit_items[len(limit_items)-1]['date']}")
    # print(limit_items[len(limit_items)-1]['summary'])

    summary_contents = ''
    # 각 item summary 글자수 확인용 리스트 - voice API 최대 1000자 제한
    for item in limit_items:
        # 999자까지만 출력
        # summary_contents = (f'{i+1}번째 뉴스 묶음.' +
        #                     '다음 뉴스.'.join(item['summary'] for item in limit_items))[:999]
        summary_contents = (f'다음 뉴스.'.join(
            item['summary'] for item in limit_items))[: 999]

    # =========voice 변환하기=========
    print(f'======{len(summary_contents)}======')
    # tts 로 만들기
    result = tts(client_id=voice_storage_info['client_id'], client_secret=voice_storage_info['client_secret'],
                 text=summary_contents, file_folder=file_folder, file_name=file_name)

    # =========Object Storage 에 업로드=========
    # 파일 경로 설정
    local_info['local_file'] = file_name
    bucket_info['upload_file'] = file_name
    bucket_info['upload_folder'] = kst_target_date

    # Voice 변환이 정상이면 업로드하기
    if result['status'] == 'ok':
        upload_storage(storage_info=storage_info, local_info=local_info,
                       bucket_info=bucket_info)
        # 저장공간 관리를 위해 storage 업로드 후 파일 삭제
        result_msg = remove_file(
            local_info['local_folder'], local_info['local_file'])
        print(result_msg)
