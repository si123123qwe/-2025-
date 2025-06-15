from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field, user_username

class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
    )
    SAVING_TYPE_CHOICES = [
        ('thrifty', '알뜰형'),
        ('challenging', '도전형'),
        ('diligent', '성실형'),
    ]

    username = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField(blank=True, null=True)
    address = models.TextField(help_text="예: '서울특별시 마포구 연남동 사파리월드 12-3'", blank=True)

    # 월급, 자산, 목표 자산, 가입한 금융 상품
    salary = models.IntegerField(blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
    target_asset = models.IntegerField(blank=True, null=True)
    financial_products = models.JSONField(default=list, blank=True)

    # 포트폴리오
    saving_type = models.CharField(max_length=20, choices=SAVING_TYPE_CHOICES, blank=True, null=True)
    favorite_company = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    mbti = models.CharField(max_length=4, blank=True, null=True)  # MBTI 필드 추가

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        nickname = data.get("nickname")
        gender = data.get("gender")
        age = data.get("age")
        address = data.get("address")
        money = data.get("money")
        salary = data.get("salary")
        target_asset = data.get("target_asset")
        saving_type = data.get("saving_type")
        favorite_company= data.get("favorite_company")
        mbti = data.get("mbti")

        financial_product = data.get("financial_products")

        # user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if nickname:
            user_field(user, "nickname", nickname)
        if gender:
            user.gender = gender
        if age:
            user.age = age
        if address:
            user.address = address
        if money:
            user.money = money
        if salary:
            user.salary = salary
        if target_asset:
            user.target_asset = target_asset
        if saving_type in dict(User.SAVING_TYPE_CHOICES):
            user.saving_type = saving_type
        if favorite_company:
            user.favorite_company = favorite_company
        if mbti:
            user.mbti = mbti
        if financial_product:
            financial_products = user.financial_products.split(',')
            financial_products.append(financial_product)
            if len(financial_products) > 1:
                financial_products = ','.join(financial_products)
            user_field(user, "financial_products", financial_products)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user
    