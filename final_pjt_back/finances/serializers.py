from rest_framework import serializers
from .models import Company, CompanyOption
from .models import DepositProduct, DepositOption
from .models import SavingProduct, SavingOption
from .models import AnnuitySavingProduct, AnnuitySavingOption
from .models import MortgageLoanProduct, MortgageLoanOption
from .models import RentHouseLoanProduct, RentHouseLoanOption
from .models import CreditLoanProduct, CreditLoanOption

# 금융회사
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


# 금융회사 옵션
class CompanyOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyOption
        fields = '__all__'
        read_only_fields = ['company']


# 예금 상품
class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'


# 예금 상품 옵션
class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'
        read_only_fields = ['product']


# 적금 상품
class SavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'


# 적금 상품 옵션
class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'
        read_only_fields = ['product']
        
        
# 연금저축 상품
class AnnuitySavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnuitySavingProduct
        fields = '__all__'


# 연금저축 옵션
class AnnuitySavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnuitySavingOption
        fields = '__all__'
        read_only_fields = ['product']
        
        
# 주택담보 대출 상품
class MortgageLoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortgageLoanProduct
        fields = '__all__'


# 주택담보 대출 옵션
class MortgageLoanOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortgageLoanOption
        fields = '__all__'
        read_only_fields = ['product']


# 전세자금 대출 상품
class RentHouseLoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentHouseLoanProduct
        fields = '__all__'


# 전세자금 대출 옵션
class RentHouseLoanOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentHouseLoanOption
        fields = '__all__'
        read_only_fields = ['product']
        
        
# 신용 대출 상품
class CreditLoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditLoanProduct
        fields = '__all__'


# 신용 대출 옵션
class CreditLoanOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditLoanOption
        fields = '__all__'
        read_only_fields = ['product']
