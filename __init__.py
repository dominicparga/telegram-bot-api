'''
This module provides general access to the official Telegram Bot API by
implementing useful functions.
'''

import json
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

  def send_msg(self, msg, to, inline_keyboard=None):
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
    if inline_keyboard is not None:
      data['reply_markup'] = json.dumps({
        'inline_keyboard': inline_keyboard
      })
    return requests.post(url=url, data=data)

class Input:

  def __init__(self, data: dict):
    self.update_id = data.get('update_id')
    self.message = Input.Message.new(data.get('message'))

  def as_dict(self) -> dict:
    d = {}
    if self.update_id is not None:
      d['update_id'] = self.update_id
    if self.message is not None:
      d['message'] = self.message.as_dict()
    return d

  class Message:

    @staticmethod
    def new(data: dict):
      if data is None:
        return None
      else:
        message = Input.Message()
        message.id = data.get('message_id')
        message.sender = Input.Message.Sender.new(data.get('from'))
        message.chat = Input.Message.Chat.new(data.get('chat'))
        message.date = data.get('date')
        message.text = data.get('text')
        return message

    def as_dict(self) -> dict:
      d = {}
      if self.id is not None:
        d['message_id'] = self.id
      if self.sender is not None:
        d['from'] = self.sender.as_dict()
      if self.chat is not None:
        d['chat'] = self.chat.as_dict()
      if self.date is not None:
        d['date'] = self.date
      if self.text is not None:
        d['text'] = self.text
      return d

    class Sender:

      @staticmethod
      def new(data: dict):
        if data is None:
          return None
        else:
          sender = Input.Message.Sender()
          sender.id = data.get('id')
          sender.is_bot = data.get('is_bot')
          sender.first_name = data.get('first_name')
          sender.last_name = data.get('last_name')
          sender.username = data.get('username')
          sender.language_code = data.get('language_code')
          return sender

      def as_dict(self):
        d = {}
        if self.id is not None:
          d['id'] = self.id
        if self.is_bot is not None:
          d['is_bot'] = self.is_bot
        if self.first_name is not None:
          d['first_name'] = self.first_name
        if self.last_name is not None:
          d['last_name'] = self.last_name
        if self.username is not None:
          d['username'] = self.username
        if self.language_code is not None:
          d['language_code'] = self.language_code
        return d

    class Chat:

      @staticmethod
      def new(data: dict):
        if data is None:
          return None
        else:
          chat = Input.Message.Chat()
          chat.id = data.get('id')
          chat.first_name = data.get('first_name')
          chat.last_name = data.get('last_name')
          chat.username = data.get('username')
          chat.type = data.get('type')
          return chat

      def as_dict(self):
        d = {}
        if self.id is not None:
          d['id'] = self.id
        if self.first_name is not None:
          d['first_name'] = self.first_name
        if self.last_name is not None:
          d['last_name'] = self.last_name
        if self.username is not None:
          d['username'] = self.username
        if self.type is not None:
          d['type'] = self.type
        return d

