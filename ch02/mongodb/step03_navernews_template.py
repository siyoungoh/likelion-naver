# 사전작업
# 1. 가상환경에 pymongo 패키지 설치! (되어있으면 상관없음)
# 2. 네이버 클라우드 서버의  공인 ip(public ip) 확인하기!
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
# news api 사용하기 위한 패키지
import json
import requests


def get_news(keywords, client_id, client_secret):
    """
    네이버 검색 뉴스 API 사용해 특정 키워드들의 뉴스 검색
    :params list keywords: 키워드 리스트
    :params str client_id: 인증정보
    :params str client_secret: 인증정보
    :return news_items : API 검색 결과 중 뉴스 item들
    :rtype list
    """
    news_items = []

    for keyword in keywords:
        # B. API Request
        # B-1. 준비하기 - 설정값 세팅
        url = 'https://openapi.naver.com/v1/search/news.json'

        sort = 'date'  # sim: similarity 유사도, date: 날짜
        display_num = 100
        start_num = 1

        params = {'display': display_num, 'start': start_num,
                  'query': keyword.encode('utf-8'), 'sort': sort}
        headers = {'X-Naver-Client-Id': client_id,
                   'X-Naver-Client-Secret': client_secret, }

        # B-2. API Request
        r = requests.get(url, headers=headers,  params=params)

        # C. Response 결과
        # C-1. 응답결과값(JSON) 가져오기
        # Request(요청)이 성공하면
        if r.status_code == requests.codes.ok:
            result_response = json.loads(r.content.decode('utf-8'))

            result = result_response['items']
            # for item in result :
            #     print('========single item===========')
            #     # print(item)
            #     print(item['title'])

        # Request(요청)이 성공하지 않으면
        else:
            print('request 실패!')
            failed_msg = json.loads(r.content.decode('utf-8'))
            print(failed_msg)

        news_items.extend(result)

    return news_items


# =======NEWS API 불러오기 TEST==========
# API Request 설정값
client_id = '내 client id'
client_secret = '내 client secret'
keywords = ['KOVO', '여자 배구']  # 뉴스 검색할 키워드

docs = get_news(keywords, client_id, client_secret)
print(len(docs))  # 총 뉴스 갯수 출력
# print(docs) # 뉴스 정보 출력

# =======DB 저장==========
# Connect to MongoDB server
my_ip = ' 서버 public ip'
client = MongoClient('mongodb://likelion:wearethefuture' + '@' + my_ip, 27017)
db = client['likelion']
collection = db['navernews_test']  # unique key 설정할 collection

# 뉴스 link field 에 unique key 설정 - unique 하게 유일한 row 데이터만 입력됨.
collection.create_index([('link', 1)], unique=True)

try:
    collection.insert_many(docs, ordered=False)

except BulkWriteError as bwe:
    print('중복 데이터 발생')
