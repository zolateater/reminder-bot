import requests
from typing import Dict
from abc import abstractmethod, ABC

"""
This module contains classes and functions for
handling transport aspects of Telegram API
"""

"""
Represents HTTP request to the API call.
"""
class TelegramRequest():
    def __init__(self, url: str, http_method: str, params: dict):
        """
        :param token:
        :param http_method:
        :param params:
        """
        self.uri = url
        self.http_method = http_method
        self.params = params

"""
Response from Telegram API.
A wrapper used for type hint.
"""
class TelegramResponse():
    def __init__(self, http_status: int, body: bytearray):
        """
        Initializes telegram response
        :param int status:
        :param bytearray body:
        """
        self.http_status = http_status
        self.body = body

"""
Helper for building API request
"""
class RequestBuilder():
    HTTP_GET = 'GET'
    HTTP_POST = 'POST'

    @classmethod
    def is_method_allowed(cls, http_method: str) -> bool:
        """
        Method which allows to validate if HTTP method is supported
        by current application.
        :param http_method:
        :return:
        """
        return http_method in [cls.HTTP_GET, cls.HTTP_POST]

    def __init__(self, token: str):
        """
        Initializes request builder.
        :param str token: Your telegram API token
        """
        self.__token__ = token

    def build(self, method_name: str, http_method: str, params: Dict[str, str]) -> TelegramRequest:
        """
        :param str method_name: Method name in Telegram API.
        :param str http_method: Used http verb. Depends on used method.
        :param Dict[str, str] params: Method parameters.
        :return: TelegramAPIRequest
        """

        if not self.__class__.is_method_allowed(http_method):
            raise ValueError("Http method {} is not supported".format(http_method))

        url = "https://api.telegram.org/bot{}/{}".format(
            self.__token__,
            method_name
        )

        return TelegramRequest(url=url, http_method=http_method, params=params)

"""
Абстрактный HTTP-клиент.
Наличие всего одного метода позволяет достаточно просто подменить клиент.
"""
class AbstractHttpClient(ABC):
    @abstractmethod
    def exec(self, request: TelegramRequest) -> TelegramResponse:
        """
        Abstract method.
        Executes Telegram API Request, returns API Response
        :param request: TelegramAPIRequest
        :return:
        """
        pass

"""
Default client which uses 'requests' python library.
"""
class HttpClient(AbstractHttpClient):
    def exec(self, request: TelegramRequest) -> TelegramResponse:
        """
        Send request using 'requests' python library.
        :param TelegramRequest request:
        :return TelegramResponse:
        """
        if request.http_method == RequestBuilder.HTTP_GET:
            raw_response = requests.get(url=request.uri, params=request.params)
        else:
            raw_response = requests.post(url=request.uri, params=request.params)

        response = TelegramResponse(raw_response.status_code, raw_response.content)
        return response