from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import boto3
from datetime import datetime, timedelta
import pytz
import json


app = Flask(__name__)

# ======Flask 에 필요한 설정 정보 config.json 에서 가져오기======
with open('config.json', 'r') as f:
    config = json.load(f)
bucket_info = config['BUCKET']
storage_info = config['STORAGE']
db_info = config['DB']
before_date = config['BEFORE_DATE']
# ====TEST : 설정 불러오는지 확인========
# print(db_info, bucket_info, before_date)


@app.route("/")
def home():
    """
    화면에 접속
    """
    return render_template("index.html")


@app.route("/api/audios")
def get_audios():
    """
    audio 파일 보내기
    """

    # STEP 01. audio file url 직접 입력해서 테스트
    # STEP 02. 특정 이름의 폴더의 url 가져오기
    # STEP 03. 날짜 계산 함수를 사용해 특정 일자 폴더의 url 가져오기

    result = {}
    # result['status'] = 'success'

    # ======before_date일 전 날짜 형태로 폴더명 만들기=======
    target_date = cal_datetime_kst(before_date)
    # 연-월-일 문자열 형태로 반환
    target_date_str = target_date['date_st'].strftime("%Y-%m-%d")
    folder = target_date_str
    # print(f'audio folder: {folder}')
    # print(get_storage_filelist(bucket_info, folder))

    result['audio_list'] = get_storage_filelist(bucket_info, folder)

    # print(result)

    # ========STEP 01. audio file url 직접 입력해서 테스트========
    # 내 버킷에 저장된 파일 url 사용하기
    # result['audio_list'] = [
    #     {
    #         'source': 'https://kr.object.ncloudstorage.com/내버킷명/2021-09-12/2021-09-12-0.mp3'
    #     },
    #     {
    #         'source': 'https://kr.object.ncloudstorage.com/내버킷명/2021-09-12/2021-09-12-1.mp3'
    #     }
    # ]

    return jsonify(result)


@app.route("/api/news")
def send_news():
    """
    전날 뉴스 데이터 가져오기
    """

    # TODO : 특정 일자 데이터 조회하기
    client = MongoClient(host=db_info['my_ip'], port=27017,
                         username=db_info['username'], password=db_info['password'])
    db = client[db_info['db_name']]
    collection = db[db_info['collection_name']]

    # ======before_date 일 전 데이터 조회하기=======
    target_date = cal_datetime_utc(before_date)
    # print(f'UTC targetdate: {target_date}')

    news_items = list(collection.find(
        {'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}}, {'_id': False}).sort('date', 1))
    # print(news_items)

    return jsonify({"news": news_items})


def get_storage_filelist(bucket_info, folder):
    """
    내 bucket 에서 특정 폴더에 있는 파일 목록을 반환
    :param bucket_info: bucket 정보
    :param folder: bucket안 특정 폴더명
    :return: 특정 폴더에 있는 파일 url 목록
    :rtype: list of dictionaries
    """

    service_name = 's3'
    endpoint_url = 'https://kr.object.ncloudstorage.com/'
    # bucket_url : https://kr.object.ncloudstorage.com/내버킷명/
    bucket_url = endpoint_url + bucket_info['bucket_name'] + '/'

    s3 = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=storage_info['access_key'],
                      aws_secret_access_key=storage_info['secret_key'])

    result = []
    objects = s3.list_objects_v2(
        Bucket=bucket_info['bucket_name'], Prefix=folder)

    entries = objects.get('Contents') or []

    for entry in entries:
        if entry['Size'] != 0:
            result.append({'source': bucket_url + entry['Key']})

    return result


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
    현재 일자에서 before_date 만큼 이전의 일자의 시작시간,끝시간 반환
    :param before_date: 이전일자
    :param timezone: 타임존
    :return: 해당일의 시작시간(date_st)과 끝 시간(date_end)
    :rtype: dict of datetime object
    :Example:
    2021-09-13 KST 에 get_date(1) 실행시,
    return은 {'date_st': datetype object 형태의 '2021-09-12 00:00:00+09:00'), 'date_end': datetype object 형태의 '2021-09-12 23:59:59.999999+90:00'}
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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
