from .models import Member
from rest_framework import serializers
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
 
    def create(self, validated_data):
        user = Member.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            nickname = validated_data['nickname'],
            qual = None,
            introduce = None,
            image_path = None,
        )
        return user