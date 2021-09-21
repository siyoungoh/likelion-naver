# -*- coding: utf-8 -*-
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz

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


# =====Update to Date=======
# Update 한번에 하기
collection.update_many({}, [{'$set': {'date': {"$toDate": "$pubDate"}}}])

# =====Date function=======


def cal_datetime(before_date, timezone='Asia/Seoul'):
    """
    현재 일자에서 before_date 만큼 이전의 일자를 UTC 시간으로 변환하여 반환
    :param before_date: 이전일자
    :param timezone: 타임존
    :return: UTC 해당일의 시작시간(date_st)과 끝 시간(date_end) 
    :rtype: dict of datetime object
    :Example:
    2021-09-13 KST 에 get_date(1) 실행시,
    return은 {'date_st': datetype object 형태의 '2021-09-11 15:00:00+00:00'), 'date_end': datetype object 형태의 '2021-09-12 14:59:59.999999+00:00'}
    """
    today = pytz.timezone(timezone).localize(datetime.now())
    target_date = today - timedelta(days=before_date)

    # 같은 일자 same date 의 00:00:00 로 변경 후, UTC 시간으로 바꿈
    start = target_date.replace(hour=0, minute=0, second=0,
                                microsecond=0).astimezone(pytz.UTC)

    # 같은 일자 same date 의 23:59:59 로 변경 후, UTC 시간으로 바꿈
    end = target_date.replace(
        hour=23, minute=59, second=59, microsecond=999999).astimezone(pytz.UTC)

    return {'date_st': start, 'date_end': end}


target_date = cal_datetime(1)

# =====Read from Date=======

# taget_date_items = list(collection.find(
#     {'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}}, {'_id': False}))
# print(len(taget_date_items))

summary_items = list(collection.find(
    {'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}, 'naverNews': 'Y'}, {'_id': False}))
# print(len(summary_items))

summary_queue = []

for item in summary_items:
    if 200 < len(item['content']) < 2000:
        summary_queue.append(item)
        result = ''
        # TODO : Do summary
    else:
        # description -> summary field
        result = item['description']

print(len(summary_queue))
