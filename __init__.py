'''
This module provides general access to the official Telegram Bot API by
implementing useful functions.
'''

import json
import requests
from . import data

def check_with_exception(response):
  if not response.ok:
    response = response.json()
    raise Exception('{} ({})'.format(
      response['description'],
      response['error_code']))
  return response

class SupportedMethod:
  SEND_MSG = 'sendMessage'
  EDIT_MSG_TEXT = 'editMessageText'
  ANSWER_CALLBACK_QUERY = 'answerCallbackQuery'
  GET_WEBHOOK_INFO = 'getWebhookInfo'
  SET_WEBHOOK = 'setWebhook'
  DELETE_WEBHOOK = 'deleteWebhook'

class Webhook:

  def __init__(self, token, check_response=lambda x: x):
    self._token = token
    self._check_response = check_response

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
    return self._check_response(requests.get(url).json())

  @property
  def url(self):
    '''
    Returns the webhook url (string).
    '''
    return self.info['result']['url']

  def set_url_adding_token(self, base_url, certificate = None):
    '''
    Sets the webhook of this bot so incoming updates will be
    forwarded to it.
    Adds the bot's token after the given 'url'.
    '''
    api_url = self.url_for(SupportedMethod.SET_WEBHOOK)
    content = {'url': f'{base_url}/{self.token}'}
    if certificate is not None:
      content['certificate'] = certificate
    return self._check_response(requests.get(api_url, data=content))

  def delete(self):
    api_url = self.url_for(SupportedMethod.DELETE_WEBHOOK)
    return self._check_response(requests.get(api_url))

class Bot():

  def __init__(self, token, check_response=lambda x:x):
    self._webhook = Webhook(token, check_response=check_response)
    self._check_response = check_response

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
    content = {
      'chat_id': to,
      'text': msg
    }
    if inline_keyboard is not None:
      keyboard_data = []
      for row in inline_keyboard:
        new_row = []
        for button in row:
          if isinstance(button, data.InlineKey):
            new_row.append({
              'text': button.text,
              'callback_data': button.callback_data
            })
          else:
            new_row.append(button)
        keyboard_data.append(new_row)
      content['reply_markup'] = json.dumps({
        'inline_keyboard': keyboard_data
      })
    return self._check_response(requests.post(url=url, data=content))

  def answer_callback_query(
    self,
    callback_query_id,
    text=None,
    is_alert_not_notification=False
  ):
    url = self.webhook.url_for(SupportedMethod.ANSWER_CALLBACK_QUERY)
    content = {
      'callback_query_id': callback_query_id,
      'show_alert': is_alert_not_notification
    }
    if text is not None:
      content['text'] = text
    return self._check_response(requests.post(url=url, data=content))

  def edit_msg_text(self, chat_id, msg_id, new_text, inline_keyboard=None):
    url = self.webhook.url_for(SupportedMethod.EDIT_MSG_TEXT)
    content = {
      'chat_id': chat_id,
      'message_id': msg_id,
      'text': new_text
    }
    if inline_keyboard is not None:
      content['reply_markup'] = json.dumps({
        'inline_keyboard': inline_keyboard
      })
    return self._check_response(requests.post(url=url, data=content))

