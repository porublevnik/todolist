from django.db import models

from core.models import User


class TGUser(models.Model):
    chat_id = models.IntegerField(primary_key=True, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    verification_code = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.__class__.name} ({self.chat_id})'
