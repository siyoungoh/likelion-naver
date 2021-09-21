# -*- coding: utf-8 -*-
import requests
import json
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz

client_id = '내 인공지능 API client_id'
client_secret = '내 인공지능 API client_secret'

my_ip = '내 public ip'
db_name = 'likelion'
# collection_name = 'navernews'
collection_name = 'navernews_copy'
username = 'likelion'
password = 'wearethefuture'

client = MongoClient(host=my_ip, port=27017,
                     username=username, password=password)
db = client[db_name]
collection = db[collection_name]

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


def summary02(txt, client_id, client_secret):
    '''
    텍스트 입력받아서 요약 - clova summary api
    :param: text 요약할 텍스트
    :param: client_id api 사용시 필요한 client_id
    :param: client_secret api 사용시 필요한 client_secret
    :return: summary_txt 요약된 텍스트
    :rtype: str
    '''

    headers = {'X-NCP-APIGW-API-KEY-ID': client_id,
               'X-NCP-APIGW-API-KEY': client_secret,
               'Content-Type': 'application/json'}

    document = {'content': txt}
    option = {'language': 'ko', 'model': 'news', 'tone': 0, 'summaryCount': 2}

    data = {'document': document, 'option': option}

    r = requests.post('https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize',
                      headers=headers, data=json.dumps(data))

    summary_txt = ''
    if r.status_code == requests.codes.ok:
        result_response = json.loads(r.content)
        summary_txt = result_response['summary']

    return summary_txt


target_date = cal_datetime(5)


# =====Read from Date=======
# 특정일자 item 만 조회
# summary_items = list(collection.find(
#     {'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}}, {'_id': False}))

# 전체 item 조회
summary_items = list(collection.find({}, {'_id': False}))

for item in summary_items:
    if 200 < len(item['content']) < 2000:
        result = summary02(item['content'], client_id,
                           client_secret) or item['description']
    else:
        # description -> summary field
        result = item['description']

    # DB 에 업데이트
    collection.update_one(
        {'link': item['link']}, {'$set': {'summary': result}})
