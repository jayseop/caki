from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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
        )
        return user
    


class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['nickname'] = user.nickname
        token['qual'] = user.qual

        return token