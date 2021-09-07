from pymongo import MongoClient

# 사전작업
# 1. 서버 설정 끝내기
# 2. Robo3T 연결 - 데이터베이스 안에 정보 눈으로 보기
# db  > collection > row (has field)

# Connect to MongoDB server

my_ip = ' 서버 public ip'
client = MongoClient('mongodb://likelion:wearethefuture@' + my_ip, 27017)
db = client['likelion']
collection = db['mbti']
# collection.drop()

# =============== Create ===============
# Create - one
# lion_info = {'name': 'lion', 'type': 'INFP', 'age': 3}
# collection.insert_one(lion_info)

# tiger_info = {'name': 'tiger', 'type': 'ENFJ', 'age': 3}
# collection.insert_one(tiger_info)

# bear_info = {'name': 'bear', 'type': 'ENFJ', 'age': 5}
# collection.insert_one(bear_info)

# Create - many
# docs = []
# cat_info = {'name': 'cat', 'type': 'INFP', 'age': 5}
# dog_info = {'name': 'dog', 'type': 'ENFP', 'age': 2}

# docs.append(cat_info)
# docs.append(dog_info)

# # print(docs)
# collection.insert_many(docs)

# =============== Read ===============
# Read - all
# list_mbti = list(collection.find({},{'_id': False}))
# print(list_mbti)

# Read - many
# list_age = list(collection.find({'age':5},{'_id': False}))
# print(list_age)

# list_infp = list(collection.find({'type':'INFP'},{'_id': False}))
# print(list_infp)


# Read - multiple condition
# age_infp = list(collection.find({'type':'INFP', 'age': 3},{'_id': False}))
# print(age_infp)

# Read - one
# age_three = collection.find_one({'age':5},{'_id': False})
# print(age_three)

# infp = collection.find_one({'type':'INFP'},{'_id': False})
# print(infp)

# =============== Update ===============

# Update - one
# collection.update_one({'name':'tiger'},{'$set':{'age':7}})
# tiger = collection.find_one({'name':'tiger'}, {'_id': False})
# print(tiger)

# Update - many
# collection.update_many({'type':'INFP'},{'$set':{'age':100}})
# list_infp = list(collection.find({'type':'INFP'},{'_id': False}))
# print(list_infp)

# Update - field - one
# collection.update_one({'name':'lion'}, {'$set': {'hobby':'climbing'}})
# Update - field - many with filter
# collection.update_many({'type':'INFP'}, {'$set': {'phone':'iPhone'}})
# Update - field - many not exist
# collection.update_many({'phone':{"$exists": False}}, {'$set': {'phone':'Galaxy'}})

# ============== Delete ===============
# drop collection
# collection.drop()

# Delete - one
# collection.delete_one({'name':'tiger'})
# tiger = collection.find_one({'name':'tiger'}, {'_id': False})
# print(tiger) # None

# Delete - many
# collection.delete_many({'type':'INFP'})
# list_infp = list(collection.find({'type':'INFP'},{'_id': False}))
# print(list_infp) # []
