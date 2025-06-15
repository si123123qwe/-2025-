from django.urls import path
from . import views


urlpatterns = [
    path('user/', views.userinfo),
    path('update-user/', views.update_user, name='update_user'),
]
