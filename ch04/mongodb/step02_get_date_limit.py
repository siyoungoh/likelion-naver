# -*- coding: utf-8 -*-
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz

"""
특정 일자 정보 DB 에서 가져오기 - 4개씩
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

# =====Read from DB=======

# # ========일부 데이터 가져오기 page number=========
# =====pagenation 예시=======
# 134 개 게시글
# page_num = (전체 갯수 134 // page 당 수 30) + 1
# 1page 당 30개
# 1page : 1~30 번 = 1~ page번호 * 30
# 2page : 31~60 번 = (page번호-1 * 30)+1 ~ page번호 * 30 = (2-1) * 30 + 1 ~ 2 * 30 = 31~60
# 3page : 61~90 번 = (page번호-1 * 30)+1 ~ page번호 * 30 = (3-1) * 30 + 1 ~ 3 * 30 = 61~90
# 4page : 91~120 번
# 5page : 121~134 번

# item 갯수 확인
date_cnt_items = collection.count_documents({
    'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}})
print(date_cnt_items)

# 순서대로 일부 item 조회
# limit_items_30 = list(collection.find({}, {'_id': False}).limit(30))
# print(len(limit_items_30))

# 31~60 번
# test_items = list(collection.find({}, {'_id': False}).skip(30).limit(30))
# 965개 -> 960개 skip 하고 30개 보여줘 -> 960개 skip 하고 남은 나머지 갯수 조회
# test_items = list(collection.find({}, {'_id': False}).skip(960).limit(30))
# print(len(test_items))

# page 번호 - 몇 페이지까지 조회해와야 데이터를 다 가져올 수 있을지 계산하기
page_num = (date_cnt_items // 4) + 1
print(page_num)

# 4개씩 데이터 가져오기
for i in range(page_num):
    # print(i)
    skip_num = i * 4
    print(f'======{i}번째 진행. {skip_num}번째 이후부터======')
    limit_items = list(collection.find(
        {'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}}, {'_id': False}).skip(skip_num).limit(4))

    # 각 item summary 글자수 확인용 리스트 - voice API 최대 1000자 제한
    len_items = []
    # sum_len_items = 0

    for item in limit_items:
        # print(len(item['summary']))
        # TODO: voice 변환하기
        print(item['summary'])

        # 데이터 갯수 추가하기
        # len_items.append(len(item['summary']))
        # sum_len_items += len(item['summary'])

    # print(f'sum_len_items: {sum_len_items}')
    # print(len_items)
