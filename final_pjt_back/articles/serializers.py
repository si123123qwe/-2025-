from rest_framework import serializers
from .models import Article, Comment


# 게시판 글 리스트
class ArticleListSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        fields = ('id', 'username', 'title', 'content')


# 게시판 댓글 조회 
class CommentSerializer(serializers.ModelSerializer):
    # override
    article = ArticleListSerializer(read_only=True)
    username = serializers.ReadOnlyField(source='author.username') 


    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author',)


# 게시판 글 단일
class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    username = serializers.ReadOnlyField(source='author.username')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # 한글로 요일 및 날짜 표시
        korean_created_at = instance.created_at.strftime("%Y년 %m월 %d일 (%A)")
        korean_updated_at = instance.updated_at.strftime("%Y년 %m월 %d일 (%A)")

        representation['created_at'] = korean_created_at.replace(
            'Monday', '월요일').replace('Tuesday', '화요일').replace('Wednesday', '수요일').replace(
            'Thursday', '목요일').replace('Friday', '금요일').replace('Saturday', '토요일').replace(
            'Sunday', '일요일')
        representation['updated_at'] = korean_updated_at.replace(
            'Monday', '월요일').replace('Tuesday', '화요일').replace('Wednesday', '수요일').replace(
            'Thursday', '목요일').replace('Friday', '금요일').replace('Saturday', '토요일').replace(
            'Sunday', '일요일')
        return representation

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('author', 'like_authors')