'''
This module provides general access to the official Telegram Bot API by
implementing useful functions.
'''

import requests

class SupportedMethod:
  SEND_MSG = 'sendMessage'
  GET_WEBHOOK_INFO = 'getWebhookInfo'
  SET_WEBHOOK = 'setWebhook'
  DELETE_WEBHOOK = 'deleteWebhook'


class Webhook:
  def __init__(self, token):
    self._token = token

  @property
  def token(self):
    return self._token

  def url_for(self, method):
    '''
    Helper method to access the Telegram Bot API.
    '''
    return "https://api.telegram.org/bot{}/{}".format(
      self._token,
      method)

  @property
  def info(self):
    '''
    Returns the webhook info provided by Telegram Bot API in json
    format (as python dict).
    '''
    url = self.url_for(SupportedMethod.GET_WEBHOOK_INFO)
    return requests.get(url).json()

  @property
  def url(self):
    '''
    Returns the webhook url (string).
    '''
    return self.info['result']['url']

  def set_url_adding_token(self, base_url):
    '''
    Sets the webhook of this bot so incoming updates will be
    forwarded to it.
    Adds the bot's token after the given 'url'.
    '''
    api_url = self.url_for(SupportedMethod.SET_WEBHOOK)
    return requests.get(api_url, data={'url': f'{base_url}/{self.token}'})

  def delete(self):
    api_url = self.url_for(SupportedMethod.DELETE_WEBHOOK)
    return requests.get(api_url)


class Bot():
  def __init__(self, token):
    self._webhook = Webhook(token)

  @property
  def webhook(self):
    return self._webhook

  @property
  def token(self):
    return self.webhook._token

  def send_msg(self, msg, to):
    '''
    Sends the given message 'msg' to the user 'to', where 'to' is
    the user's chat_id (int) or the username (string) of the target
    channel (in the format @channelusername)
    '''
    url = self.webhook.url_for(SupportedMethod.SEND_MSG)
    data = {
      'chat_id': to,
      'text': msg
    }
    return requests.post(url=url, data=data)

