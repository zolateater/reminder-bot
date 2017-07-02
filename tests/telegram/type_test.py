from src.telegram.type import *
import datetime

"""
Создание сообщения и MessageEntities для теста
"""
def build_message(entities_offsets: list, msg_text: str) -> Message:
    """
    Создание тестового сообщения с переданными MessageEntity и текстом
    :param entities:
    :param msg_text:
    :return:
    """
    entities = list(map(
        lambda x: MessageEntity(MessageEntityType(MessageEntityType.TYPE_MENTION), offset=x[0], length=x[1]),
        entities_offsets
    ))

    fake_chat = Chat(0, ChatType(ChatType.PRIVATE))
    return Message(id=0, date=datetime.datetime.now(), chat=fake_chat, text=msg_text, entities=entities)

"""
Тесты получения текста сообщения с различными MessageEntity
"""

def test_get_message_text_without_entities_no_entities():
    msg = build_message([], "test")
    assert msg.get_text_without_entities() == "test"


def test_get_message_text_without_entities_two_entities():
    msg = build_message([(0, 13)], "/setsomething 1, 2")
    assert msg.get_text_without_entities() == " 1, 2"

def test_get_message_text_without_entities_one_entity():
    msg = build_message([(0, 19), (20, 13)], "@SpecialReminderBot /setsomething 1, 2")
    assert msg.get_text_without_entities() == "  1, 2"