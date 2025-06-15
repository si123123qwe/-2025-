from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from datetime import datetime


# 환율정보 불러올 함수
@api_view(['GET'])
def exchange_rate(request):

    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&data=AP01'
    response = requests.get(url)
    data = response.json()

    # 오늘날짜
    today = datetime.today().strftime("%Y%m%d")
    minus = 1
    print(f'today: {today}')

    # data가 비어있을 때(주말 등) 최신의 날짜를 찾기
    if data == []:
        while True:
            searchdate = int(today) - minus
            print(f'searchdate: {searchdate}')
            # 끝에 자리가 0이 되면 이전 월 28일로 바꾸기
            if searchdate % 100 == 0:
                minus += 72
                continue
            
            url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&data=AP01&searchdate={searchdate}'
            response = requests.get(url)
            data = response.json()            

            if data:
                break
            else:
                minus += 1

    return Response(data)
