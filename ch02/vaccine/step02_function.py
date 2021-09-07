# import 사용할 package / venv 에 사전 설치하기
import json
import requests

# 함수 설계
# input -함수-> output
# 기능 : get_center_info /  공공데이터 API 사용해 COVID-19 예방접종 센터 정보 조회
# input(parameter, param) : service_key, perPage, page
# ouput(return) : API 결과값 (json 형태의 정보)

serviceKey = "FvQEWvb4UXm31iCKhuIHRwkS+o9EtwAWgPJBTrrYycPSPIyJtUaZGbW7KxMZI1JQjezEy3CTcYzJ6BOlGu8Y0A=="
perPage = 1
page = 1

def get_center_info(service_key, perPage, page):
    result = {}

    # A. API 기능 : COVID-19 예방접종 센터 정보 조회
    # API 문서 : https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15077586

    # =====B. API Request=====
    # B-1. 요청 URL 
    url = "https://api.odcloud.kr/api/15077586/v1/centers"  # API URL

    # B-2. 요청 인자 Request Parameter 설정
    # 인증 설정 service_key - TODO: 직접 발급받기!

    params = {"serviceKey": service_key, "perPage": perPage, "page": page}
    # params = {"serviceKey": "FvQEWvb4UXm31iCKhuIHRwkS+o9EtwAWgPJBTrrYycPSPIyJtUaZGbW7KxMZI1JQjezEy3CTcYzJ6BOlGu8Y0A==", "perPage": 1, "page": 30}
    # 잘못된 파라미터 설정
    # params = {"serviceKey": "sdfsfsdfsdfsdfsf", "perPage": perPage, "page": page}

    # B-3. Request 요청하기 - GET
    r = requests.get(url, params=params)
    # print(r.url) # request url 확인하기

    # ======C. Response 응답 결과값 로딩하기======
    # C-1. 응답결과값(JSON) 가져오기
    # Request(요청)이 성공하면
    if r.status_code == requests.codes.ok:
        result = json.loads(r.content)
    # Request(요청)이 성공하지 않으면
    else:
        result = json.loads(r.content)

    # Test
    # print(result)
    
    return result
    
# 함수 호출 - TEST
result = get_center_info(serviceKey, perPage, page)
print(result)