from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import TelegramUser



class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'username', 'first_name', 'last_name', 'photo_url', 'is_premium', 'language_code']

class TelegramUserTokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'first_name', 'last_name', 'token']

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Call the base class validate method to generate the token
        data = super().validate(attrs)
        
        # Add custom fields to the token response
        data.update({
            'user_id': self.user.telegram_id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'username': self.user.username,
        })
        
        return data
