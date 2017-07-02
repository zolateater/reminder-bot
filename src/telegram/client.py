import json
from .request import *

"""
Фасад для взаимодействия с API телеграма.
Содержит высокоуровневые методы, полагаясь на подклассы в вопросе делалей
"""
class TelegramClient():

    ATTEMPTS = 0

    def __init__(self, request_builder: RequestBuilder, client: AbstractHttpClient):
        """
        :param RequestBuilder request_builder:
        :param AbstractHttpClient client:
        """
        self.last_update_id = -1
        self.request_builder = request_builder
        self.client = client

    def set_on_message_handler(self, handler: callable):
        """
        Adds request listener.
        When message will be delivered, handler will be called with one argument - response body,
        which is list of updates. Each update is simply a dict, since we don't want to
        :param handler:
        :return:
        """
        self.handler = handler

    def send_message(self, chat_id: str, text: str, parse_mode: str='html') -> TelegramResponse:
        """
        Execute sendMessage API method
        :param chat_id:
        :param text:
        :param parse_mode:
        :return:
        """
        params = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        return self.client.exec(self.request_builder.build("sendMessage", RequestBuilder.HTTP_POST, params))

    def listen(self, timeout: int=5) -> None:
        """
        Blocks execution until messages is received.
        :param int timeout:
        :return:
        """

        request = self.build_get_updates_request(self.last_update_id, timeout)
        response = self.client.exec(request)
        json_response = json.loads(str(response.body, 'utf8'))

        if "result" in json_response:
            updates = json_response['result']
            if len(updates) != 0:
                self.handler(updates)
                self.last_update_id = updates[len(updates) - 1]['update_id'] + 1

    def build_get_updates_request(self, last_update_id: int, timeout: int) -> TelegramRequest:
        """
        Builds API request for getting updates.
        :param token: str
        :param last_update_id: int
        :param timeout: int
        :return: str
        """
        return self.request_builder.build("getUpdates", RequestBuilder.HTTP_GET, {
            "timeout": str(timeout),
            "offset": str(last_update_id)
        })

"""
Factory for building clients
"""
class TelegramFactory:
    @staticmethod
    def get_client(token: str) -> TelegramClient:
        """
        Builds general telegram client.
        :param str token:
        :return:
        """
        return TelegramClient(RequestBuilder(token), HttpClient())