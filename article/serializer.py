from rest_framework import serializers
from .models import Comments, Articles

from users.serializers import UserViewSerializer
from drf_extra_fields.fields import Base64ImageField

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
            return obj.user.email
    
    class Meta:
        model = Comments
        fields = "__all__"


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("content",)


class ArticleSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True)
    author = serializers.SerializerMethodField()
    def get_author(self, obj):
        return obj.author.email
    
    class Meta:
        model = Articles
        fields = "__all__"


class ArticleCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    class Meta:
        model = Articles
        fields = ["title","content","image"]

class ArticleListSerializer(serializers.ModelSerializer):
    author = UserViewSerializer()
    likes = UserViewSerializer(many=True)
    class Meta:
        model = Articles
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'likes', 'image']


class ArticleSearchSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    class Meta:
        model=Articles
        fields = '__all__'