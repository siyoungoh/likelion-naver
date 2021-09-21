# -*- coding: utf-8 -*-
import requests
import json

sample_title = "7일 V리그 여자 드래프트, 주목할 선수는 누구…신생팀 페퍼가 5명 우선 지명"
sample_txt = "[스포츠경향] 한국프로배구 여자부 신인 드래프트에 도전한 43명이 떨리는 마음으로 7개 구단의 선택을 기다린다. 한국배구연맹(KOVO)은 7일 오후 2시 서울시 강남구 청담 리베라 호텔에서 2021~2022 KOVO 여자 신인선수 드래프트를 개최한다. KOVO는 1일 43명의 드래프트 신청자 명단을 공개했다. 18세 이하 대표 출신인 강릉여고 박수연(레프트)과 대구여고 박사랑(세터), 국가대표 상비군을 지낸 세화여고 김주희(레프트), 차유정(센터·레프트) 등이 프로구단의 관심을 얻고 있다. 드래프트 참가자 중 키가 가장 큰 중앙여고 센터 이예담(185.1㎝), 공격력이 뛰어난 일신여상 레프트 박은서도 주목해야 할 선수다. 2021~2022시즌부터 V리그에 참여하는 신생팀 페퍼저축은행은 우선 지명권 6장 중 5장을 쓴다. 페퍼저축은행은 자유계약선수(FA) 하혜진을 영입하며 원소속구단 한국도로공사에 지난 시즌 연봉 200%인 2억원과 신인드래프트 6명 우선 지명권 중 4순위 지명권을 넘겼다. 페퍼저축은행이 우선 지명을 마치면, 지난 시즌 최종순위 역순을 기준으로 현대건설 35%, KGC인삼공사 30%, 한국도로공사 20%, IBK기업은행 9%, 흥국생명 4%, GS칼텍스 2%의 확률로 추첨해 지명 순위를 정한다. 이번 신인 드래프트는 정부의 사회적 거리두기 지침으로 인해 비대면으로 연다. 드래프트를 신청한 선수들은 현장이 아닌 온라인 화상 프로그램으로 참여한다. 남자 신인선수 드래프트는 9월 28일에 열린다.이정호 기자 alpha@kyunghyang.com"

# print(len(sample_txt))
# print(sample_txt)


# =====request=======
client_id = "내 인공지능 API client_id"
client_secret = "내 인공지능 API client_secret"

headers = {"X-NCP-APIGW-API-KEY-ID": client_id,
           "X-NCP-APIGW-API-KEY": client_secret,
           "Content-Type": "application/json"}

document = {"title": sample_title, "content": sample_txt}
option = {"language": "ko", "model": "news", "tone": 0, "summaryCount": 2}

data = {"document": document, "option": option}

# print(data)

r = requests.post("https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize",
                  headers=headers, data=json.dumps(data))

result = ""
if r.status_code == requests.codes.ok:
    result_response = json.loads(r.content)
    # print(result_response)
    result = result_response["summary"]
else:
    print(f"Error Code: {r.status_code}")
    print(f"Error Message: {r.text}")

# print(len(result), result)
