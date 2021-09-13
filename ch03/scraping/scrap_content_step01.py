import requests
from bs4 import BeautifulSoup
from requests.exceptions import SSLError

# ==========1. GET Request==========
# Request 설정값(HTTP Msg) - Desktop Chrome 인 것처럼
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# sports.news URL
# url = 'https://sports.news.naver.com/news.nhn?oid=382&aid=0000930543'
# url = 'https://sports.news.naver.com/news.nhn?oid=530&aid=00000070'
# '#newsEndContents'

# navernews 유형 01
# url = 'https://news.naver.com/main/read.naver?mode=LSD&mid=sec&sid1=106&oid=008&aid=0004639637'
# '#articeBody'

# navernews 유형 02
url = 'https://news.naver.com/main/read.naver?mode=LSD&mid=sec&sid1=103&oid=023&aid=0003637624'
# '#articleBodyContents'

# 제외 url - HTML 구조 다시 보기 필요
# url = 'https://news.mtn.co.kr/newscenter/news_viewer.mtn?gidx=2021090117471793052'

# 예외처리 후
try:
    data = requests.get(url, headers=headers)
except SSLError as e:
    # print(e)
    data = requests.get(url, headers=headers, verify=False)

# ========2. 특정 요소 접근하기===========
# BeautifulSoup4 사용해서 html 요소에 각각 접근하기 쉽게 만듦.
soup = BeautifulSoup(data.text, 'html.parser')
content = ''

# ======== sports_news =========
# sport_content = soup.select_one('#newsEndContents')
# print(sport_content)

# for tag in sport_content(['div', 'span', 'p', 'br']):
#     tag.decompose()
# sport_result = sport_content.text.strip()
# print(sport_result)

# =====naver news 유형 01 ==========
# naver_content01 = soup.select_one('#articeBody')

# for tag in naver_content01(['div', 'span', 'p', 'br', 'script']):
#     tag.decompose()

# result_naver_content01 = naver_content01.text.strip()
# print(result_naver_content01)

# =====naver news 유형 02 ==========
naver_content02 = soup.select_one('#articleBodyContents')

for tag in naver_content02(['div', 'span', 'p', 'br', 'script']):
    tag.decompose()

result_naver_content02 = naver_content02.text.strip()
print(result_naver_content02)
