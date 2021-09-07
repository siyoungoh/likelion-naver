# news api 기본 사용
import json
import requests

# =====함수 설계======
# 기능 : 네이버 검색 뉴스 API 사용해 특정키워드들의 뉴스 검색
# 함수명: get_news
# input(params) : keywords, client_id, client_secret
# output(return) : 키워드로 검색된 뉴스 정보 list


def get_news(keywords, client_id, client_secret):
    news_items = []

    for keyword in keywords:
        # 뉴스 검색해오기
        sort = 'date'  # sim: similarity 유사도, date: 날짜
        display_num = 2
        start_num = 1

        # B. API Request
        # B-1. 준비하기 - 설정값 세팅
        url = 'https://openapi.naver.com/v1/search/news.json'
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


# API Request 에 필요한 인증 정보 가져오기
client_id = '내 client id'
client_secret = '내 client secret'

keywords = ['KOVO', '여자 배구']

# =======TEST==========
result_all = get_news(keywords, client_id, client_secret)
print(len(result_all))
print(result_all)
