from http import client
import json

from .config import load_config

HOST = 'api.telegram.org'
REQ_TEMPLATE = '/bot{token}/{api_method}{query}'

class TelegramApi:
    """
    Simple telegram REST api wrapper

    Attributes
    ----------
    bot_token : str
        Token used in telegram api
    conn : HTTPConnection
        Telegram api http connection

    Methods
    -------

    get_me()
        Returns information about bot
    send_message(chat_id, text)
        Sends text to chat_id chat
    get_updates()
        Return updates related with bot
    _request(request_method, api_method, api_data='')
        Utility method for communicating with telegram bot api
    """
    def __init__(self, bot_token = None):
        self.bot_token = bot_token
        self.conn = client.HTTPSConnection(HOST)

    def get_me(self):
        """
        Returns
        -------
        dictionary
            status
                request status
            error_message optional
                if status 'error' contain error description
            data optional
                if status 'success' contain returned data
        """
        return self._request('GET', 'getMe')

    def send_message(self, chat_id, text):
        """
        Returns
        -------
        dictionary
            status
                request status
            error_message optional
                if status 'error' contain error description
            data optional
                if status 'success' contain returned data
        """
        api_data = {
            'chat_id': chat_id,
            'text': text
        }
        return self._request('POST', 'sendMessage', api_data)
    
    def get_updates(self):
        """
        Returns
        -------
        dictionary
            status
                request status
            error_message optional
                if status 'error' contain error description
            data optional
                if status 'success' contain returned data
        """
        return self._request('GET', 'getUpdates')

    # TODO: get query
    def _request(self, request_method, api_method, api_data = ''):
        """
        Parameters
        ----------
        request_method : str
            HTTP method GET or POST
        api_method : str
            api endpoint
        api_data : str
            data for endpoint

        Returns
        -------
        dictionary
            status
                request status
            error_message optional
                if status 'error' contain error description
            data optional
                if status 'success' contain returned data
        
        Raises
        ------
        NotImplementedError
            If trying sending api_data trough GET method
        http.client.HTTPException
            If trying use other methods except GET and POST
        """
        url = ''
        query = ''
        result = None
        try:
            if request_method in ['GET', 'get']:
                if query != '':
                    raise NotImplementedError('get query not supported')
                url = REQ_TEMPLATE.format(token=self.bot_token, api_method=api_method, query=query)
                self.conn.request(request_method, url)
                    
            elif request_method in ['POST', 'post']:
                url = REQ_TEMPLATE.format(token=self.bot_token, api_method=api_method, query=query)
                self.conn.request(request_method, url, body=json.dumps(api_data), headers={'Content-Type': 'application/json'})
            else:
                raise client.HTTPException('unsupported request method: %s' % request_method)
        except client.HTTPException as e:
            result = {
                'status': 'error',
                'error_message': e
            }
        except TimeoutError:
            result = {
                'status': 'error',
                'error_message': 'cant connect to remote host'
            }

        if result is None:
            response = self.conn.getresponse()
            if response.status != 200:
                result = {
                    'status': 'error',
                    'error_message': response.reason
                }
            response.body = json.load(response)
            if not response.body.get('ok'):
                result = {
                    'status': 'error',
                    'error_message': response.body.get('description')
                }
            else:
                result = {
                    'status': 'success',
                    'data': response.body.get('result')
                }

            self.conn.close()

        return result
