from rest_framework import serializers, exceptions

from bot.models import TGUser


class TGUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.IntegerField(source='chat_id', read_only=True)
    username = serializers.CharField(allow_null=True, read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    verification_code = serializers.CharField(write_only=True)

    class Meta:
        model = TGUser
        fields = ('tg_id', 'username', 'user_id', 'verification_code')
        read_only_field = ('tg_id', 'username', 'user_id')

    def validate_verification_code(self, code: str) -> str:
        try:
            self.instance = TGUser.objects.get(verification_code=code)
        except TGUser.DoesNotExist:
            raise exceptions.ValidationError('Неправильный код верификации')
        return code

