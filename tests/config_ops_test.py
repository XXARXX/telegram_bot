import unittest
import os

from src import config_ops

class TestConfigOps(unittest.TestCase):
    def test_config_load_token(self):
        token = config_ops.load_token('test_cfg.xml')
        assert token == 'test_token:2135_4fASDf'
    
    def test_config_make_config(self):
        args = {'token': 'test_token:to_save12345'}
        config_ops.make_config(args, 'test_save_cfg.xml')
        with open('test_save_cfg.xml') as f:
            data = f.read()
            assert args['token'] in data
        os.remove('test_save_cfg.xml')