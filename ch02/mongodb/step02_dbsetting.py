# 사전작업
# 1. 가상환경에 pymongo 패키지 설치! (되어있으면 상관없음)
# 2. 네이버 클라우드 서버의  공인 ip(public ip) 확인하기!
from pymongo import MongoClient

"""
likelion 데이터베이스의 mbti, mbti_unique 콜렉션을 초기화하고, 데이터를 저장합니다.
각 콜렉션을 삭제하고 다시 새로운 정보(docs)를 저장합니다. 
"""

# Connect to MongoDB server
my_ip = ' 서버 public ip'
client = MongoClient('mongodb://likelion:wearethefuture@' + my_ip, 27017)
db = client['likelion']

docs = [{'name': 'lion', 'type': 'INFP', 'age': 3}, {'name': 'tiger', 'type': 'ENFJ', 'age': 3}, {'name': 'bear',
                                                                                                  'type': 'ENFJ', 'age': 5}, {'name': 'cat', 'type': 'INFP', 'age': 5}, {'name': 'dog', 'type': 'ENFP', 'age': 2}]

# =============== 작업할 데이터를 Create ===============
# mbti - Create - many
collection = db['mbti']
collection.drop()  # mbti 콜렉션 삭제 - 초기화

collection.insert_many(docs)  # docs 정보 insert

# mbti_unique - Create - many
collection_unique = db['mbti_unique']  # unique key 설정할 collection
collection_unique.drop()  # mbti 콜렉션 삭제 - 초기화

collection_unique.insert_many(docs)  # docs 정보 insert
