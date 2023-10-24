import json

from flask import Flask, request, g, abort

from . import sql
from .config_ext import ConfigExtension
from .telegram_api_ext import TelegramExtension

def create_app(config='config.xml'):
    """
    Create flask app with extensions

    Returns
    -------
    app : flask.Flask
        flask app instance
    """
    config_extension = ConfigExtension()
    telegram_extension = TelegramExtension()

    app = Flask(__name__)
    config_extension.init_app(app, config)
    telegram_extension.init_app(app)

    status_queue = []

    @app.post('/api/send_message')
    def rest_send_msg():
        handle_message(request.get_json())
        return 'OK'

    @app.get('/api/get_message_status')
    def rest_get_message_status():
        id = request.args.get('id')
        message = None
        if id:
            status = sql.get(id, g.db_path)
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

        return json.dumps({'id': id, 'status': 'error', 'error_message': 'id not found'})


    def handle_message(message):
        try:
            validate_message(message)
        except ValueError as e:
            abort(400, e)
        
        status = {
            'id': message.get('id', None),
            'status': ''
        }

        result = g.api.send_message(int(message.get('chat_id')), message.get('msg'))

        status_message = ''
        if result['status'] == 'success':
            status_message = result['status']
        else:
            status_message = result['error_message']
        sql.insert({'id': message.get('id'), 'status': status_message}, g.db_path)

    def validate_message(message):
        keys = ['id', 'chat_id', 'msg']
        for key in keys:
            if key not in message:
                raise ValueError('key "%s" not found' % key)

    return app