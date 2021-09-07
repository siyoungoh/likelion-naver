# 사전작업
# news api 사용하기 위한 패키지
import json
import requests

# =======NEWS API 불러오기==========
# API Request 설정값
client_id = '내 client id'
client_secret = '내 client secret'

keywords = ['KOVO', '여자 배구']  # 뉴스 검색할 키워드

news_items = []

for keyword in keywords:
    # B. API Request
    # B-1. 준비하기 - 설정값 세팅
    url = 'https://openapi.naver.com/v1/search/news.json'

    sort = 'date'  # sim: similarity 유사도, date: 날짜

    # ========일부 데이터만 탐색해보기========
    display_num = 10  # 탐색할 개수
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

# ===========데이터 탐색하기==========
        result = result_response['items']
        for item in result:
            # print('========single item===========')
            # print(item['title'])
            originallink = item['originallink']
            link = item['link']
            # print(originallink, link)

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

print(news_items[0])
print(news_items[1])
