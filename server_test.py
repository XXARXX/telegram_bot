import unittest

import server

class TestServer(unittest.TestCase):
    def setUp(self):
        self.test_client = server.app.test_client()

    def test_send_message_get_method(self):
        response = self.test_client.get('/api/send_message')
        assert '405 METHOD NOT ALLOWED' in response.status

    def test_send_message_post_method(self):
        response = self.test_client.post(
            '/api/send_message', 
            data=b'{"id": "293bf460-acf6-434f-af88-b53d0691ef1f", "chat_id": "5037333810", "msg": "Hello, world"}',
            mimetype='application/json'
        )
        assert '200 OK' in response.status

    def test_get_message_status(self):
        response = self.test_client.get('/api/get_message_status')
        assert '200 OK' in response.status