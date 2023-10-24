from flask import g

from .config import *
from .telegram_api import TelegramApi

class TelegramExtension:
    """
    Flask application extension that adds telegram api to global context

    Attributes
    ----------
    api : TelegramApi
        TelegramApi instance
    """
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """
        Initialize app with TelegramApi context

        Note
        ----
        'token' key should be already in flask.g

        Raises
        ------
        RuntimeError
            if bot token not present in context
        """

        self.api = TelegramApi()

        @app.before_request
        def with_telegram_api():
            """
            Push TelegramApi as g.api
            """
            g.api = self.api
            bot_token = g.get('token')
            if bot_token is None:
                raise RuntimeError('bot token not found in context')
            g.api.bot_token = bot_token