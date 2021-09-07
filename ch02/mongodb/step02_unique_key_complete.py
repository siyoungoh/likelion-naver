# 사전작업
# 1. 가상환경에 pymongo 패키지 설치! (되어있으면 상관없음)
# 2. 네이버 클라우드 서버의  공인 ip(public ip) 확인하기!
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

"""
특정 field 에 언제나 유일한 데이터만 저장되도록 합니다
"""

# Connect to MongoDB server
my_ip = ' 서버 public ip'
client = MongoClient('mongodb://likelion:wearethefuture' + '@' + my_ip, 27017)
db = client['likelion']
collection_unique = db['mbti_unique']  # unique key 설정할 collection

# name field 에 unique key 설정 - unique 하게 유일한 row 데이터만 입력됨.
collection_unique.create_index([('name', 1)], unique=True)

# insert_many option 사용하기
docs = []
lion_info = {'name': 'lion', 'type': 'INFP', 'age': 3}
fish_info = {'name': 'fish', 'type': 'INFJ', 'age': 1}
rabbit_info = {'name': 'rabbit', 'type': 'INFJ', 'age': 10000}
docs.append(lion_info)
docs.append(fish_info)
docs.append(rabbit_info)

try:
    collection_unique.insert_many(docs, ordered=False)

except BulkWriteError as bwe:
    print('중복 데이터 발생:', bwe.details)
