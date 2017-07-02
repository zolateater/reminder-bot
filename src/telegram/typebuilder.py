from .type import *
from abc import ABC, abstractmethod
from functools import wraps
import pdb


class ParseError(Exception):
    """
    Represents an error happening during parsing process.
    """
    def __init__(self, class_name: str, payload: dict, previous: Exception):
        self.class_name = class_name
        self.payload = payload
        self.previous = previous

def exception_as_parse_error(func):
    @wraps(func)
    def wrapper(self, data):
        """
        Wrapper function for method which is building an object from one argument.
        For building we won't need to use more that one arg, so we do not use *args and **kwargs
        :param self:
        :param data:
        :return:
        """
        if not isinstance(self, AbstractBuilder):
            raise TypeError("exception_as_parse_error decorator is only for classes extending AbstractBuilder")
        try:
            return func(self, data)
        except Exception as e:
            raise ParseError(self.get_building_class_name(), data, e)
    return wrapper

class AbstractBuilder(ABC):
    """
    Base abstract class for building telegram types from dict (which are parsed json).
    Method "get_building_class_name" is used for finding class,
    for which parsing has failed thus making debug easier.
    """
    @abstractmethod
    def get_building_class_name(self) -> str:
        """
        Returns class (telegram type) name which is being constructed.
        :return:
        """
        pass

class UserBuilder(AbstractBuilder):
    """
    User object builder
    """
    def get_building_class_name(self) -> str:
        return User.__name__

    @exception_as_parse_error
    def build(self, telegram_data: dict) -> User:
        return User(
            id=int(telegram_data['id']),
            first_name=telegram_data['first_name'],
            last_name=telegram_data.get('last_name'),
            username=telegram_data.get('username'),
            language_code=telegram_data.get('language_code')
        )

class ChatBuilder(AbstractBuilder):
    """
    Chat object builder
    """
    def get_building_class_name(self) -> str:
        return Chat.__name__

    @exception_as_parse_error
    def build(self, telegram_data: dict) -> Chat:
        chat_type = ChatType(telegram_data['type'])
        return Chat(
            id=int(telegram_data['id']),
            type=chat_type,
            title=telegram_data.get('title'),
            username=telegram_data.get('username'),
            first_name=telegram_data.get('first_name'),
            last_name=telegram_data.get('last_name')
        )

class MessageEntityBuilder(AbstractBuilder):
    """
    Message entity builder.
    """
    def get_building_class_name(self) -> str:
        return MessageEntity.__name__

    @exception_as_parse_error
    def build(self, telegram_data: dict) -> MessageEntity:
        user = telegram_data.get('user')
        return MessageEntity(
            MessageEntityType(telegram_data['type']),
            int(telegram_data['offset']),
            int(telegram_data['length']),
            telegram_data.get('url'),
            UserBuilder().build(user) if user is not None else None
        )

class MessageBuilder(AbstractBuilder):
    """
    Message builder.
    """
    def get_building_class_name(self) -> str:
        return Message.__name__

    @exception_as_parse_error
    def build(self, telegram_data: dict):
        chat = ChatBuilder().build(telegram_data['chat'])
        user_from = None
        entities = None
        message_text = telegram_data['text']

        if 'from' in telegram_data:
            user_from = UserBuilder().build(telegram_data['from'])

        # Создание MessageEntity с текстом
        if 'entities' in telegram_data:
            entity_builder = MessageEntityBuilder()
            entities = []
            for entity_data in telegram_data['entities']:
                entity = entity_builder.build(entity_data)
                entity.text = entity.extract_text_from(message_text)
                entities.append(entity)

        return Message(
            id=telegram_data['message_id'],
            date=datetime.fromtimestamp(int(telegram_data['date'])),
            chat=chat,
            text=message_text,
            user_from=user_from,
            entities=entities
        )

class UpdateBuilder(AbstractBuilder):
    """
    Update builder
    """
    @exception_as_parse_error
    def build(self, telegram_data: dict) -> Update:
        return Update(
            int(telegram_data['update_id']),
            MessageBuilder().build(telegram_data['message']) if 'message' in telegram_data else None
        )

    def get_building_class_name(self) -> str:
        return Update.__name__

