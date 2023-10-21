import json

from flask import Flask, request

from .telegram_api import TelegramApi
from . import sql

app = Flask(__name__)

status_queue = []

api = TelegramApi()

@app.post('/api/send_message')
def rest_send_msg():
    if request.method == 'POST':
        handle_message(request.get_json())
        return 'OK'

@app.get('/api/get_message_status')
def rest_get_message_status():
    id = request.args.get('id')
    if id:
        status = sql.get(id)
        message = None
        if status != 'success':
            message = {
                'id': id,
                'status': 'error',
                'error_message': status
            }
        else:
            message = {
                'id': id,
                'status': status
            }
        
        return json.dumps(message)
    return 'test'


def handle_message(message):
    validate_message(message)
    status = {
        'id': message.get('id', None),
        'status': 'failed'
    }

    result = api.send_message(int(message.get('chat_id')), message.get('msg'))
    if result:
        status['status'] = 'success'

    sql.insert(status)

    status_queue.append(status)

def validate_message(message):
    keys = ['id', 'chat_id', 'msg']
    for key in keys:
        if key not in message:
            raise 'key "%s" not found' % key
