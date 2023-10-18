import unittest
import os

import config_ops

class TestConfigOps(unittest.TestCase):
    def test_config_load_token(self):
        token = config_ops.load_token('test_cfg.xml')
        assert token == 'test_token:2135_4fASDf'
    
    def test_config_make_config(self):
        token = 'test_token:to_save12345'
        config_ops.make_config(token, 'test_save_cfg.xml')
        with open('test_save_cfg.xml') as f:
            data = f.read()
            assert token in data
        os.remove('test_save_cfg.xml')