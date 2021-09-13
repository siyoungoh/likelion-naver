import requests
from bs4 import BeautifulSoup
from requests.exceptions import SSLError

# 함수 설계하기
# 1. 함수명 / 기능: scrap_content
# 2. input(param): url
# 3. output(return): str content 기사본문, 없으면 빈 문자열

def scrap_content(url):
    """
    네이버 뉴스에서 기사 본문 scraping 해오기
    :param url: 네이버 뉴스 기사 url
    :return content 기사본문 없으면 빈 문자열
    :rtype: str
    """

    # ==========1. GET Request==========
    # Request 설정값(HTTP Msg) - Desktop Chrome 인 것처럼 
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

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

    if 'sports.news.naver' in url:
        # ======== sports_news =========
        sport_content = soup.select_one('#newsEndContents')

        for tag in sport_content(['div', 'span', 'p', 'br']):
            tag.decompose()
        content = sport_content.text.strip()
    elif 'news.naver.com' in url:
        #========== news_naver ==========
        naver_content = soup.select_one('#articeBody') or soup.select_one('#articleBodyContents')

        for tag in naver_content(['div', 'span', 'p', 'br', 'script']):
            tag.decompose()
        content = naver_content.text.strip()

    return content

#=======TEST==========

# sports.news URL
# url = 'https://sports.news.naver.com/news.nhn?oid=382&aid=0000930543'
# url = 'https://sports.news.naver.com/news.nhn?oid=530&aid=0000007040'

# navernews 유형 01
# url = 'https://news.naver.com/main/read.naver?mode=LSD&mid=sec&sid1=106&oid=008&aid=0004639637'
# navernews 유형 02
url = 'https://news.naver.com/main/read.naver?mode=LSD&mid=sec&sid1=103&oid=023&aid=0003637624'

result = scrap_content(url)
print(result)