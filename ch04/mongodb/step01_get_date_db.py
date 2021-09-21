# -*- coding: utf-8 -*-
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz

"""
특정 일자 정보 DB 에서 가져오기
"""

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


# 이전 특정일자 정보 가져오기
target_date = cal_datetime(6)
# target_date = cal_datetime(2)

# =====Read from DB=======

# item 갯수 확인
# target_date['date_st'] 특정일자 00:00:00 ~ target_date['date_end'] 특정일자 23:59:59 의 게시글 갯수 확인
date_cnt_items = collection.count_documents({
    'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}})
print(date_cnt_items)


limit_items = list(collection.find(
    {'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}}, {'_id': False}).limit(100))

for item in limit_items:
    # print('==================')
    # print(item['summary'])
    # 각 summary 의 길이 확인하기 - voice api 1000자 글자수 제한
    print(len(item['summary']))

    # [300 200 200 300] [200 300 200]
    # 1000자 -> 1 audio file
    # 4개 summary 를 묶어서 -> 하나의 파일로 만들자!
