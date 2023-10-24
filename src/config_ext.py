from flask import g

from .config import *

class ConfigExtension:
    """
    Adds token to flask.g context
    """
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app, config_path=None):
        """
        Initialize app with config data
        

        Raises
        ------
        config.ConfigError
            if token not found in config file
        """
        config = None
        if config_path is None:
            config = load_config()
        else:
            config = load_config(config_path)
        
        if 'token' not in config:
            raise ConfigError("'token' not found in config")
        
        self.token = config['token']
        self.db_path = config['database']

        @app.before_request
        def with_token():
            g.token = self.token
            g.db_path = self.db_path