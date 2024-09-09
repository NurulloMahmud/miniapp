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
from django.conf import settings

bot_token = settings.BOT_TOKEN


class TelegramLoginView(APIView):

    def post(self, request):
        # Extract init data from the Authorization header
        auth_header = request.headers.get('Authorization', '')
        auth_type, auth_data = auth_header.split(' ') if auth_header else ('', '')

        if auth_type != 'tma' or not auth_data:
            return Response({"error": "Unauthorized: Invalid Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)

        token = "your-telegram-bot-token"  # Replace with your bot token

        # Verify the init data with the bot token
        is_valid, parsed_data = verify_telegram_auth(auth_data, token)

        if not is_valid:
            return Response({"error": "Invalid authentication data"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract user information from the parsed data
        telegram_id = parsed_data['id']
        first_name = parsed_data.get('first_name', '')
        last_name = parsed_data.get('last_name', '')
        username = parsed_data.get('username', None)

        # Now, proceed with creating or logging in the user as usual
        user, created = TelegramUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'auth_date': now(),
            }
        )

        # Update user details if the user already exists
        if not created:
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
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

