# news api 기본 사용
from pymongo import MongoClient, mongo_client
from pymongo.errors import BulkWriteError

import json
import requests


def get_news(keywords, client_id, client_secret):
    """
    - 네이버 검색 뉴스 API 사용해 특정 키워드들의 뉴스 검색
    - 수집 데이터를 기반으로 Naver News 페이지 존재 여부를 
    뉴스 item 항목에 추가

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
            for item in result:
                originallink = item['originallink']
                link = item['link']

                # ===naver news 페이지 여부 항목 추가====
                # naver news 페이지가 없다면
                if originallink == link:
                    item['naverNews'] = 'N'
                # naver news 페이지가 있다면
                else:
                    item['naverNews'] = 'Y'

        # Request(요청)이 성공하지 않으면
        else:
            print('request 실패!')
            failed_msg = json.loads(r.content.decode('utf-8'))
            print(failed_msg)

        news_items.extend(result)

    return news_items


def save_to_db(my_ip, username, password, db_name, collection_name, docs):
    """
    딕셔너리 리스트를 데이터베이스에 저장
    :params str my_ip: 데이터베이스 IP
    :params str username: 데이터베이스 계정
    :params str password: 데이터베이스 계정 비밀번호
    :params str db_name: 데이터베이스 이름
    :params str collection_name: 데이터베이스 collection 이름
    :params list docs: 데이터베이스 저장할 딕셔너리 리스트
    :return result: 데이터베이스 저장 결과
    :rtype dict
    """
    db_result = {'result': 'success'}

    client = MongoClient(host=my_ip, port=27017,
                         username=username, password=password)
    db = client[db_name]
    collection = db[collection_name]  # unique key 설정할 collection

    # 뉴스 link field 에 unique key 설정 - unique 하게 유일한 row 데이터만 입력됨.
    collection.create_index([('link', 1)], unique=True)

    try:
        collection.insert_many(docs, ordered=False)

    except BulkWriteError as bwe:
        db_result['result'] = 'Insert and Ignore duplicated data'

    return db_result


# =======NEWS API 불러오기 TEST==========
# API Request 설정값
client_id = '내 client id'
client_secret = '내 client secret'

keywords = ['KOVO', '여자 배구']  # 뉴스 검색할 키워드

docs = get_news(keywords, client_id, client_secret)

# =======DB 저장==========
# Connect to MongoDB server
host = ' 서버 public ip'
username = 'likelion'
password = 'wearethefuture'

db_name = 'likelion'
collection_name = 'naver_filter'

result = save_to_db(host, username, password, db_name, collection_name, docs)
print(result)
