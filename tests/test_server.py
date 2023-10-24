from pathlib import Path
import unittest

from src.server import create_app
from src.config import load_config
from src import sql
import json

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        conf_path = 'test_config.xml'
        self.test_client = create_app(conf_path).test_client()
        self.config = load_config(conf_path)
        p = Path(self.config['database'])
        if p.exists() and p.is_file():
            p.unlink()
        sql.create_db(self.config['database'])

    @classmethod
    def tearDownClass(self):
        p = Path(self.config['database'])
        if p.exists() and p.is_file():
            p.unlink()

    def test_send_message_get_method(self):
        response = self.test_client.get('/api/send_message')
        assert '405 METHOD NOT ALLOWED' in response.status

    def test_send_message_post_method(self):
        response = self.test_client.post(
            '/api/send_message', 
            data=('{"id": "293bf460-acf6-434f-af88-b53d0691ef1f", "chat_id": "%s", "msg": "Hello, world"}' % self.config['chatid']).encode('utf-8'),
            mimetype='application/json'
        )
        assert '200 OK' in response.status
    
    def test_send_message_post_method_no_chat_id(self):
        response = self.test_client.post(
            '/api/send_message', 
            data=('{"id": "293bf460-acf6-434f-af88-b53d0691ef1f", "msg": "Hello, world"}').encode('utf-8'),
            mimetype='application/json'
        )
        assert '400' in response.status

    def test_send_message_post_method_no_msg(self):
        response = self.test_client.post(
            '/api/send_message', 
            data=('{"id": "293bf460-acf6-434f-af88-b53d0691ef1f", "chat_id": "%s"}' % self.config['chatid']).encode('utf-8'),
            mimetype='application/json'
        )
        assert '400' in response.status

    def test_send_message_post_method_no_id(self):
        response = self.test_client.post(
            '/api/send_message', 
            data=('{"chat_id": "%s", "msg": "Hello, world"}' % self.config['chatid']).encode('utf-8'),
            mimetype='application/json'
        )
        assert '400' in response.status

    def test_get_message_status_error(self):
        id = 1
        sql.insert({'id': '%s' % id, 'status': 'test'}, self.config['database'])
        response = self.test_client.get('/api/get_message_status?id=%s' % id)
        assert '200 OK' in response.status
        parsed_data = json.loads(response.data)
        assert str(id) in parsed_data.get('id')
        assert 'error' in parsed_data.get('status')
        assert 'test' in parsed_data.get('error_message')
    
    def test_get_message_status_success(self):
        id = 2
        sql.insert({'id': '%s' % id, 'status': 'success'}, self.config['database'])
        response = self.test_client.get('/api/get_message_status?id=%s' % id)
        assert '200 OK' in response.status
        parsed_data = json.loads(response.data)
        assert str(id) in parsed_data.get('id')
        assert 'success' in parsed_data.get('status')
    
    def test_get_message_status_not_found(self):
        id = 3
        response = self.test_client.get('/api/get_message_status?id=%s' % id)
        assert '200 OK' in response.status
        parsed_data = json.loads(response.data)
        assert str(id) in parsed_data.get('id')
        assert 'error' in parsed_data.get('status')
        assert 'not found' in parsed_data.get('error_message')