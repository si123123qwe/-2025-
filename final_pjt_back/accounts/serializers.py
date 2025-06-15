from rest_framework import serializers
from django.contrib.auth import get_user_model

from allauth.account import app_settings as allauth_settings
from allauth.utils import get_username_max_length
from allauth.account.adapter import get_adapter
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class CustomRegistorSerializer(RegisterSerializer):
    nickname = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255
    )
    gender = serializers.CharField(max_length=1, required=True)
    age = serializers.IntegerField(required=False)
    address = serializers.CharField(max_length=255, required=True)
    money = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)
    target_asset = serializers.IntegerField(required=False)
    saving_type = serializers.CharField(max_length=255, required=False)
    favorite_company = serializers.CharField(max_length=255, required=False)
    mbti = serializers.CharField(max_length=4, required=False)

    financial_products = serializers.ListField(child=serializers.IntegerField(), required=False)

    def get_cleaned_data(self):
        return {
        'username': self.validated_data.get('username', ''),
        'password1': self.validated_data.get('password1', ''),
        'nickname': self.validated_data.get('nickname', ''),
        'gender': self.validated_data.get('gender', ''),
        'age': self.validated_data.get('age', ''),
        'address': self.validated_data.get('address', ''),
        'money': self.validated_data.get('money', ''),
        'salary': self.validated_data.get('salary', ''),
        'target_asset': self.validated_data.get('target_asset', ''),
        'financial_products': self.validated_data.get('financial_products', ''),
        'saving_type': self.validated_data.get('saving_type', ''),
        'favorite_company': self.validated_data.get('favorite_company', ''),
        'mbti':self.validated_data.get('mbti', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user
