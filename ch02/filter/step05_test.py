from pymongo import MongoClient
from pymongo.errors import BulkWriteError

# Connect to MongoDB server
host = ' 서버 public ip'
username = 'likelion'
password = 'wearethefuture'

db_name = 'likelion'
collection_name = 'naver_filter'

client = MongoClient(host=host, port=27017,
                     username=username, password=password)
db = client[db_name]
collection = db[collection_name]  # _filter

# naver news 아닌 뉴스 조회해보기
not_naver = list(collection.find({'naverNews': 'N'}, {'_id': False}))
# print(len(not_naver))
# print(not_naver[0])
# print(not_naver[1])

# naver news 페이지들 조회해보기
naver_news = list(collection.find({'naverNews': 'Y'}, {'_id': False}))
# print(len(naver_news))
# print(naver_news[0])
# print(naver_news[1])
