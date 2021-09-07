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
collection = db['mbti']
collection_unique = db['mbti_unique']  # unique key 설정할 collection

# =======문제 01=======
# 여러 번 데이터 입력하면 같은 데이터 여러 번 입력됨.
# lion_info = {'name': 'lion', 'type': 'INFP', 'age': 3}
# collection.insert_one(lion_info)

# =======해결 01=======
# db 에 unique key 설정을 해주자!
# unique 하게 유일한 row 데이터만 입력됨. - 예. name:lion 은 오직 하나만 저장
# collection_unique.create_index([('name',1)],unique=True)

# =======문제 02=======
# 같은 이름의 데이터가 있다면 오류가 발생한다.
# 여러번 실행하면 오류(DuplicateKeyError(error.get("errmsg"), 11000, error))가 발생하면서 중복값 저장하지 않음
# lion_info = {'name': 'lion', 'type': 'INFP', 'age': 3}
# collection_unique.insert_one(lion_info)

# # 앞에서 오류가 나니 뒤에 내용도(insert fish) 실행이 안됨.
# fish_info = {'name': 'fish', 'type': 'INFJ', 'age': 1}
# collection_unique.insert_one(fish_info)

# =======해결 02=======
# insert_many option 사용하기
docs = []
lion_info = {'name': 'lion', 'type': 'INFP', 'age': 3}
fish_info = {'name': 'fish', 'type': 'INFJ', 'age': 1}
rabbit_info = {'name': 'rabbit', 'type': 'INFJ', 'age': 10000}
docs.append(lion_info)
docs.append(fish_info)
docs.append(rabbit_info)

# collection_unique.insert_many(docs, ordered=False)

# =======문제 03=======
# BulkWriteError 가 발생함.

# =======해결 03=======
# 맨 위 줄에 아래 import 구문 추가해주기
# from pymongo.errors import BulkWriteError

# =====예외 처리 try - except=========
try:
    collection_unique.insert_many(docs, ordered=False)

except BulkWriteError as bwe:
    print('중복 데이터 발생:', bwe.details)
