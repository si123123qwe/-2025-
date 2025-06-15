from django.db import models
from django.conf import settings

# 금융회사
class Company(models.Model):
    dcls_month = models.TextField()             # 공시 제출월[YYYYMM]
    fin_co_no = models.TextField()              # 금융회사코드
    kor_co_nm = models.TextField()              # 금융회사명
    dcls_chrg_man = models.TextField()          # 공시담당자
    homp_url = models.TextField()               # 홈페이지 주소
    cal_tel = models.TextField()                # 콜센터 전화번호


# 금융회사 옵션
class CompanyOption(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)    # 외래키
    dcls_month = models.TextField()
    fin_co_no = models.TextField()          # 금융회사코드
    area_cd = models.TextField()            # 지역구분
    area_nm = models.TextField()            # 지역이름
    exis_yn = models.BooleanField()         # 점포 소재 여부


# 예금 상품
class DepositProduct(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)    # 외래키
    dcls_month = models.TextField()             # 공시 제출월[YYYYMM]
    fin_co_no = models.TextField()   # 금융회사코드
    kor_co_nm = models.TextField()              # 금융회사명
    fin_prdt_cd = models.TextField() # 금융 상품 코드
    fin_prdt_nm = models.TextField()            # 금융 상품명
    join_way = models.TextField(null=True)               # 가입방법
    mtrt_int = models.TextField()               # 만기 후 이자율
    spcl_cnd = models.TextField()               # 우대조건
    join_deny = models.IntegerField(choices=((1, '제한 없음'), (2, '서민전용'), (3, '일부제한')))           # 가입제한(1:제한 없음, 2: 서민전용, 3: 일부제한)
    join_member = models.TextField()            # 가입대상
    etc_note = models.TextField()               # 금융 상품 설명
    max_limit = models.IntegerField(null=True)           # 최고한도
    dcls_strt_day = models.TextField()          # 공시 시작일
    dcls_end_day = models.TextField(null=True)           # 공시 종료일
    fin_co_subm_day = models.TextField()        # 금융회사 제출일 [YYYYMMDDHH24MI]


# 예금 상품 옵션
class DepositOption(models.Model):
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE)   # 외래키
    dcls_month = models.TextField()
    fin_co_no = models.TextField()
    fin_prdt_cd = models.TextField()   # 금융 상품 코드
    intr_rate_type = models.TextField()
    intr_rate_type_nm = models.CharField(max_length=100)    # 저축금리 유형명
    intr_rate = models.FloatField()     # 저축금리
    intr_rate2 = models.FloatField()    # 최고우대금리
    save_trm = models.IntegerField()    # 저축기간 (단위: 개월)


# 적금 상품
class SavingProduct(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)    # 외래키
    dcls_month = models.TextField()             # 공시 제출월[YYYYMM]
    fin_co_no = models.TextField()   # 금융회사코드
    kor_co_nm = models.TextField()              # 금융회사명
    fin_prdt_cd = models.TextField() # 금융 상품 코드
    fin_prdt_nm = models.TextField()            # 금융 상품명
    join_way = models.TextField(null=True)               # 가입방법
    mtrt_int = models.TextField()               # 만기 후 이자율
    spcl_cnd = models.TextField()               # 우대조건
    join_deny = models.IntegerField(choices=((1, '제한 없음'), (2, '서민전용'), (3, '일부제한')))           # 가입제한(1:제한 없음, 2: 서민전용, 3: 일부제한)
    join_member = models.TextField()            # 가입대상
    etc_note = models.TextField()               # 금융 상품 설명
    max_limit = models.IntegerField(null=True)           # 최고한도
    dcls_strt_day = models.TextField()          # 공시 시작일
    dcls_end_day = models.TextField(null=True)           # 공시 종료일
    fin_co_subm_day = models.TextField()        # 금융회사 제출일 [YYYYMMDDHH24MI]


# 적금 상품 옵션
class SavingOption(models.Model):
    product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE)
    dcls_month = models.TextField()
    fin_co_no = models.TextField()
    fin_prdt_cd = models.TextField()   # 금융 상품 코드
    intr_rate_type = models.TextField()
    intr_rate_type_nm = models.CharField(max_length=100)    # 저축금리 유형명
    rsrv_type = models.TextField()
    rsrv_type_nm = models.TextField()   # 적립 유형
    save_trm = models.IntegerField()    # 저축기간 (단위: 개월)
    intr_rate = models.FloatField()     # 저축금리
    intr_rate2 = models.FloatField()    # 최고우대금리


# 연금저축 상품
class AnnuitySavingProduct(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)    # 외래키
    dcls_month = models.TextField()             # 공시 제출월[YYYYMM]
    fin_co_no = models.TextField()   # 금융회사코드
    fin_prdt_cd = models.TextField() # 금융 상품 코드
    kor_co_nm = models.TextField()              # 금융회사명
    fin_prdt_nm = models.TextField()            # 금융 상품명
    join_way = models.TextField(null=True)               # 가입방법
    pnsn_kind = models.TextField()  # 연금종류
    pnsn_kind_nm = models.TextField()   # 연금종류명
    sale_strt_day = models.TextField()  # 판매 개시일
    mntn_cnt = models.IntegerField()   # 유지건수[단위: 건] 또는 설정액 [단위: 원]
    prdt_type = models.TextField()  # 상품유형
    prdt_type_nm = models.TextField()   # 상품유형명
    avg_prft_rate = models.FloatField()
    dcls_rate = models.FloatField(null=True) # 공시이율 [소수점 2자리]
    guar_rate = models.TextField(null=True) # 최저 보증이율
    btrm_prft_rate_1 = models.FloatField(null=True)  # 과거 수익률1(전년도) [소수점 2자리]
    btrm_prft_rate_2 = models.FloatField(null=True)  # 과거 수익률2(전전년도) [소수점 2자리]
    btrm_prft_rate_3 = models.FloatField(null=True)  # 과거 수익률3(전전전년도) [소수점 2자리]
    etc = models.TextField(null=True)    # 기타 사항
    sale_co = models.TextField(null=True)    # 판매사
    dcls_strt_day = models.TextField()          # 공시 시작일
    dcls_end_day = models.TextField(null=True)           # 공시 종료일
    fin_co_subm_day = models.TextField()        # 금융회사 제출일 [YYYYMMDDHH24MI]


# 연금저축 옵션
class AnnuitySavingOption(models.Model):
    product = models.ForeignKey(AnnuitySavingProduct, on_delete=models.CASCADE)
    dcls_month = models.TextField()
    fin_co_no = models.TextField()
    fin_prdt_cd = models.TextField()
    pnsn_recp_trm = models.JSONField(default=list, blank=True)
    pnsn_recp_trm_nm = models.JSONField(default=list, blank=True)
    pnsn_entr_age = models.JSONField(default=list, blank=True)
    pnsn_entr_age_nm = models.JSONField(default=list, blank=True)
    mon_paym_atm = models.JSONField(default=list, blank=True)
    mon_paym_atm_nm = models.JSONField(default=list, blank=True)
    paym_prd = models.JSONField(default=list, blank=True)
    paym_prd_nm = models.JSONField(default=list, blank=True)
    pnsn_strt_age = models.JSONField(default=list, blank=True)
    pnsn_strt_age_nm = models.JSONField(default=list, blank=True)
    pnsn_recp_amt = models.IntegerField()


# 주택담보대출 상품
class MortgageLoanProduct(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)    # 외래키
    dcls_month = models.TextField()
    fin_co_no = models.TextField()
    fin_prdt_cd = models.TextField()
    kor_co_nm = models.TextField()
    fin_prdt_nm = models.TextField()
    join_way = models.TextField()
    loan_inci_expn = models.TextField()
    erly_rpay_fee = models.TextField()
    dly_rate = models.TextField()
    loan_lmt = models.TextField()
    dcls_strt_day = models.TextField(null=True)
    dcls_end_day = models.TextField(null=True)

# 주택담보대출 옵션
class MortgageLoanOption(models.Model):
    product = models.ForeignKey(MortgageLoanProduct, on_delete=models.CASCADE)
    dcls_month = models.TextField()
    fin_co_no = models.TextField()
    fin_prdt_cd = models.TextField()
    mrtg_type = models.TextField()
    mrtg_type_nm = models.TextField()
    rpay_type = models.TextField()
    rpay_type_nm = models.TextField()
    lend_rate_type = models.TextField()
    lend_rate_type_nm = models.TextField()
    lend_rate_min = models.FloatField()
    lend_rate_max = models.FloatField()
    lend_rate_avg = models.TextField(null=True)

# 전세자금대출 상품
class RentHouseLoanProduct(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)    # 외래키
    dcls_month = models.TextField()
    fin_co_no = models.TextField()
    fin_prdt_cd = models.TextField()
    kor_co_nm = models.TextField()
    fin_prdt_nm = models.TextField()
    join_way = models.TextField()
    loan_inci_expn = models.TextField()
    erly_rpay_fee = models.TextField()
    dly_rate = models.TextField()
    loan_lmt = models.TextField()
    dcls_strt_day = models.TextField()
    dcls_end_day = models.TextField(null=True)
    fin_co_subm_day = models.TextField()

# 전세자금대출 옵션
class RentHouseLoanOption(models.Model):
    product = models.ForeignKey(RentHouseLoanProduct, on_delete=models.CASCADE)
    dcls_month = models.TextField()
    fin_co_no = models.TextField()
    fin_prdt_cd = models.TextField()
    rpay_type = models.TextField()
    rpay_type_nm = models.TextField()
    lend_rate_type = models.TextField()
    lend_rate_type_nm = models.TextField()
    lend_rate_min = models.FloatField()
    lend_rate_max = models.FloatField()
    lend_rate_avg = models.FloatField(null=True)

# 개인신용대출 상품
class CreditLoanProduct(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)    # 외래키
    dcls_month = models.TextField()
    fin_co_no = models.TextField()
    fin_prdt_cd = models.TextField()
    kor_co_nm = models.TextField()
    fin_prdt_nm = models.TextField()
    join_way = models.TextField()
    cb_name = models.TextField()
    crdt_prdt_type = models.TextField()
    crdt_prdt_type_nm = models.TextField()
    dcls_strt_day = models.TextField()
    dcls_end_day = models.TextField(null=True)
    fin_co_subm_day = models.TextField()

# 개인신용대출 옵션
class CreditLoanOption(models.Model):
    product = models.ForeignKey(CreditLoanProduct, on_delete=models.CASCADE)
    dcls_month = models.TextField()
    fin_co_no = models.TextField()
    fin_prdt_cd = models.TextField()
    crdt_prdt_type = models.TextField()
    crdt_lend_rate_type = models.TextField()
    crdt_lend_rate_type_nm = models.TextField()
    crdt_grad_1 = models.FloatField(null=True)
    crdt_grad_4 = models.FloatField(null=True)
    crdt_grad_5 = models.FloatField(null=True)
    crdt_grad_6 = models.FloatField(null=True)
    crdt_grad_10 = models.FloatField(null=True)
    crdt_grad_11 = models.FloatField(null=True)
    crdt_grad_12 = models.FloatField(null=True)
    crdt_grad_13 = models.FloatField(null=True)
    crdt_grad_avg = models.FloatField(null=True)
    