'''
This module provides general access to the official Telegram Bot API by
implementing useful functions.
'''

import requests

class Bot():
    '''
    This class represents the bot. To keep the bot token private, the
    execution environment has to be setup, e.g. in a local file '.env'.

    Environment variables are:

    TELEGRAM_BOT_TOKEN
        the respective bot token given by BotFather
    '''

    def __init__(self, token):
        self._token = token

    @property
    def token(self):
        '''
        Returns the bot's token (previously set in __init__).
        '''
        return self._token

    def send_msg(self, msg, to):
        '''
        Sends the given message 'msg' to the user 'to', where 'to' is
        the user's chat_id (int) or the username (string) of the target
        channel (in the format @channelusername)
        '''
        return requests.post(self.func_url("sendMessage"), data={
            'chat_id': to,
            'text': msg
        })

    # --- webhook ---

    @property
    def webhook_info(self):
        '''
        Returns the webhook info provided by Telegram Bot API in json
        format (as python dict).
        '''
        return requests.get(self.func_url('getWebhookInfo')).json()

    @property
    def webhook_url(self):
        '''
        Returns the webhook url (string).
        '''
        return self.webhook_info['result']['url']

    @webhook_url.setter
    def webhook_url(self, url):
        '''
        Sets the webhook of this bot so incoming updates will be
        forwarded to it.
        '''
        return requests.get(self.func_url('setWebhook'), data={'url': url})

    def set_webhook_url_adding_token(self, url):
        '''
        Sets the webhook of this bot so incoming updates will be
        forwarded to it.
        Adds the bot's token after the given 'url'.
        '''
        return requests.get(self.func_url('setWebhook'), data={
            'url': f'{url}/{self.token}'
        })

    # --- utils ---

    def func_url(self, method):
        '''
        Helper method to access the Telegram Bot API.
        '''
        return "https://api.telegram.org/bot{}/{}".format(self.token, method)

