import unittest
import os

from telegram_api import TelegramApi

class TestTelegramApi(unittest.TestCase):
    def setUp(self):
        self.api = TelegramApi()

    def test_get_me(self):
        print()
        user = self.api.get_me()
        print(user.get('id'))
        print(user.get('is_bot'))
        print(user.get('first_name'))
        print(user.get('last_name'))
        print(user.get('username'))