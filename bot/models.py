from django.db import models
from django.utils.crypto import get_random_string

from core.models import User


class TGUser(models.Model):
    chat_id = models.IntegerField(primary_key=True, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    verification_code = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.__class__.__name__} ({self.chat_id})'

    @staticmethod
    def _generate_verification_code() -> str:
        return get_random_string(20)

    def update_verification_code(self) -> None:
        self.verification_code = self._generate_verification_code()
        self.save(update_fields=['verification_code'])

    @property
    def is_verified(self) -> bool:
        return bool(self.user)