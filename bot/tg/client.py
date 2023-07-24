import logging
from typing import Any, TypeVar, Type

import requests
from django.conf import settings
from pydantic import BaseModel, ValidationError

from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse

T = TypeVar('T', bound=BaseModel)
logger = logging.getLogger()


class TgClientException(Exception):
    ...


class TgClient:
    def __init__(self, token: str | None = settings.BOT_TOKEN):
        self.__token = token
        self.__url = f'https://api.telegram.org/bot{self.__token}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        data = self._get('getUpdates', offset=offset, timeout=timeout)
        return self.__serialize_response(GetUpdatesResponse, data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        data = self._get('sendMessage', chat_id=chat_id, text=text)
        return self.__serialize_response(SendMessageResponse, data)

    def __get_url(self, method: str) -> str:
        return f'{self.__url}{method}'

    def _get(self, command: str, **params: Any):
        url = self.__get_url(command)
        params.setdefault('timeout', 60)
        response = requests.get(url, params=params)
        if not response.ok:
            logger.warning('Invalid status code from Telegram %d on command %s', response.status_code, command)
            logger.debug('Tg response: %s', response.text)
            if command == 'getUpdates':
                return {'ok': False, 'result': []}
            raise TgClientException

        return response.json()

    @staticmethod
    def __serialize_response(serializer_class: Type[T], data: dict) -> T:
        try:
            return serializer_class(**data)
        except ValidationError:
            logger.error('Failed to serialize response with data %s', data)
            raise TgClientException