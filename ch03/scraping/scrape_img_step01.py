import requests
from bs4 import BeautifulSoup

# ==========1. GET Request==========
# 정상 URL
# url = 'https://sports.news.naver.com/news.nhn?oid=382&aid=0000930543'
# url = 'https://sports.news.naver.com/news.nhn?oid=530&aid=0000007040'
# url = 'https://news.naver.com/main/read.naver?mode=LSD&mid=sec&sid1=106&oid=008&aid=0004639637'
# url = 'https://news.naver.com/main/read.naver?mode=LSD&mid=sec&sid1=103&oid=023&aid=0003637624'

# 예외처리 필요 url
url = 'https://news.mtn.co.kr/newscenter/news_viewer.mtn?gidx=2021090117471793052'


# Request 설정값(HTTP Msg) - Desktop Chrome 인 것처럼 
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# URL request 해서 HTML 코드를 response 받음.
data = requests.get(url, headers=headers)

# ========2. 특정 요소 접근하기===========
# BeautifulSoup4 사용해서 html 요소에 각각 접근하기 쉽게 만듦.
soup = BeautifulSoup(data.text, 'html.parser')

image_url = ''

# image url 가져오기 - og:image
image_url = soup.select_one('meta[property="og:image"]')['content']
print(image_url)