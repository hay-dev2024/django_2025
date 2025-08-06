# Serializers
from rest_framework import serializers
from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__' # 모두 가져올 때
        # fields = ['title', 'content'] # 특정 필드만 가져올 때
