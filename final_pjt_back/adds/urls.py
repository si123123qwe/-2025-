from django.urls import path
from . import views

app_name = 'adds'
urlpatterns = [
    path('exchange-rate/', views.exchange_rate, name='exchange_rate'),
]
