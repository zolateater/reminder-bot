import enum
from datetime import datetime
from typing import List

"""
For all available types see:
https://core.telegram.org/bots/api#available-types

Since we do not need all of the types, we are not going to present all of them.
"""

class User():
    def __init__(self,
                 id: int,
                 first_name: str,
                 last_name: str = None,
                 username: str = None,
                 language_code: str = None):
        self.id = id
        self.first_name = first_name
        self.username = username
        self.language_code = language_code
        self.last_name = last_name


@enum.unique
class ChatType(enum.Enum):
    """
    Type of chat, can be either “private”, “group”, “supergroup” or “channel”
    """
    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"

class Chat():
    def __init__(self, id: int, type: ChatType, title: str = None, username: str = None,
                 first_name: str = None, last_name: str = None):
        """
        :param int id: Unique identifier for this chat.
        :param ChatType type: Type of chat.
        :param str title: Title, for supergroups, channels and group chats.
        :param srt username: Username, for private chats, supergroups and channels if available
        :param str first_name: First name of the other party in a private chat
        :param str last_name: Last name of the other party in a private chat
        """
        self.id = id
        self.type = type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

@enum.unique
class MessageEntityType(enum.Enum):
    """
    Can be mention (@username), hashtag, bot_command, url, email,
    bold (bold text), italic (italic text), code (monowidth string), pre (monowidth block),
    text_link (for clickable text URLs), text_mention (for users without usernames)
    """
    TYPE_MENTION = 'mention'
    TYPE_HASHTAG = 'hashtag'
    TYPE_BOT_COMMAND = 'bot_command'
    TYPE_URL = 'url'
    TYPE_EMAIL = 'email'
    TYPE_BOLD = 'bold'
    TYPE_ITALIC = 'italic'
    TYPE_CODE = 'code'
    TYPE_PRE = 'pre'
    TYPE_TEXT_LINK = 'text_link'
    TYPE_TEXT_MENTION = 'text_mention'


class MessageEntity():
    """
    MessageEntity
    This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc.
    """

    def __init__(self, type: MessageEntityType, offset: int, length: int, url: str=None, user: User=None):
        """
        :param str type: Type of the entity.
        :param int offset: Offset in UTF-16 code units to the start of the entity
        :param int length: Length of the entity in UTF-16 code units
        :param str url: Optional. For “text_link” only, url that will be opened after user taps on the text
        :param User user: Optional. For “text_mention” only, the mentioned user
        """
        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user


class Message():
    def __init__(self, id: int, date: datetime, chat: Chat, text: str = "", user_from: User = None, entities: List[MessageEntity]=None):
        """
        :param int id: Unique message identifier inside this chat
        :param int date: Date the message was sent in Unix time
        :param Chat chat: Conversation the message belongs to
        :param str text: For text messages, the actual UTF-8 text of the message, 0-4096 characters.
        :param User user_from: Sender, can be empty for messages sent to channels
        :param list entities: Array of MessageEntity. For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text
        """
        if entities is None:
            entities = []
        self.id = id
        self.date = date
        self.chat = chat
        self.text = text
        self.user_from = user_from
        self.entities = entities


class Update():
    def __init__(self, update_id: int, message: Message = None):
        self.update_id = update_id
        self.message = message
