from .models import Member, Post
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def create(self, validated_data):
        user = Member.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            nickname = validated_data['nickname'],
            qual = validated_data.get('qual',None),
            introduce = validated_data.get('introduce',None)
        )
        return user
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'
    
    def create(self, validated_data):
        post=Post.objects.create_post(
            title=validated_data['title'],
            text=validated_data['text']
        )
        return post