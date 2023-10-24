from src.server import create_app
from src.telegram_api import TelegramApi

t = TelegramApi()
c = create_app().test_client()

def send_message(id, message):
    data = ('{"id": "%s", "chat_id": "5037333810", "msg": "%s"}' % (id, message)).encode('utf-8')
    response = c.post(
        '/api/send_message',
        data=data,
        mimetype='application/json'
    )

    return response

def get_status(id):
    query = '/api/get_message_status?id=%s' % id
    response = c.get(
        query
    )

    return response

def get_me():
    return t.get_me()