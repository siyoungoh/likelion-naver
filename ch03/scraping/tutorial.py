import requests
from bs4 import BeautifulSoup

# ==========1. GET Request==========
# Request 설정값(HTTP Msg) - Desktop Chrome 인 것처럼
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
url = 'https://elastic-hugle-d528b6.netlify.app/demo/simple.html'

# URL request 해서 HTML 코드를 response 받음.
data = requests.get(url, headers=headers)
# print(data.text)

# ========2. 특정 요소 접근하기===========

# BeautifulSoup4 사용해서 html 요소에 각각 접근하기 쉽게 만듦.
soup = BeautifulSoup(data.text, 'html.parser')
# print(soup)
# data.text 와 soup 은 타입이 다릅니다! 접근쉽게 형태를 바꿈.
# print(f'data.text: {type(data.text)} / soup : {type(soup)}')

# HTML의 특정 element요소만 가지고 옴.
# p_el = soup.select_one('body > p')
# print(p_el)
# print('text만 가정져오기:' + p_el.text)

# selector 이용 - id 는 유일하므로 더 확실!
# news_el = soup.select_one('#news')
# print(news_el)
# print('text만 가져오기:' + news_el.text)

# 여러 요소 가져오기
# div_els = soup.select('div')
# print(div_els)
# # text만 가져오기
# for div_el in div_els:
#     print(div_el.text)

# 여러 요소 가져오기 - selector class
# cool_els = soup.select('.cool')
# # print(cool_els)
# # text만 가져오기
# for cool_el in cool_els:
#     print(cool_el.text)

# 첫번째 요소만 가져오게 됨
# first_div_els = soup.select_one('div')
# print(first_div_els)
# print(first_div_els.text)

# copy selector 사용 - div 4번째 자식 요소
# we_cool_el = soup.select_one('body > div:nth-child(4)')
# print(we_cool_el)
# print(we_cool_el.text)

# a_el = soup.select_one('body > a')
# print(a_el)

# news
# news_el_selector = soup.select_one('#news')
# print(news_el_selector)

# og:image 가져오기
# head > meta:nth-child(7)

og_img_el = soup.select_one('meta[property="og:image"]')
# print(og_img_el)

image_url = og_img_el['content']
# print(image_url)

og_image_url = soup.select_one('meta[property="og:image"]')['content']
# print(og_image_url)
