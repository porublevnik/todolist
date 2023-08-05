from rest_framework import generics, permissions
from rest_framework.request import Request
from rest_framework.response import Response

from bot.models import TGUser
from bot.serializers import TGUserSerializer
from bot.tg.client import TgClient


class VerificationView(generics.GenericAPIView):
    serializer_class = TGUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request: Request, *args, **kwargs) -> Response:
        serializer = TGUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tg_user: TGUser = serializer.save(user=request.user)
        TgClient().send_message(chat_id=tg_user.chat_id, text='Bot token has been verified')
        return Response(serializer.data)
    