import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from requests.exceptions import SSLError

my_ip = '내서버 ip'
db_name = 'likelion'
collection_name = 'navernews_copy'
username = 'likelion'
password = '비밀번호'

client = MongoClient(host=my_ip, port=27017,
                     username=username, password=password)
db = client[db_name]
collection = db[collection_name]


# 작은 갯수로 테스트
news_items = list(collection.find(
    {'naverNews': 'Y'}, {'_id': False}).limit(10))
# naver_news_items = list(collection.find({'naverNews': 'Y'}, {'_id': False}))
# news_items = list(collection.find({}, {'_id': False}))


def scrape_image_url(url):
    # ref : https://unsplash.com/photos/tAcoHIvCtwM
    image_url = 'https://images.unsplash.com/photo-1588492069485-d05b56b2831d?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1051&q=80'

    # Request 설정값(HTTP Msg) - Desktop Chrome 인 것처럼
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    # URL request 해서 HTML 코드를 response 받음.
    try:
        data = requests.get(url, headers=headers)
    except SSLError as e:
        data = requests.get(url, headers=headers, verify=False)

    # BeautifulSoup4 사용해서 html 요소에 각각 접근하기 쉽게 만듦.
    soup = BeautifulSoup(data.text, 'html.parser')

    # image url 가져오기 - og:image
    og_img_el = soup.select_one('meta[property="og:image"]')

    image_url = og_img_el['content']
    if not og_img_el:
        return image_url

    if 'http' not in image_url:
        image_url = 'http:' + image_url

    return image_url


def scrape_content(url):
    content = ''

    # Request 설정값(HTTP Msg) - Desktop Chrome 인 것처럼
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    if 'sports.news.naver.com' in url:
        raw_news = soup.select_one('#newsEndContents')
        if not raw_news:
            return content


        for tag in raw_news(['div', 'span', 'p', 'br']):
            tag.decompose()
        content = raw_news.text.strip()

    elif 'news.naver.com' in url:
        raw_news = soup.select_one('#articeBody') or soup.select_one(
            '#articleBodyContents')
        if not raw_news:
            return content

        for tag in raw_news(['div', 'span', 'p', 'br', 'script']):
            tag.decompose()

        content = raw_news.text.strip()

    return content


for item in news_items:
    link = item['link']
    item['imageUrl'] = scrape_image_url(link)

    if item['naverNews'] == 'Y':
        content = scrape_content(link)
        item['content'] = content
        if content is not '':
            item['content'] = content
        else:
            item['content'] = item['description']
        # 줄여서 쓰기
        # item['content'] = content if content is not '' else item['description']
        # 예. "짝수" if num % 2 == 0 else "홀수"

    else:
        item['content'] = item['description']

    # print(item)

    collection.update_one(
        {'link': link}, {'$set': {'content': item['content']}})
    collection.update_one(
        {'link': link}, {'$set': {'imageUrl': item['imageUrl']}})
