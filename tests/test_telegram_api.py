import unittest
import os

from src import config
from src.telegram_api import TelegramApi

class TestTelegramApi(unittest.TestCase):
    def setUp(self):
        self.api = TelegramApi()
        conf_path = 'test_config.xml'
        c = config.load_config(conf_path)
        self.api.bot_token = c['token']
        self.config = c

    def test_get_me(self):
        result = self.api.get_me()
        self.assertEqual(result.get('status'), 'success')
        user = result.get('data')
        self.assertEqual(user.get('is_bot'), True)

    def test_send_message(self):
        result = self.api.send_message(self.config['chatid'], 'test')
        self.assertEqual('success', result.get('status'))