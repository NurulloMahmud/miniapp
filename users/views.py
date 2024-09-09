from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from .models import TelegramUser
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import verify_telegram_auth  # Telegram hash verification
from .serializers import TelegramUserSerializer
from .permissions import IsSuperUser


class TelegramLoginView(APIView):

    def post(self, request):
        user_data = request.data
        token = "your-telegram-bot-token"  # Replace with your actual bot token

        # Verify the authenticity of the Telegram data
        if not verify_telegram_auth(user_data, token):
            return Response({"error": "Invalid authentication data"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract user information from Telegram
        telegram_id = user_data.get('id')
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name', '')
        username = user_data.get('username', None)
        is_premium = user_data.get('is_premium', False)
        photo_url = user_data.get('photo_url', None)
        language_code = user_data.get('language_code', None)

        # Check if user exists or create a new one (implicit registration)
        user, created = TelegramUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'is_premium': is_premium,
                'photo_url': photo_url,
                'language_code': language_code,
                'auth_date': now(),
            }
        )

        # Update user details if the user already exists
        if not created:
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.is_premium = is_premium
            user.photo_url = photo_url
            user.language_code = language_code
            user.auth_date = now()
            user.save()

        # Generate and return a JWT token with custom user fields
        refresh = RefreshToken.for_user(user)
        token_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.telegram_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
        }

        return Response(token_data, status=status.HTTP_200_OK)


class TelegramUserListView(generics.ListAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]

