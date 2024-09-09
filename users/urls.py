from django.urls import path
from .views import (
    TelegramLoginView, TelegramUserListView
)

urlpatterns = [
    path('api/login/', TelegramLoginView.as_view(), name='telegram-login'),
    path('api/users/', TelegramUserListView.as_view(), name='telegram-users'),
]
