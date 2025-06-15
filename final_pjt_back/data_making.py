# make_data.py 파일은 랜덤한 더미 데이터를 만드는 예시 파일입니다.
# 반드시, 사용하는 필드를 확인한 후 본인의 프로젝트에 맞게 수정하여 진행해야 합니다.

# [참고] 현재 코드는 아래 User 모델을 기준으로 작성되어 있습니다.
# class User(AbstractBaseUser):
#     username = models.CharField(max_length=30, unique=True)
#     nickname = models.CharField(max_length=255, blank=True, null=True)
#     email = models.EmailField(max_length=254, blank=True, null=True)
#     age = models.IntegerField(blank=True, null=True)
#     money = models.IntegerField(blank=True, null=True)
#     salary = models.IntegerField(blank=True, null=True)
#     # 가입한 상품 목록 리스트를 ,로 구분된 문자열로 저장함
#     financial_products = models.TextField(blank=True, null=True)
    
#     # superuser fields
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

# import os
# import django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt_back.settings")
# django.setup()

import random
import requests
# from django.conf import settings


# 이름만들기
first_name_samples = "김이박최정강조윤장임삼성커피가맹문의"
middle_name_samples = "민서예지도하주윤채현지텀블백갤럭시"
last_name_samples = "준윤우원호후서연아은진후드티상품추천"

def random_name():
    result = ""
    result += random.choice(first_name_samples)
    result += random.choice(middle_name_samples)
    result += random.choice(last_name_samples)
    return result + str(random.randint(1, 100))

username_list = []
N = 3000
i = 0
while i < N:
    # print(f'user: {i}')
    rn = random_name()
    if rn in username_list:
        continue
    username_list.append(rn)
    i += 1


# 닉네임 만들기
nick_first_samples = "참크래커버터와플야도란피카츄울릉도키보드"
nick_second_samples = "타잔텀블러아이폰갤럭시영일이궁극기사용함"
nick_third_samples = "삼성아카데미포유스퀸동갓충무공제네럴엠퍼"
nick_fourth_samples = "금융상품추천모니터숨이안쉬어져핫빗두근대"

def random_nick():
    result = ""
    result += random.choice(nick_first_samples)
    result += random.choice(nick_second_samples)
    result += random.choice(nick_third_samples)
    result += random.choice(nick_fourth_samples)
    return result

nick_list = []
N = 3000
i = 0
while i < N:
    # print(f'nick: {i}')
    rn = random_nick()
    if rn in nick_list:
        continue
    nick_list.append(rn)
    i += 1

# 성별
GENDER_CHOICES = ['M', 'F']

# 주소만들기
cities = ['서울특별시', '부산광역시', '인천광역시']
# 서울
seoul = ['강남구', '노원구', '종로구']
gangnam = ['역삼1동', '삼성2동', '신사동']
nowon = ['공릉1동', '하계1동', '중계본동']
jongro = ['평창동', '혜화동', '가회동']
# 부산
busan = ['남구', '동래구', '해운대구']
nam = ['용당동', '우암동', '우암동']
dongrae = ['명장2동', '복산동', '안락1동']
haewoondae = ['송정동', '우3동', '반여4동']
# 인천
incheon = ['강화군', '미추홀구', '부평구']
ganghwa = ['강화읍', '서도면', '화도면']
michu = ['문학동', '주안5동', '관교동']
boopyeong = ['부평3동', '일신동', '청천2동']

def random_address():
    city = random.choice(cities)
    if city == '서울특별시':
        district = random.choice(seoul)
        if district == '강남구':
            dong = random.choice(gangnam)
        elif district == '노원구':
            dong = random.choice(nowon)
        else:
            dong = random.choice(jongro)
    elif city == '부산광역시':
        district = random.choice(busan)
        if district == '남구':
            dong = random.choice(nam)
        elif district == '동래구':
            dong = random.choice(dongrae)
        else:
            dong = random.choice(haewoondae)     
    else:
        district = random.choice(incheon)
        if district == '강화군':
            dong = random.choice(ganghwa)
        elif district == '미추홀구':
            dong = random.choice(michu)
        else:
            dong = random.choice(boopyeong)     
    result = city + ' ' + district + ' ' + dong
    return result

address_list = []
N = 3000
i = 0
while i < N:
    # print(f'address: {i}')
    rn = random_address()
    # print(address_list)
    address_list.append(rn)
    i += 1

# mbti 만들기
mbti_first = ['E', 'I']
mbti_second = ['S', 'N']
mbti_third = ['T', 'F']
mbti_fourth = ['J', 'P']

def random_mbti():
    result = ""
    result += random.choice(mbti_first)
    result += random.choice(mbti_second)
    result += random.choice(mbti_third)
    result += random.choice(mbti_fourth)
    return result

mbti_list = []
N = 3000
i = 0
while i < N:
    # print(f'mbti: {i}')
    rn = random_mbti()
    mbti_list.append(rn)
    i += 1    


from datetime import datetime, timedelta

# updated_at 만들기
def random_datetime():
    now = datetime.now()
    return now - timedelta(days=random.randint(0, 365), hours=random.randint(0, 24), minutes=random.randint(0, 60), seconds=random.randint(0, 60))



# 현재 API 에 들어있는 금융 상품 코드 리스트 저장
DP_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
SP_URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
AP_URL = 'http://finlife.fss.or.kr/finlifeapi/annuitySavingProductsSearch.json'

API_KEY = '1cc0fa380494e22182caef54795e8b1f'
# API_KEY = settings.FINANCE_API_KEY

financial_products = []

params = {
  'auth': API_KEY,
  # 금융회사 코드 020000(은행), 030200(여신전문), 030300(저축은행), 050000(보험), 060000(금융투자)
  'topFinGrpNo': '020000',
  'pageNo': 1
}

params2 = {
  'auth': API_KEY,
  # 금융회사 코드 020000(은행), 030200(여신전문), 030300(저축은행), 050000(보험), 060000(금융투자)
  'topFinGrpNo': '050000',
  'pageNo': 1
}

# 정기예금 목록 저장
response = requests.get(DP_URL, params=params).json()
baseList = response.get('result').get('baseList')   # 상품 목록

for product in baseList:
    financial_products.append(product['fin_prdt_cd'])

# 적금 목록 저장
response = requests.get(SP_URL, params=params).json()
baseList = response.get('result').get('baseList')   # 상품 목록

for product in baseList:
    financial_products.append(product['fin_prdt_cd'])

# 연금 목록 저장
response = requests.get(AP_URL, params=params2).json()
baseList = response.get('result').get('baseList')   # 상품 목록

for product in baseList:
    print(product['fin_prdt_cd'])
    financial_products.append(product['fin_prdt_cd'])

dict_keys = ['username', 'nickname', 'gender', 'age', 'address', 'salary', 'money', 'target_asset', 'financial_products']

# json 파일 만들기
import json
from collections import OrderedDict

file = OrderedDict()


N = 3000
i = 0
# 저장 위치는 프로젝트 구조에 맞게 수정합니다.
save_dir = 'accounts/fixtures/accounts/user_data.json'
with open(save_dir, 'w', encoding="utf-8") as f:
    f.write('[')
    
    for i in range(N):
        # print(i)
        # 랜덤한 데이터를 삽입
        file["model"] = "accounts.User"
        file["pk"] = i+1
        file["fields"] = {
            'username': username_list[i],  # 유저 이름 랜덤 생성
            'nickname': nick_list[i],
            'updated_at': random_datetime().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'gender': random.choice(GENDER_CHOICES),
            'age': random.randint(1, 80),  # 나이
            'address': address_list[i],
            'salary': random.randrange(0, 30000, 100), # 연봉
            'money': random.randrange(0, 15000, 10),    # 현재 가진 금액
            # 랜덤한 0~5개의 상품을 가입하도록 삽입됨
            'financial_products': [[str(random.randrange(20, 24))+str(random.randrange(1, 13))+str(random.randrange(1, 31)), random.choice(financial_products), random.randrange(10, 2000)] for _ in range(random.randint(0, 5))],
            'password': "1234",
            'mbti': mbti_list[i],
            'is_active': True,
            'is_staff': False,
            'is_superuser': False
        }

        json.dump(file, f, ensure_ascii=False, indent="\t")
        if i != N-1:
            f.write(',')
    f.write(']')
    f.close()

print(f'데이터 생성 완료 / 저장 위치: {save_dir}')