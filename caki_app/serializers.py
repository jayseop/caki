from .models import Member
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
            qual = validated_data['qual'],
            introduce = validated_data['introduce']
        )
        return user