from django.db import models
from django.contrib.auth.models import AbstractBaseUser



class TelegramUser(AbstractBaseUser):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    photo_url = models.URLField(null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    language_code = models.CharField(max_length=10, null=True, blank=True)
    auth_date = models.DateTimeField()

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.telegram_id})"

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"
        db_table = "telegram_users"

