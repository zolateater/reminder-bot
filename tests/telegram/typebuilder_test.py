import pytest
import unittest
from src.telegram.typebuilder import *


class TestUserBuilder(unittest.TestCase):
    def test_parse_error_is_formed_when_wrong_payload(self):
        """
        :return:
        """
        exception = None
        try:
            UserBuilder().build(1)
        except ParseError as e:
            exception = e

        assert isinstance(exception, ParseError)
        assert exception.class_name == "User"
        assert exception.payload == 1

        # Catches previous exception (it should be TypeError)
        assert isinstance(exception.previous, TypeError)

    def test_user_is_formed_when_only_mandatory_data(self):
        user = UserBuilder().build({"id": "1234", "first_name": "Johnny"})
        assert isinstance(user, User)
        assert user.first_name == "Johnny"
        assert user.id == 1234

    def test_user_is_formed_when_all_data(self):
        user = UserBuilder().build({"id": "1234", "first_name": "Johnny",
                                    "last_name": "Cage", "language_code": "en-US", "username": "@johnnycage"})
        assert isinstance(user, User)
        assert user.last_name == "Cage"
        assert user.language_code == "en-US"
        assert user.username == "@johnnycage"

class UpdateBuilderTest(unittest.TestCase):
    def test_update_parsing(self):
        update_dict = {
            'update_id': 1,
            'message':
                {
                    'message_id': 1,
                    'chat':
                        {
                            'first_name': 'test_first_name',
                            'id': 1,
                            'type': 'private',
                            'username': 'test_username',
                            'last_name': 'test_last_name'
                        },
                    'date': 1497713955,
                    'text': '1'
                }
        }

        update_obj = UpdateBuilder().build(update_dict)
        assert isinstance(update_obj.message, Message)
        assert update_obj.update_id == 1
