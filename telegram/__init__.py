'''
This module provides general access to the official Telegram Bot API by
implementing useful functions.
'''

from os import environ as env

import requests

class Bot():
    '''
    This class represents the bot. To keep the bot token private, the
    execution environment has to be setup, e.g. in a local file '.env'.

    Environment variables are:

    TELEGRAM_BOT_TOKEN
           the respective bot token given by BotFather
    '''

    @property
    def token(self):
        '''
        Returns the value of the environment variable
        'TELEGRAM_BOT_TOKEN'.
        '''
        return env['TELEGRAM_BOT_TOKEN']

    ###########################################################################
    # webhook

    @property
    def webhook_info(self):
        '''
        Returns the webhook info provided by Telegram Bot API in json
        format (string).
        '''
        return requests.get(self.get_url('getWebhookInfo'))

    @property
    def webhook(self):
        '''
        Returns the webhook url (string).
        '''
        import json
        info = json.loads(self.webhook_info)
        return info['result']['url']

    @webhook.setter
    def webhook(self, url):
        '''
        Sets the webhook of this bot so incoming updates will be
        forwarded to it.
        '''
        return requests.get(self.get_url('setWebhook'), data={'url': url})

    ###########################################################################
    # utils

    def get_url(self, method):
        '''
        Helper method to access the Telegram Bot API.
        '''
        return "https://api.telegram.org/bot{}/{}".format(self.token, method)
