import xml
import json
import requests
from bs4 import BeautifulSoup

DataGoKr_APP_KEY = '발급받은 APP KEY'

# 네이버 API: 좌표 -> 주소
def get_current_address(coords_arr):
    coords = str(coords_arr[0]) + "," + str(coords_arr[1])
    url = 'https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc'
    response = requests.get(url, headers={
        'X-NCP-APIGW-API-KEY-ID': NAVER_ID,
        'X-NCP-APIGW-API-KEY': NAVER_SECRET,
    }, params={
        'coords': coords,
    })
    soup = BeautifulSoup(response.text, 'html.parser')

    result_code = soup.select_one('status').select_one('code').get_text()
    if result_code != '0':
        print('Error : Naver API Reverce GC 이용 중에 에러가 발생하였습니다.')
        return 'error'

    for order in soup.select_one('results'):
        name = order.select_one('name').get_text()
        if name == 'legalcode':
            arr = order.select_one('region').select('name')
            return list(map(lambda l: l.get_text(), arr))[1:]
    return 'error'


def get_ill_list():
    """백신 리스트 검색
    Returns:
        dict: key=상위분류코드, value={
            name: 질병이름, 
            vaccines=[
                # 백신정보
                {
                    code: 상세분류코드,
                    name: 백신 이름
                }, ...
            ]}
    """
    url = 'http://apis.data.go.kr/B551182/nonPaymentDamtInfoService/getNonPaymentItemCodeList2'
    response = requests.get(url, params={
        'ServiceKey': DataGoKr_APP_KEY,
        'numOfRows': 1000,
    })

    soup = BeautifulSoup(response.text, 'html.parser')
    result_code = soup.select_one('resultcode').get_text()
    if result_code != '00':
        print('Error : 공공데이터 포털 API 백신 목록 이용 중에 오류가 발생하였습니다.')
        return 'error'
    
    result = {}
    for item in soup.select('items > item')[1:]:
        text = item.select_one('npaymdivcdnm')
        if '예방접종' in str(text):
            # 부모 구분 확인
            parent_code = item.select_one('npaysdivcd').get_text()
            if len(parent_code) <= 2: continue
            if parent_code not in result:
                result[parent_code] = {
                    'name': item.select_one('npaysdivcdnm').get_text(),
                    'vaccines': [],
                }
            
            # 자식 추가
            code = item.select_one('npaydtldivcd').get_text()
            if code == parent_code: continue    
            result[parent_code]['vaccines'].append({
                'id': item.select_one('npaycd').get_text(),             # 비급여코드
                'path': item.select_one('npaykornm').get_text(),        # 비급여한글명(항목소속경로)
                'code': code,                                           # 상세분류코드(백신코드)
                'name': item.select_one('npaydtldivcdnm').get_text(),   # 상세분류명(백신명)
            })
    
    return result


def search_vaccines(search, ill_list):
    """입력한 검색어에 맞는 백신 검색
    병명 혹은 백신 종류를 입력하였을 때 그에 맞는 백신 정보를 반환합니다.
    Args:
        search (str): 검색어(병명, 백신명)
        ill_list (): 전체 백신 목록

    Returns:
        dict: 검색어에 해당하는/연관되는 백신 리스트
    """

    result = []
    for [pcode, item] in ill_list.items():
        for vaccine in item['vaccines']:
            if search in vaccine['path']:
                result.append({
                    'id': vaccine['id'],                # 비급여코드
                    'parent_code': pcode,               # 상위분류코드
                    'parent_name': item['name'],        # 상위분류항목명
                    'vaccine_code': vaccine['code'],    # 분류코드
                    'vaccine_name': vaccine['name'],    # 백신명
                    'hospitals': [],                    # 병원 목록(다른 함수에서 사용)
                })
    return result


def search_hospital_list(search, ill_list):
    """검색어에 해당하는 백신을 처방하는 전국 병원 목록

    Args:
        search (str): 검색어
        ill_list (dict): 전체 백신 목록

    Returns:
        dict: 검색어에 해당하는 백신을 처방하는 전국 병원 목록
    """
    vaccines = search_vaccines(search, ill_list)

    for vaccine in vaccines:
        url = 'http://apis.data.go.kr/B551182/nonPaymentDamtInfoService/getNonPaymentItemHospList2'
        response = requests.get(url, params={
            'ServiceKey': DataGoKr_APP_KEY,
            'numOfRows': 1000,
            'itemCd': vaccine['id']
        })

        soup = BeautifulSoup(response.text, 'html.parser')
        result_code = soup.select_one('resultcode').get_text()
        if result_code != '00':
            print('Error : 공공데이터 포털 API 병원목록 이용 중에 오류가 발생하였습니다.')
            return 'error'

        for item in soup.select('item'):
            city = item.select_one('sidocdnm').get_text()
            vaccine['hospitals'].append({
                'ykiho': item.find('ykiho').get_text(),         # 암호화된 요양기호
                'name': item.select_one('yadmnm').get_text(),   # 병원 이름
                'grade': [item.select_one('clcd').get_text(),   # 병원등급: [등급코드(예: 01), 
                        item.select_one('clcdnm').get_text()],  #          등급명(예: 상급종합)]
                'loc_code': [                                   # 지역 코드
                    item.select_one('sidocd').get_text(),       # 시/도 코드
                    item.select_one('sggucd').get_text()],      # 시/군/구 코드
                'loc':[                                         # 지역명
                    city,                                       # 시/도 명
                    item.select_one('sggucdnm').get_text()],    # 시/군/구 명
                'url': item.select_one('urladdr').get_text(),   # 병원 홈페이지(없을 경우 NO URL)
                'price':[                                       # 백신 처방 가격
                    item.select_one('minprc').get_text(),       # 최소 가격
                    item.select_one('maxprc').get_text()],      # 최고 가격
            })
    
    return vaccines


def main():
    global DataGoKr_APP_KEY

    # 원래는 환경변수로 해야하지만 일단 편의상 .env 파일 만들어서 사용함
    with open('.env', 'r') as file:
        for line in file:
            [key, value] = line.strip().split(':')
            if key == 'DataGoKr_APP_KEY':
                DataGoKr_APP_KEY = value.strip()

    # 아래 두 줄은 한 세트입니다.
    ill_list = get_ill_list()
    hospital_list = search_hospital_list('대상포진', ill_list)

    # 테스트 코드
    # TODO: 삭제
    print(hospital_list)


if __name__ == '__main__':
    main()