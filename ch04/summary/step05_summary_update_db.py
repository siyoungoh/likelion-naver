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
# summary_items = list(collection.find(
#     {'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}}, {'_id': False}))

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

# # ========일부 데이터 가져오기 page number=========
# 전체 item 조회
# items = list(collection.find({}, {'_id': False}))

# =====예시=======
# 134 개 게시글
# page_num = (전체 갯수 134 // page 당 수 30) + 1
# 1page = 30개
# 1page : 1~30 번 = 1~ page번호 * 30
# 2page : 31~60 번 = (page번호-1 * 30)+1 ~ page번호 * 30 = (2-1) * 30 + 1 ~ 2 * 30 = 31~60
# 3page : 61~90 번 = (page번호-1 * 30)+1 ~ page번호 * 30 = (3-1) * 30 + 1 ~ 3 * 30 = 61~90
# 4page : 91~120 번
# 5page : 121~134 번

# item 갯수 확인
# date_cnt_items = collection.count_documents({
#     'date': {'$gte': target_date['date_st'], '$lte': target_date['date_end']}})
# cnt_items = collection.count_documents({})
# print(cnt_items)

# 순서대로 일부 item 조회
# 전체 횟수 확인하기
# page_num = (cnt_items // 30) + 1

# limit_items_30 = list(collection.find({}, {'_id': False}).limit(30))
# print(len(limit_items_30))

# 31~60 번
# test_items = list(collection.find({}, {'_id': False}).skip(30).limit(30))
# 965개 -> 960개 skip 하고 30개 보여줘 -> 960개 skip 하고 남은 나머지 갯수 조회
# test_items = list(collection.find({}, {'_id': False}).skip(960).limit(30))
# print(len(test_items))

# 데이터 일부 조회해오기
# page_num = (cnt_items // 30) + 1

# for i in range(page_num):
#     # print(i)
#     skip_num = i * 30
#     print(i, skip_num)
#     # 예. 61~90 번 -> skip(60).limit(30)
#     limit_items = list(collection.find(
#         {}, {'_id': False}).skip(skip_num).limit(30))
#     # for item in limit_items:
#     #     if 200 < len(item['content']) < 2000:
#     #         result = summary02(item['content'], client_id,
#     #                         client_secret) or item['description']
#     #     else:
#     #         # description -> summary field
#     #         result = item['description']

#     # # DB 에 업데이트
#     # collection.update_one(
#     #     {'link': item['link']}, {'$set': {'summary': result}})

#     print(f'limit_items: {len(limit_items)}')


# # 30개씩 가져와서 summary 한 후 데이터베이스에 업데이트하기 - 반복
# # for i in range(page_num+1):
# #     skip_num = i * 30
# #     # print(i, skip_num)
# #     limit_items = list(collection.find(
# #         {}, {'_id': False}).skip(skip_num).limit(30))

# #     # print(f'limit_items: {len(limit_items)}')

# #     for item in summary_items:
# #         if 200 < len(item['content']) < 2000:
# #             result = summary02(item['content'], client_id,
# #                                client_secret) or item['description']
# #         else:
# #             # description -> summary field
# #             result = item['description']

# #     # DB 에 업데이트
# #         collection.update_one(
# #             {'link': item['link']}, {'$set': {'summary': result}})
