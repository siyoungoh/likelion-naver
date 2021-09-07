def main(args):
    # name 이라는 키워드 인자(argument,arg) 를 가져옴. 없으면 World 로 대신함
    name = args.get('name', 'World')
    # place 라는 키워드 인자(argument,arg) 를 가져옴. 없으면 Naver 로 대신함
    place  = args.get('place', 'Naver')

    result = say_hello(name, place)
    
    return result

def say_hello(name, place):
    result = {'name': name, 'place': place, 'msg': 'hello' + name}
    
    # 출력 return 형태는 dictionary
    return result