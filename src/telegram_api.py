from http import client
import json

from .config import load_config

HOST = 'api.telegram.org'
REQ_TEMPLATE = '/bot{token}/{api_method}{query}'

# TODO: Consider custom exceptions
# TODO: Remove debug level
class TelegramApi:
    def __init__(self):
        self.bot_token = load_config()['token']
        self.conn = client.HTTPSConnection(HOST)

    def get_me(self):
        data = self._request('GET', 'getMe')
        return data

    def send_message(self, chat_id, text):
        api_data = {
            'chat_id': chat_id,
            'text': text
        }
        data = self._request('POST', 'sendMessage', api_data)
        return data
    
    def get_updates(self):
        data = self._request('GET', 'getUpdates')

    # TODO: get query
    def _request(self, request_method, api_method, api_data = ''):
        url = ''
        query = ''
        if request_method in ['GET', 'get']:
            if query != '':
                raise NotImplementedError('get query not supported')
            url = REQ_TEMPLATE.format(token=self.bot_token, api_method=api_method, query=query)
            self.conn.request(request_method, url)
        elif request_method in ['POST', 'post']:
            url = REQ_TEMPLATE.format(token=self.bot_token, api_method=api_method, query=query)
            self.conn.request(request_method, url, body=json.dumps(api_data), headers={'Content-Type': 'application/json'})
        else:
            raise Exception('unsupported request method: %s' % request_method)

        response = self.conn.getresponse()
        if response.status != 200:
            print('request error {status}: {reason}'.format(status=response.status, reason=response.reason))
        response.body = json.load(response)
        if not response.body.get('ok'):
            print('server return error {0}'.format(body))

        self.conn.close()
        return vars(response)
