from django.urls import path
from . import views

urlpatterns = [
    # 게시판 글 목록 불러오기
    path('articles/', views.article_list),
    # 게시판 글 상세보기
    path('articles/<int:article_pk>/', views.article_detail),
    # 좋아요 기능
    path('articles/<int:article_pk>/like/', views.article_like),
    # 댓글 목록 및 작성
    path('articles/<int:article_pk>/comments/', views.comment_list),
    # 댓글 단일
    path('comments/<int:comment_pk>/', views.comment_detail),
]
