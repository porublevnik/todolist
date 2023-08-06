from django.core.management import BaseCommand

from bot.tg.client import TgClient
from bot.tg.dc import Message
from bot.models import TGUser


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()
    def handle(self, *args, **options):
        offset = 0

        self.stdout.write(self.style.SUCCESS('Bot start handling...'))

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message) -> None:
        tg_user, _ = TGUser.objects.get_or_create(
            chat_id=msg.message_from.id, defaults={'username': msg.message_from.username}
        )
        if not tg_user.is_verified:
            tg_user.update_verification_code()
            self.tg_client.send_message(msg.message_from.id, text=tg_user.verification_code)
        else:
            self.handle_auth_user(tg_user, msg)


    def handle_auth_user(self, tg_user: TGUser, msg: Message) -> None:
        print('Обработка')