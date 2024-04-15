from .models import Member
from django.db import models
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password1')

        user = Member.objects.create_user(
            email = email,
            password = password
        )
        return user


        # member_db = Member.objects.create(
        #     email = validated_data['email'],
        #     password = validated_data['password'],
        #     nickname = validated_data['nickname'],
        #     qual = '1' if validated_data['qual'] else '0',
        #     introduce = validated_data['introduce']
        # )
        # member_db.save()
        return user