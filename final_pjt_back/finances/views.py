from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from accounts.models import User
# from django.contrib.auth.models import User
from accounts.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer

from .models import Company, CompanyOption, DepositProduct, DepositOption, SavingProduct, SavingOption, AnnuitySavingProduct, AnnuitySavingOption, MortgageLoanProduct, MortgageLoanOption, RentHouseLoanProduct, RentHouseLoanOption, CreditLoanProduct, CreditLoanOption
from .serializers import CompanySerializer, CompanyOptionSerializer, DepositProductSerializer, DepositOptionSerializer, SavingProductSerializer, SavingOptionSerializer, AnnuitySavingProductSerializer, AnnuitySavingOptionSerializer, MortgageLoanProductSerializer, MortgageLoanOptionSerializer, RentHouseLoanProductSerializer, RentHouseLoanOptionSerializer, CreditLoanProductSerializer, CreditLoanOptionSerializer

api_key = settings.FINANCE_API_KEY
domain = 'http://finlife.fss.or.kr/finlifeapi'
topFinGrpNo_list = ['020000', '030200', '030300', '050000', '060000']

# 금융회사 저장
@api_view(['GET'])
def save_companys(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/companySearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            print(max_page_no, pageNo, topFinGrpNo)
            
            # 은행 목록 순회
            for li in response.get("result").get("baseList"):
                fin_co_no = li['fin_co_no']

                # 이미 존재하는 데이터인지 확인
                if Company.objects.filter(fin_co_no=fin_co_no).exists():
                    continue  # 이미 존재하면 건너뛰기
                
                # 은행 데이터 할당
                save_data = {
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'dcls_chrg_man': li['dcls_chrg_man'],
                    'homp_url': li['homp_url'],
                    'cal_tel': li['cal_tel'],
                }
                # 직렬화
                serializer = CompanySerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    
            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month'],
                fin_co_no = li['fin_co_no']
                area_cd  = li['area_cd']
                area_nm =  li['area_nm']
                
                # 이미 존재하는 데이터인지 확인
                if CompanyOption.objects.filter(dcls_month=dcls_month,
                    fin_co_no=fin_co_no,
                    area_cd=area_cd,
                    area_nm=area_nm
                    ).exists():
                    continue  # 이미 존재하면 건너뛰기
                
                # 데이터 변환
                if li['exis_yn'] == 'Y':
                    exis_yn = True
                else:
                    exis_yn = False
                
                company = Company.objects.get(fin_co_no=fin_co_no)

                option = CompanyOption(company=company, dcls_month=dcls_month,fin_co_no=fin_co_no, area_cd=area_cd, area_nm=area_nm, exis_yn=exis_yn)
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 예금 저장
@api_view(['GET'])
def save_deposit_products(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/depositProductsSearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            
            # 예금 목록 순회
            for li in response.get("result").get("baseList"):
                # company = Company.objects.get(fin_co_no=li['fin_co_no'])
                companies = Company.objects.filter(fin_co_no=li['fin_co_no'])

                if companies.exists():
                    company = companies.first() 


                
                # 이미 존재하는 데이터 패스
                if DepositProduct.objects.filter(fin_prdt_cd=li['fin_prdt_cd']).exists():
                    continue
                
                # 예금 상품 데이터 할당
                save_data = {
                    'company': company.pk if company else None,
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'fin_prdt_cd': li['fin_prdt_cd'],
                    'fin_prdt_nm': li['fin_prdt_nm'],
                    'join_way': li['join_way'],
                    'mtrt_int': li['mtrt_int'],
                    'spcl_cnd': li['spcl_cnd'],
                    'join_deny': li['join_deny'],
                    'join_member': li['join_member'],
                    'etc_note': li['etc_note'],
                    'max_limit': li['max_limit'],
                    'dcls_strt_day': li['dcls_strt_day'],
                    'dcls_end_day': li['dcls_end_day'],
                    'fin_co_subm_day': li['fin_co_subm_day'],
                }
                # 직렬화
                serializer = DepositProductSerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month']
                fin_co_no = li['fin_co_no']
                fin_prdt_cd = li['fin_prdt_cd']
                intr_rate_type = li['intr_rate_type']
                intr_rate_type_nm  = li['intr_rate_type_nm']
                intr_rate =  li['intr_rate']
                intr_rate2 =  li['intr_rate2']
                save_trm =  li['save_trm']
                
                # 이미 존재하는 데이터 패스
                if DepositOption.objects.filter(dcls_month=dcls_month, fin_co_no=fin_co_no, 
                    fin_prdt_cd=fin_prdt_cd, intr_rate_type=intr_rate_type, 
                    intr_rate_type_nm=intr_rate_type_nm,
                    intr_rate=intr_rate,
                    intr_rate2=intr_rate2,
                    save_trm=save_trm).exists():
                    continue
                
                # 결측치 처리
                if not intr_rate:
                    intr_rate = -1
                if not intr_rate2:
                    intr_rate2 = -1

                product = DepositProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
                option = DepositOption(product=product, dcls_month=dcls_month, fin_co_no=fin_co_no, fin_prdt_cd=fin_prdt_cd, intr_rate_type=intr_rate_type, intr_rate_type_nm=intr_rate_type_nm, intr_rate=intr_rate, intr_rate2=intr_rate2, save_trm=save_trm)
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 적금 저장
@api_view(['GET'])
def save_saving_products(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/savingProductsSearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            
            # 적금 상품 목록 순회
            for li in response.get("result").get("baseList"):
                # company = Company.objects.get(fin_co_no=li['fin_co_no'])
                companies = Company.objects.filter(fin_co_no=li['fin_co_no'])

                if companies.exists():
                    company = companies.first() 

                
                # 중복 데이터 패스
                if SavingProduct.objects.filter(fin_prdt_cd=li['fin_prdt_cd']).exists():
                    continue
                
                # 적금 상품 데이터 할당
                save_data = {
                    'company': company.pk if company else None,
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'fin_prdt_cd': li['fin_prdt_cd'],
                    'fin_prdt_nm': li['fin_prdt_nm'],
                    'join_way': li['join_way'],
                    'mtrt_int': li['mtrt_int'],
                    'spcl_cnd': li['spcl_cnd'],
                    'join_deny': li['join_deny'],
                    'join_member': li['join_member'],
                    'etc_note': li['etc_note'],
                    'max_limit': li['max_limit'],
                    'dcls_strt_day': li['dcls_strt_day'],
                    'dcls_end_day': li['dcls_end_day'],
                    'fin_co_subm_day': li['fin_co_subm_day'],
                }
                # 직렬화
                serializer = SavingProductSerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month']
                fin_co_no = li['fin_co_no']
                fin_prdt_cd = li['fin_prdt_cd']
                intr_rate_type =li['intr_rate_type']
                intr_rate_type_nm  = li['intr_rate_type_nm']
                rsrv_type = li['rsrv_type']
                rsrv_type_nm = li['rsrv_type_nm']
                intr_rate =  li['intr_rate']
                intr_rate2 =  li['intr_rate2']
                save_trm =  li['save_trm']
                
                # 중복 데이터 패스
                if SavingOption.objects.filter(dcls_month=dcls_month, fin_co_no=fin_co_no, 
                    fin_prdt_cd=fin_prdt_cd, intr_rate_type=intr_rate_type, 
                    intr_rate_type_nm=intr_rate_type_nm,
                    rsrv_type=rsrv_type, 
                    rsrv_type_nm=rsrv_type_nm,
                    intr_rate=intr_rate,
                    intr_rate2=intr_rate2,
                    save_trm=save_trm).exists():
                    continue
                
                # 결측치 처리
                if not intr_rate:
                    intr_rate = -1
                if not intr_rate2:
                    intr_rate2 = -1

                product = SavingProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
                option = SavingOption(product=product, dcls_month=dcls_month, fin_co_no=fin_co_no, fin_prdt_cd=fin_prdt_cd, intr_rate_type=intr_rate_type, intr_rate_type_nm=intr_rate_type_nm, rsrv_type=rsrv_type, rsrv_type_nm = rsrv_type_nm, intr_rate=intr_rate, intr_rate2=intr_rate2, save_trm=save_trm)
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 연금저축 저장
@api_view(['GET'])
def save_annuity_saving_products(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/annuitySavingProductsSearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            
            # 연금저축 상품 목록 순회
            for li in response.get("result").get("baseList"):
                company = Company.objects.filter(fin_co_no=li['fin_co_no'])
                if not company:
                    continue
                # 중복 데이터 패스
                if AnnuitySavingProduct.objects.filter(fin_prdt_cd=li['fin_prdt_cd']).exists():
                    continue
                
                # 연금저축 상품 데이터 할당
                save_data = {
                    'company': company[0].id,
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'fin_prdt_cd': li['fin_prdt_cd'],
                    'fin_prdt_nm': li['fin_prdt_nm'],
                    'join_way': li['join_way'],
                    'pnsn_kind': li['pnsn_kind'],
                    'pnsn_kind_nm': li['pnsn_kind_nm'],
                    'sale_strt_day': li['sale_strt_day'],
                    'mntn_cnt': li['mntn_cnt'],
                    'prdt_type': li['prdt_type'],
                    'prdt_type_nm': li['prdt_type_nm'],
                    'avg_prft_rate': li['avg_prft_rate'],
                    'dcls_rate': li['dcls_rate'],
                    'guar_rate': li['guar_rate'],
                    'btrm_prft_rate_1': li['btrm_prft_rate_1'],
                    'btrm_prft_rate_2': li['btrm_prft_rate_2'],
                    'btrm_prft_rate_3': li['btrm_prft_rate_3'],
                    'etc': li['etc'],
                    'sale_co': li['sale_co'],
                    'dcls_strt_day': li['dcls_strt_day'],
                    'dcls_end_day': li['dcls_end_day'],
                    'fin_co_subm_day': li['fin_co_subm_day'],
                }
                # 직렬화
                serializer = AnnuitySavingProductSerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month']
                fin_co_no = li['fin_co_no']
                fin_prdt_cd = li['fin_prdt_cd']
                
                pnsn_recp_trm = li.get('pnsn_recp_trm', [])
                pnsn_recp_trm_nm = li.get('pnsn_recp_trm_nm', [])
                pnsn_entr_age = li.get('pnsn_entr_age', [])
                pnsn_entr_age_nm = li.get('pnsn_entr_age_nm', [])
                mon_paym_atm = li.get('mon_paym_atm', [])
                mon_paym_atm_nm = li.get('mon_paym_atm_nm', [])
                paym_prd = li.get('paym_prd', [])
                paym_prd_nm = li.get('paym_prd_nm', [])
                pnsn_strt_age = li.get('pnsn_strt_age', [])
                pnsn_strt_age_nm = li.get('pnsn_strt_age_nm', [])
                
                pnsn_recp_amt = li['pnsn_recp_amt']
                
                print(pnsn_recp_trm, pnsn_recp_trm_nm)
                
                # 중복 데이터 패스
                if AnnuitySavingOption.objects.filter(
                    dcls_month=dcls_month,
                    fin_co_no=fin_co_no,
                    fin_prdt_cd=fin_prdt_cd,
                    pnsn_recp_trm=pnsn_recp_trm,
                    pnsn_recp_trm_nm = pnsn_recp_trm_nm,
                    pnsn_entr_age = pnsn_entr_age,
                    pnsn_entr_age_nm = pnsn_entr_age_nm,
                    mon_paym_atm = mon_paym_atm,
                    mon_paym_atm_nm =mon_paym_atm_nm,
                    paym_prd = paym_prd,
                    paym_prd_nm = paym_prd_nm,
                    pnsn_strt_age =pnsn_strt_age,
                    pnsn_strt_age_nm = pnsn_strt_age_nm,
                    pnsn_recp_amt = pnsn_recp_amt).exists():
                    continue
                if not AnnuitySavingProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
                    continue

                product = AnnuitySavingProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
                option = AnnuitySavingOption(product=product, dcls_month=dcls_month, fin_co_no=fin_co_no, fin_prdt_cd=fin_prdt_cd,pnsn_recp_trm=pnsn_recp_trm, pnsn_recp_trm_nm = pnsn_recp_trm_nm, pnsn_entr_age = pnsn_entr_age,pnsn_entr_age_nm = pnsn_entr_age_nm, mon_paym_atm = mon_paym_atm, mon_paym_atm_nm=mon_paym_atm_nm, paym_prd = paym_prd, paym_prd_nm = paym_prd_nm, pnsn_strt_age =pnsn_strt_age, pnsn_strt_age_nm = pnsn_strt_age_nm, pnsn_recp_amt = pnsn_recp_amt)
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 주택담보 대출 저장
@api_view(['GET'])
def save_mortgage_loan_products(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/mortgageLoanProductsSearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            print(max_page_no, pageNo, topFinGrpNo)

            
            # 주택담보 대출 상품 목록 순회
            for li in response.get("result").get("baseList"):
                # company = Company.objects.get(fin_co_no=li['fin_co_no'])

                companies = Company.objects.filter(fin_co_no=li['fin_co_no'])

                if companies.exists():
                    company = companies.first() 

                
                # 중복 데이터 패스
                if MortgageLoanProduct.objects.filter(fin_prdt_cd=li['fin_prdt_cd']).exists():
                    continue
                
                # 연금저축 상품 데이터 할당
                save_data = {
                    'company': company.pk if company else None,
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'fin_prdt_cd': li['fin_prdt_cd'],
                    'fin_prdt_nm': li['fin_prdt_nm'],
                    'join_way': li['join_way'],
                    'loan_inci_expn': li['loan_inci_expn'],
                    'erly_rpay_fee': li['erly_rpay_fee'],
                    'dly_rate': li['dly_rate'],
                    'loan_lmt': li['loan_lmt'],
                    'dcls_strt_day': li['dcls_strt_day'],
                    'dcls_end_day': li['dcls_end_day']
                }
                # 직렬화
                serializer = MortgageLoanProductSerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month']
                fin_co_no = li['fin_co_no']
                fin_prdt_cd = li['fin_prdt_cd']
                mrtg_type = li['mrtg_type']
                mrtg_type_nm = li['mrtg_type_nm']
                rpay_type = li['rpay_type']
                rpay_type_nm = li['rpay_type_nm']
                lend_rate_type = li['lend_rate_type']
                lend_rate_type_nm = li['lend_rate_type_nm']
                lend_rate_min = li['lend_rate_min']
                lend_rate_max = li['lend_rate_max']
                lend_rate_avg = li['lend_rate_avg']
                
                # 중복 데이터 패스
                if MortgageLoanOption.objects.filter(
                    dcls_month = dcls_month,
                    fin_co_no = fin_co_no,
                    fin_prdt_cd = fin_prdt_cd,
                    mrtg_type = mrtg_type,
                    mrtg_type_nm = mrtg_type_nm,
                    rpay_type = rpay_type,
                    rpay_type_nm = rpay_type_nm,
                    lend_rate_type = lend_rate_type,
                    lend_rate_type_nm = lend_rate_type_nm,
                    lend_rate_min = lend_rate_min,
                    lend_rate_max = lend_rate_max,
                    lend_rate_avg = lend_rate_avg).exists():
                    continue

                product = MortgageLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
                option = MortgageLoanOption(product=product, dcls_month = dcls_month,
                    fin_co_no = fin_co_no,
                    fin_prdt_cd = fin_prdt_cd,
                    mrtg_type = mrtg_type,
                    mrtg_type_nm = mrtg_type_nm,
                    rpay_type = rpay_type,
                    rpay_type_nm = rpay_type_nm,
                    lend_rate_type = lend_rate_type,
                    lend_rate_type_nm = lend_rate_type_nm,
                    lend_rate_min = lend_rate_min,
                    lend_rate_max = lend_rate_max,
                    lend_rate_avg = lend_rate_avg)
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 전세자금 대출 저장
@api_view(['GET'])
def save_rent_house_loan_products(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/rentHouseLoanProductsSearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            
            # 전세자금 대출 상품 목록 순회
            for li in response.get("result").get("baseList"):
                # company = Company.objects.get(fin_co_no=li['fin_co_no'])
                companies = Company.objects.filter(fin_co_no=li['fin_co_no'])

                if companies.exists():
                    company = companies.first() 


                
                # 중복 데이터 패스
                if RentHouseLoanProduct.objects.filter(fin_prdt_cd=li['fin_prdt_cd']).exists():
                    continue
                
                # 전세자금 상품 데이터 할당
                save_data = {
                    'company': company.pk if company else None,
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'fin_prdt_cd': li['fin_prdt_cd'],
                    'fin_prdt_nm': li['fin_prdt_nm'],
                    'join_way': li['join_way'],
                    'loan_inci_expn': li['loan_inci_expn'],
                    'erly_rpay_fee': li['erly_rpay_fee'],
                    'dly_rate': li['dly_rate'],
                    'loan_lmt': li['loan_lmt'],
                    'dcls_strt_day': li['dcls_strt_day'],
                    'dcls_end_day': li['dcls_end_day'],
                    'fin_co_subm_day': li['fin_co_subm_day']
                }
                # 직렬화
                serializer = RentHouseLoanProductSerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month']
                fin_co_no = li['fin_co_no']
                fin_prdt_cd = li['fin_prdt_cd']
                rpay_type = li['rpay_type']
                rpay_type_nm = li['rpay_type_nm']
                lend_rate_type = li['lend_rate_type']
                lend_rate_type_nm = li['lend_rate_type_nm']
                lend_rate_min = li['lend_rate_min']
                lend_rate_max = li['lend_rate_max']
                lend_rate_avg = li['lend_rate_avg']
                
                # 중복 데이터 패스
                if RentHouseLoanOption.objects.filter(
                    dcls_month = dcls_month,
                    fin_co_no = fin_co_no,
                    fin_prdt_cd = fin_prdt_cd,
                    rpay_type = rpay_type,
                    rpay_type_nm = rpay_type_nm,
                    lend_rate_type = lend_rate_type,
                    lend_rate_type_nm = lend_rate_type_nm,
                    lend_rate_min = lend_rate_min,
                    lend_rate_max = lend_rate_max,
                    lend_rate_avg = lend_rate_avg):
                    continue

                product = RentHouseLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
                option = RentHouseLoanOption(product=product, dcls_month = dcls_month,
                    fin_co_no = fin_co_no,
                    fin_prdt_cd = fin_prdt_cd,
                    rpay_type = rpay_type,
                    rpay_type_nm = rpay_type_nm,
                    lend_rate_type = lend_rate_type,
                    lend_rate_type_nm = lend_rate_type_nm,
                    lend_rate_min = lend_rate_min,
                    lend_rate_max = lend_rate_max,
                    lend_rate_avg = lend_rate_avg)
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 개인신용 대출 저장
@api_view(['GET'])
def save_credit_loan_products(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/creditLoanProductsSearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            
            # 개인신용 대출 상품 목록 순회
            for li in response.get("result").get("baseList"):
                company = Company.objects.filter(fin_co_no=li['fin_co_no'])
                if not company.exists():
                    continue
                
                # 중복 데이터 패스
                if CreditLoanProduct.objects.filter(fin_prdt_cd=li['fin_prdt_cd']).exists():
                    continue
                
                # 개인신용대출 상품 데이터 할당
                save_data = {
                    'company': company[0].id,
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'fin_prdt_cd': li['fin_prdt_cd'],
                    'fin_prdt_nm': li['fin_prdt_nm'],
                    'join_way': li['join_way'],
                    'cb_name': li['cb_name'],
                    'crdt_prdt_type': li['crdt_prdt_type'],
                    'crdt_prdt_type_nm': li['crdt_prdt_type_nm'],
                    'dcls_strt_day': li['dcls_strt_day'],
                    'dcls_end_day': li['dcls_end_day'],
                    'fin_co_subm_day': li['fin_co_subm_day']
                }
                # 직렬화
                serializer = CreditLoanProductSerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month']
                fin_co_no = li['fin_co_no']
                fin_prdt_cd = li['fin_prdt_cd']
                crdt_prdt_type = li['crdt_prdt_type']
                crdt_lend_rate_type = li['crdt_lend_rate_type']
                crdt_lend_rate_type_nm = li['crdt_lend_rate_type_nm']
                crdt_grad_1 = li['crdt_grad_1']
                crdt_grad_4 = li['crdt_grad_4']
                crdt_grad_5 = li['crdt_grad_5']
                crdt_grad_6 = li['crdt_grad_6']
                crdt_grad_10 = li['crdt_grad_10']
                crdt_grad_11 = li['crdt_grad_11']
                crdt_grad_12 = li['crdt_grad_12']
                crdt_grad_13 = li['crdt_grad_13']
                crdt_grad_avg = li['crdt_grad_avg']
                
                # 중복 데이터 패스
                if CreditLoanOption.objects.filter(
                    dcls_month = dcls_month,
                    fin_co_no = fin_co_no,
                    fin_prdt_cd = fin_prdt_cd,
                    crdt_prdt_type = crdt_prdt_type,
                    crdt_lend_rate_type = crdt_lend_rate_type,
                    crdt_lend_rate_type_nm = crdt_lend_rate_type_nm,
                    crdt_grad_1 = crdt_grad_1,
                    crdt_grad_4 = crdt_grad_4,
                    crdt_grad_5 = crdt_grad_5,
                    crdt_grad_6 = crdt_grad_6,
                    crdt_grad_10 = crdt_grad_10,
                    crdt_grad_11 = crdt_grad_11, crdt_grad_12=crdt_grad_12, crdt_grad_13=crdt_grad_13, crdt_grad_avg=crdt_grad_avg
                    ).exists():
                    continue

                product = CreditLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
                option = CreditLoanOption(product=product, dcls_month = dcls_month,
                    fin_co_no = fin_co_no,
                    fin_prdt_cd = fin_prdt_cd,
                    crdt_prdt_type = crdt_prdt_type,
                    crdt_lend_rate_type = crdt_lend_rate_type,
                    crdt_lend_rate_type_nm = crdt_lend_rate_type_nm,
                    crdt_grad_1 = crdt_grad_1,
                    crdt_grad_4 = crdt_grad_4,
                    crdt_grad_5 = crdt_grad_5,
                    crdt_grad_6 = crdt_grad_6,
                    crdt_grad_10 = crdt_grad_10,
                    crdt_grad_11 = crdt_grad_11, crdt_grad_12=crdt_grad_12, crdt_grad_13=crdt_grad_13, crdt_grad_avg=crdt_grad_avg
                    )
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 금융 회사 조회
@api_view(['GET'])
def get_companys(request):
    # 예금 목록 불러오기
    companys = Company.objects.all()
    seralizer = CompanySerializer(companys, many=True)
    return Response(seralizer.data)

# 단일 회사 조회
@api_view(['GET'])
def get_company_detail(request, fin_co_no):
    # 예금 목록 불러오기
    company = Company.objects.get(fin_co_no=fin_co_no)
    seralizer = CompanySerializer(company)
    return Response(seralizer.data)

# 특정 금융 회사 옵션 조회
@api_view(['GET'])
def get_company_options(request, fin_co_no):
    # 예금 목록 불러오기
    optionlist = CompanyOption.objects.filter(fin_co_no=fin_co_no)
    seralizer = CompanyOptionSerializer(optionlist, many=True)
    return Response(seralizer.data)


# 전체 예금 상품 조회
@api_view(['GET'])
def get_deposit_products(request):
    # 예금 목록 불러오기
    products = DepositProduct.objects.all()
    products_contain_options = []    
    for product in products:
        option_list = DepositOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = DepositOptionSerializer(option_list, many=True)
        serializer2 = DepositProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)

    return Response(products_contain_options)
    
    
# 전체 예금 옵션 조회
@api_view(['GET'])
def get_deposit_options(request):
    # 예금 목록 불러오기
    options = DepositOption.objects.all()
    seralizer = DepositOptionSerializer(options, many=True)
    return Response(seralizer.data)


# 단일 예금 상품 조회
@api_view(['GET'])
def get_deposit_product_detail(request, fin_prdt_cd):
    product = DepositProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
    products_contain_options = []
    option_list = DepositOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
    seralizer1 = DepositOptionSerializer(option_list, many=True)
    seralizer2 = DepositProductSerializer(product)
    seralizer = {
        'product': seralizer2.data,
        'options': seralizer1.data
    }
    products_contain_options.append(seralizer)

    return Response(products_contain_options)


# 단일 예금 상품의 옵션 조회
@api_view(['GET'])
def get_deposit_product_options(request, fin_prdt_cd):
    optionlist = DepositOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionSerializer(optionlist, many=True)
    return Response(serializer.data)


# 전체 상품 검색 [예금]
@api_view(['GET'])
def search_deposit_products(request, fin_co_no, save_trm):
    
    # 예금 목록 불러오기
    if fin_co_no != '전체':
        products = DepositProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        products = DepositProduct.objects.all()
        
    filtered_products = []
    
    for product in products:
        # 옵션 목록 불러오기
        if save_trm:
            option_list = DepositOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd, save_trm=save_trm)
        else:
            option_list = DepositOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
            
        serializer1 = DepositOptionSerializer(option_list, many=True)
        serializer2 = DepositProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)

    return Response(filtered_products)


# 모든 적금 상품 조회
@api_view(['GET'])
def get_saving_products(request):
    # 예금 목록 불러오기
    products = SavingProduct.objects.all()
    products_contain_options = []    
    for product in products:
        option_list = SavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = SavingOptionSerializer(option_list, many=True)
        serializer2 = SavingProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)

    return Response(products_contain_options)

# 모든 적금 옵션 조회
@api_view(['GET'])
def get_saving_options(request):
    # 예금 목록 불러오기
    options = SavingOption.objects.all()
    seralizer = SavingOptionSerializer(options, many=True)
    return Response(seralizer.data)

# 단일 적금 상품 조회
@api_view(['GET'])
def get_saving_product_detail(request, fin_prdt_cd):
    product = SavingProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
    products_contain_options = []
    option_list = SavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
    seralizer1 = SavingOptionSerializer(option_list, many=True)
    seralizer2 = SavingProductSerializer(product)
    seralizer = {
        'product': seralizer2.data,
        'options': seralizer1.data
    }
    products_contain_options.append(seralizer)

    return Response(products_contain_options)

# 단일 적금 상품 옵션 조회
@api_view(['GET'])
def get_saving_product_options(request, fin_prdt_cd):
    optionlist = SavingOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = SavingOptionSerializer(optionlist, many=True)
    return Response(serializer.data)

# 적금 상품 검색
@api_view(['GET'])
def search_saving_products(request, fin_co_no, save_trm):
    
    # 예금 목록 불러오기
    if fin_co_no != '전체':
        products = SavingProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        products = SavingProduct.objects.all()
        
    filtered_products = []
    
    for product in products:
        # 옵션 목록 불러오기
        if save_trm:
            option_list = SavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd, save_trm=save_trm)
        else:
            option_list = SavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
            
        serializer1 = SavingOptionSerializer(option_list, many=True)
        serializer2 = SavingProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)

    return Response(filtered_products)


# 연금저축
# 전체 상품 조회 [연금저축]
@api_view(['GET'])
def get_annuity_saving_products(request):
    products = AnnuitySavingProduct.objects.all()
    products_contain_options = []    
    for product in products:
        option_list = AnnuitySavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = AnnuitySavingOptionSerializer(option_list, many=True)
        serializer2 = AnnuitySavingProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)

    return Response(products_contain_options)

# 모든 옵션 조회
@api_view(['GET'])
def get_annuity_saving_options(request):
    # 예금 목록 불러오기
    options = AnnuitySavingOption.objects.all()
    seralizer = AnnuitySavingOptionSerializer(options, many=True)
    return Response(seralizer.data)

# 단일 상품 조회
@api_view(['GET'])
def get_annuity_saving_product_detail(request, fin_prdt_cd):
    product = AnnuitySavingProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
    products_contain_options = []
    option_list = AnnuitySavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
    seralizer1 = AnnuitySavingOptionSerializer(option_list, many=True)
    seralizer2 = AnnuitySavingProductSerializer(product)
    seralizer = {
        'product': seralizer2.data,
        'options': seralizer1.data
    }
    products_contain_options.append(seralizer)

    return Response(products_contain_options)

# 단일 상품의 옵션 조회
@api_view(['GET'])
def get_annuity_saving_product_options(request, fin_prdt_cd):
    optionlist = AnnuitySavingOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = AnnuitySavingOptionSerializer(optionlist, many=True)
    return Response(serializer.data)

# 전체 상품 검색
@api_view(['GET'])
def search_annuity_saving_products(request, fin_co_no, pnsn_recp_trm):
    
    if fin_co_no != '전체':
        products = AnnuitySavingProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        products = AnnuitySavingProduct.objects.all()
        
    filtered_products = []
    for product in products:
        # 옵션 목록 불러오기
        if pnsn_recp_trm != '전체':
            option_list = AnnuitySavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd, pnsn_recp_trm=pnsn_recp_trm)
        else:
            option_list = AnnuitySavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
            
        serializer1 = AnnuitySavingOptionSerializer(option_list, many=True)
        serializer2 = AnnuitySavingProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)

    return Response(filtered_products)


# 주택담보 대출
# 전체 상품 조회 [주택담보대출]
@api_view(['GET'])
def get_mortgage_loan_products(request):
    products = MortgageLoanProduct.objects.all()
    products_contain_options = []    
    for product in products:
        option_list = MortgageLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = MortgageLoanOptionSerializer(option_list, many=True)
        serializer2 = MortgageLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)

    return Response(products_contain_options)

# 전체 옵션 조회
@api_view(['GET'])
def get_mortgage_loan_options(request):
    options = MortgageLoanOption.objects.all()
    seralizer = MortgageLoanOptionSerializer(options, many=True)
    return Response(seralizer.data)

# 단일 상품 조회
@api_view(['GET'])
def get_mortgage_loan_product_detail(request, fin_prdt_cd):
    product = MortgageLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
    seralizer = MortgageLoanProductSerializer(product)
    return Response(seralizer.data)

# 단일 상품의 옵션 조회
@api_view(['GET'])
def get_mortgage_loan_product_options(request, fin_prdt_cd):
    optionlist = MortgageLoanOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = MortgageLoanOptionSerializer(optionlist, many=True)
    return Response(serializer.data)

# 전체 상품 검색
@api_view(['GET'])
def search_mortgage_loan_products(request, fin_co_no, mrtg_type, rpay_type, lend_rate_type):
    if fin_co_no != '전체':
        products = MortgageLoanProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        products = MortgageLoanProduct.objects.all()
        
    filtered_products = []
    
    for product in products:
        # 옵션 목록 불러오기
        option_list = MortgageLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd, mrtg_type=mrtg_type, rpay_type=rpay_type, lend_rate_type=lend_rate_type)

        serializer1 = MortgageLoanOptionSerializer(option_list, many=True)
        serializer2 = MortgageLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)

    return Response(filtered_products)


# 전세자금 대출
# 전체 상품 조회 [전세자금대출]
@api_view(['GET'])
def get_rent_house_loan_products(request):
    products = RentHouseLoanProduct.objects.all()
    products_contain_options = []    
    for product in products:
        option_list = RentHouseLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = RentHouseLoanOptionSerializer(option_list, many=True)
        serializer2 = RentHouseLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)

    return Response(products_contain_options)

# 전체 옵션 조회
@api_view(['GET'])
def get_rent_house_loan_options(request):
    options = RentHouseLoanOption.objects.all()
    seralizer = RentHouseLoanOptionSerializer(options, many=True)
    return Response(seralizer.data)

# 단일 상품 조회
@api_view(['GET'])
def get_rent_house_loan_product_detail(request, fin_prdt_cd):
    product = RentHouseLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
    seralizer = RentHouseLoanProductSerializer(product)
    return Response(seralizer.data)

# 단일 상품의 옵션 조회
@api_view(['GET'])
def get_rent_house_loan_product_options(request, fin_prdt_cd):
    optionlist = RentHouseLoanOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = RentHouseLoanOptionSerializer(optionlist, many=True)
    return Response(serializer.data)

# 전체 상품 검색
@api_view(['GET'])
def search_rent_house_loan_products(request, fin_co_no, rpay_type, lend_rate_type):
    if fin_co_no != '전체':
        products = RentHouseLoanProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        products = RentHouseLoanProduct.objects.all()
        
    filtered_products = []
    
    for product in products:
        # 옵션 목록 불러오기
        option_list = RentHouseLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd, rpay_type=rpay_type, lend_rate_type=lend_rate_type)
        
        serializer1 = RentHouseLoanOptionSerializer(option_list, many=True)
        serializer2 = RentHouseLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)

    return Response(filtered_products)


# 신용대출
# 전체 상품 조회 [신용대출]
@api_view(['GET'])
def get_credit_loan_products(request):
    products = CreditLoanProduct.objects.all()
    products_contain_options = []    
    for product in products:
        option_list = CreditLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = CreditLoanOptionSerializer(option_list, many=True)
        serializer2 = CreditLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)

    return Response(products_contain_options)

# 전체 옵션 조회
@api_view(['GET'])
def get_credit_loan_options(request):
    options = CreditLoanOption.objects.all()
    seralizer = CreditLoanOptionSerializer(options, many=True)
    return Response(seralizer.data)

# 단일 상품 조회
@api_view(['GET'])
def get_credit_loan_product_detail(request, fin_prdt_cd):
    product = CreditLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
    seralizer = CreditLoanProductSerializer(product)
    return Response(seralizer.data)

# 단일 상품의 옵션 조회
@api_view(['GET'])
def get_credit_loan_product_options(request, fin_prdt_cd):
    optionlist = CreditLoanOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = CreditLoanOptionSerializer(optionlist, many=True)
    return Response(serializer.data)

# 전체 상품 검색
@api_view(['GET'])
def search_credit_loan_products(request, fin_co_no, crdt_lend_rate_type):
    if fin_co_no != '전체':
        products = CreditLoanProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        products = CreditLoanProduct.objects.all()
        
    filtered_products = []
    
    for product in products:
        # 옵션 목록 불러오기
        if crdt_lend_rate_type:
            option_list = CreditLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd, crdt_lend_rate_type=crdt_lend_rate_type)
        else:
            option_list = CreditLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = CreditLoanOptionSerializer(option_list, many=True)
        serializer2 = CreditLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)

    return Response(filtered_products)

# 전체 상품 검색 [예금]
@api_view(['GET', 'POST'])
def filter_user(request):  
    print(request.POST)  
    GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
    )
    SAVING_TYPE_CHOICES = [
        ('thrifty', '알뜰형'),
        ('challenging', '도전형'),
        ('diligent', '성실형'),
    ]

    # 필터 인자
    gender = request.POST.get('gender')
    age = request.POST.get('age')
    address = request.POST.get('address')
    salary = request.POST.get('salary')
    money = request.POST.get('money')
    target_asset = request.POST.get('target_asset')
    saving_type = request.POST.get('saving_type')
    favorite_company = request.POST.get('favorite_company')
    mbti = request.POST.get('mbti')
    print(gender, age, address, salary, money, target_asset, saving_type, favorite_company, mbti)

    # 필터링
    filtered_users = User.objects.all()
    if gender:
        filtered_users = filtered_users.filter(gender=gender)
    if age:
        if int(age) < 20:
            filtered_users = filtered_users.filter(age__lte=20)
        elif 20 <= int(age) < 30:
            filtered_users = filtered_users.filter(age__gte=20, age__lt=30)
        elif 30 <= int(age) < 40:
            filtered_users = filtered_users.filter(age__gte=30, age__lt=40)
        elif 40 <= int(age) < 50:
            filtered_users = filtered_users.filter(age__gte=40, age__lt=50)
        elif 50 <= int(age) < 60:
            filtered_users = filtered_users.filter(age__gte=50, age__lt=60)
        else:
            filtered_users = filtered_users.filter(age__gte=60)
    if address:
        filtered_users = filtered_users.filter(address=address)
    if salary:
        filtered_users = filtered_users.filter(salary__lte=(int(salary) * 0.95), salary__lt=(int(salary) * 1.05))
    if money:
        filtered_users = filtered_users.filter(money=int(money))
    if target_asset:
        filtered_users = filtered_users.filter(target_asset=int(target_asset))
    if saving_type:
        filtered_users = filtered_users.filter(saving_type=saving_type)
    if favorite_company:
        filtered_users = filtered_users.filter(favorite_company=favorite_company)
    if mbti:
        filtered_users = filtered_users.filter(mbti=mbti)

    # 필터링된 유저들이 가입한 상품
    products = {}
    
    for user in filtered_users:
        financial_products = user.financial_products
        for product in financial_products:
            if product:
                products.setdefault(product[1], 0)
                products[product[1]] += 1

    sorted_products = list(sorted(products.items(), key=lambda item: item[1], reverse=True))
    print(sorted_products)
    return Response(sorted_products)
  
# 전체 상품 조회
@api_view(['GET'])
def get_all_products(request):
    all_products = {'deposit':{}, 'saving':{}, 'annuity':{}, 'mortgage':{}, 'rent_house':{}, 'credit':{}}
    
    # 예금 목록 불러오기
    deposit_products = DepositProduct.objects.all()
    products_contain_options = []
    for product in deposit_products:
        option_list = DepositOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = DepositOptionSerializer(option_list, many=True)
        serializer2 = DepositProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)
    
    # 적금 목록 불러오기
    saving_products = SavingProduct.objects.all()
    for product in saving_products:
        option_list = SavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = SavingOptionSerializer(option_list, many=True)
        serializer2 = SavingProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)
    
    # 연금 목록 불러오기
    annuity_products = AnnuitySavingProduct.objects.all()
    for product in annuity_products:
        option_list = AnnuitySavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = AnnuitySavingOptionSerializer(option_list, many=True)
        serializer2 = AnnuitySavingProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)
    
    # 주택 담보 대출 목록 불러오기
    mortgage_products = MortgageLoanProduct.objects.all()
    for product in mortgage_products:
        option_list = MortgageLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = MortgageLoanOptionSerializer(option_list, many=True)
        serializer2 = MortgageLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)
 
    # 전세 자금 대출 목록 불러오기
    rent_house_products = RentHouseLoanProduct.objects.all()
    for product in rent_house_products:
        option_list = RentHouseLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = RentHouseLoanOptionSerializer(option_list, many=True)
        serializer2 = RentHouseLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)
 
    # 신용 대출 목록 불러오기
    credit_products = CreditLoanProduct.objects.all()
    for product in credit_products:
        option_list = CreditLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = CreditLoanOptionSerializer(option_list, many=True)
        serializer2 = CreditLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)

    return Response(products_contain_options)

# 대출 상품 검색
@api_view(['GET'])
def search_loan_products(request, fin_co_no):
    filtered_products = []
    
    # 주택 담보 대출
    if fin_co_no != '전체':
        mortgage_products = MortgageLoanProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        mortgage_products = MortgageLoanProduct.objects.all()
        
    for product in mortgage_products:
        option_list = MortgageLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = MortgageLoanOptionSerializer(option_list, many=True)
        serializer2 = MortgageLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)
        
    # 전세자금 대출
    if fin_co_no != '전체':
        rent_house_products = RentHouseLoanProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        rent_house_products = RentHouseLoanProduct.objects.all()
        
    for product in rent_house_products:
        option_list = RentHouseLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = RentHouseLoanOptionSerializer(option_list, many=True)
        serializer2 = RentHouseLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)
        
    # 신용 대출
    if fin_co_no != '전체':
        credit_products = CreditLoanProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        credit_products = CreditLoanProduct.objects.all()
        
    for product in credit_products:
        option_list = CreditLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = CreditLoanOptionSerializer(option_list, many=True)
        serializer2 = CreditLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)
    return Response(filtered_products)


# 모든 대출 상품 조회
@api_view(['GET'])
def get_loan_products(request):
    products_contain_options = []
    
    # 주택 담보 대출
    mortgage_products = MortgageLoanProduct.objects.all()
    for product in mortgage_products:
        option_list = MortgageLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = MortgageLoanOptionSerializer(option_list, many=True)
        serializer2 = MortgageLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)
        
    # 전세자금 대출
    rent_house_products = RentHouseLoanProduct.objects.all()
    for product in rent_house_products:
        option_list = RentHouseLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = RentHouseLoanOptionSerializer(option_list, many=True)
        serializer2 = RentHouseLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)
        
    # 신용 대출
    credit_products = CreditLoanProduct.objects.all()
    for product in credit_products:
        option_list = CreditLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = CreditLoanOptionSerializer(option_list, many=True)
        serializer2 = CreditLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)
    return Response(products_contain_options)

# 단일 대출 상품 조회
@api_view(['GET'])
def get_loan_product_detail(request, fin_prdt_cd):
    # 주택 담보 탐색
    product = {}
    if MortgageLoanProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
        product = MortgageLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
        option_list = MortgageLoanOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
        
        serializer1 = MortgageLoanOptionSerializer(option_list, many=True)
        serializer2 = MortgageLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        
    elif RentHouseLoanProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
        product = RentHouseLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
        option_list = RentHouseLoanOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
        
        serializer1 = RentHouseLoanOptionSerializer(option_list, many=True)
        serializer2 = RentHouseLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
    else:
        product = CreditLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
        option_list = CreditLoanOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
        
        serializer1 = CreditLoanOptionSerializer(option_list, many=True)
        serializer2 = CreditLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
    return Response(serializer)


# 예금 top3
@api_view(['GET'])
def top_dps(request):  
    print(request.POST)  
    
    # 모든 유저 정보
    user_all = User.objects.all()

    # 필터링된 유저들이 가입한 상품
    products = {}
    
    for user in user_all:
        financial_products = user.financial_products
        for product in financial_products:
            if product:
                products.setdefault(product[1], 0)
                products[product[1]] += 1

    print('상품', products)
    sorted_products = dict(sorted(products.items(), key=lambda item: item[1], reverse=True))

    # 예금 베스트
    dps_best = []
    dps = DepositProduct.objects.all()
    print(f'모든예금 : {dps}')
    for dp in dps:
        product_no = dp.fin_prdt_cd
        print(dp.fin_prdt_cd)
        for key, value in sorted_products.items():
            if product_no == key:
                dps_best.append((value, key))
    
    # 예금 베스트 정렬
    dps_best.sort(reverse=True)
    # sorted_dps_best = dict(sorted(dps_best.items(), key=lambda item: item[1], reverse=True))
    print(f'예금 베스트: {dps_best}')
    # 예금 top
    dps_top = dps_best[:5]


    return Response(dps_top)


# 적금 top3
@api_view(['GET'])
def top_sps(request):  
    print(request.POST)  
    
    # 모든 유저 정보
    user_all = User.objects.all()

    # 필터링된 유저들이 가입한 상품
    products = {}
    
    for user in user_all:
        financial_products = user.financial_products
        for product in financial_products:
            if product:
                products.setdefault(product[1], 0)
                products[product[1]] += 1

    print('상품', products)
    sorted_products = dict(sorted(products.items(), key=lambda item: item[1], reverse=True))

    # 적금 베스트
    sps_best = []
    sps = SavingProduct.objects.all()
    print(f'모든적금 : {sps}')
    for sp in sps:
        product_no = sp.fin_prdt_cd
        for key, value in sorted_products.items():
            if product_no == key:
                sps_best.append((value, key))
    
    # 적금 베스트 정렬
    sps_best.sort(reverse=True)
    # sorted_dps_best = dict(sorted(dps_best.items(), key=lambda item: item[1], reverse=True))
    print(f'적금 베스트: {sps_best}')
    # 적금 top
    sps_top = sps_best[:5]


    return Response(sps_top)


# 전체 top3
@api_view(['GET'])
def best_three(request):  
    print(request.POST)  
    
    # 모든 유저 정보
    user_all = User.objects.all()

    # 필터링된 유저들이 가입한 상품
    products = {}
    
    for user in user_all:
        financial_products = user.financial_products
        for product in financial_products:
            if product:
                products.setdefault(product[1], 0)
                products[product[1]] += 1

    print('상품', products)
    sorted_products = dict(sorted(products.items(), key=lambda item: item[1], reverse=True))

    all_best = []

    # 예금 베스트
    dps = DepositProduct.objects.all()
    print(f'모든예금 : {dps}')
    for dp in dps:
        product_no = dp.fin_prdt_cd
        print(dp.fin_prdt_cd)
        for key, value in sorted_products.items():
            if product_no == key:
                all_best.append((value, key))

    # 적금 베스트
    sps = SavingProduct.objects.all()
    print(f'모든적금 : {sps}')
    for sp in sps:
        product_no = sp.fin_prdt_cd
        for key, value in sorted_products.items():
            if product_no == key:
                all_best.append((value, key))

    # 전체 베스트 정렬
    all_best.sort(reverse=True)

    best_three = all_best[:5]


    return Response(best_three)


# 상품 단일조회
@api_view(['GET'])
def get_all_product_detail(request, fin_prdt_cd):
    if DepositProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
        product = DepositProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
        option_list = DepositOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        
        seralizer1 = DepositOptionSerializer(option_list, many=True)
        seralizer2 = DepositProductSerializer(product)
        seralizer = {
            'product': seralizer2.data,
            'options': seralizer1.data
        }
        return Response(seralizer)
    
    if SavingProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
        product = SavingProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
        option_list = SavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        
        seralizer1 = SavingOptionSerializer(option_list, many=True)
        seralizer2 = SavingProductSerializer(product)
        seralizer = {
            'product': seralizer2.data,
            'options': seralizer1.data
        }
        return Response(seralizer)
    
    if AnnuitySavingProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
        product = AnnuitySavingProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
        option_list = AnnuitySavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        
        seralizer1 = AnnuitySavingOptionSerializer(option_list, many=True)
        seralizer2 = AnnuitySavingProductSerializer(product)
        seralizer = {
            'product': seralizer2.data,
            'options': seralizer1.data
        }
        return Response(seralizer)
    
    if MortgageLoanProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
        product = MortgageLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
        option_list = MortgageLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        
        seralizer1 = MortgageLoanOptionSerializer(option_list, many=True)
        seralizer2 = MortgageLoanProductSerializer(product)
        seralizer = {
            'product': seralizer2.data,
            'options': seralizer1.data
        }
        return Response(seralizer)
    
    if RentHouseLoanProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
        product = RentHouseLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
        option_list = RentHouseLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        
        seralizer1 = RentHouseLoanOptionSerializer(option_list, many=True)
        seralizer2 = RentHouseLoanProductSerializer(product)
        seralizer = {
            'product': seralizer2.data,
            'options': seralizer1.data
        }
        return Response(seralizer)
    
    if CreditLoanProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
        product = CreditLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
        option_list = CreditLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        
        seralizer1 = CreditLoanOptionSerializer(option_list, many=True)
        seralizer2 = CreditLoanProductSerializer(product)
        seralizer = {
            'product': seralizer2.data,
            'options': seralizer1.data
        }
        return Response(seralizer)


# # 연금 top3
# @api_view(['GET'])
# def top_aps(request):  
#     print(request.POST)  
    
#     # 모든 유저 정보
#     user_all = User.objects.all()

#     # 필터링된 유저들이 가입한 상품
#     products = {}
    
#     for user in user_all:
#         financial_products = user.financial_products
#         for product in financial_products:
#             if product:
#                 products.setdefault(product[1], 0)
#                 products[product[1]] += 1

#     print('상품', products)
#     sorted_products = dict(sorted(products.items(), key=lambda item: item[1], reverse=True))

#     # 연금 베스트
#     aps_best = []
#     aps = AnnuitySavingProduct.objects.all()
#     print(f'연금 : {aps}')
#     for ap in aps:
#         product_no = ap.fin_prdt_cd
#         for key, value in sorted_products.items():
#             if product_no == key:
#                 aps_best.append((value, key))
    
#     # 연금 베스트 정렬
#     aps_best.sort(reverse=True)
#     # sorted_dps_best = dict(sorted(dps_best.items(), key=lambda item: item[1], reverse=True))
#     print(f'연금 베스트: {aps_best}')
#     # 연금 top
#     aps_top = aps_best[:3]


#     return Response(aps_top)

# 금리계산 함수
def calculate(request, user_pk):
    user = User.objects.get(pk=user_pk)
