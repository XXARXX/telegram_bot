import unittest
import os

from src.telegram_api import TelegramApi

class TestTelegramApi(unittest.TestCase):
    def setUp(self):
        self.api = TelegramApi()

    def test_get_me(self):
        result = self.api.get_me()
        self.assertEqual(result.get('status'), 200)
        body = result.get('body')
        self.assertEqual(body.get('ok'), True)
        user = body.get('result')
        self.assertEqual(user.get('is_bot'), True)