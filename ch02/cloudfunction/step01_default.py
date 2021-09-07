def main(args):
    # name 이라는 키워드 인자(argument,arg) 를 가져옴. 없으면 World 로 대신함
    name = args.get("name", "World")
    # place 라는 키워드 인자(argument,arg) 를 가져옴. 없으면 Naver 로 대신함
    place  = args.get("place", "Naver")

    # 출력 return 형태
    return {"payload": "Hello, " + name + " in " + place + "!"}
# 예상 출력 : {"payload": "Hello, World in Naver!"}
