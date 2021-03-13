'''
This module provides general access to the official Telegram Bot API by
implementing useful functions.
'''

import json

class Update:

  def __init__(self, data: dict):
    self.update_id = data.get('update_id')
    self.message = Message.new(data.get('message'))
    self.callback_query = CallbackQuery.new(data.get('callback_query'))

  def as_dict(self) -> dict:
    d = {}
    if self.update_id is not None:
      d['update_id'] = self.update_id
    if self.message is not None:
      d['message'] = self.message.as_dict()
    if self.callback_query is not None:
      d['callback_query'] = self.callback_query.as_dict()
    return d

class Message:

  def __init__(self):
    #raise Exception('Use Message.new(data: dict) instead')
    pass

  @staticmethod
  def new(data: dict):
    if data is None:
      return None
    else:
      message = Message()
      message.id = data.get('message_id')
      message.sender = User.new(data.get('from'))
      message.chat = Chat.new(data.get('chat'))
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

class User:

  def __init__(self):
    #raise Exception('Use User.new(data: dict) instead')
    pass

  @staticmethod
  def new(data: dict):
    if data is None:
      return None
    else:
      sender = User()
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

  def __init__(self):
    #raise Exception('Use Chat.new(data: dict) instead')
    pass

  @staticmethod
  def new(data: dict):
    if data is None:
      return None
    else:
      chat = Chat()
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

class CallbackQuery:

  def __init__(self):
    #raise Exception('Use CallbackQuery.new(data: dict) instead')
    pass

  @staticmethod
  def new(data: dict):
    if data is None:
      return None
    else:
      chat = Chat()
      chat.id = data.get('id')
      chat.sender = User.new(data.get('from'))
      chat.message = Message.new(data.get('message'))
      chat.chat_instance = data.get('chat_instance')
      chat.data = data.get('data')
      return chat

  def as_dict(self):
    d = {}
    if self.id is not None:
      d['id'] = self.id
    if self.sender is not None:
      d['from'] = self.sender.as_dict()
    if self.message is not None:
      d['message'] = self.message.as_dict()
    if self.chat_instance is not None:
      d['chat_instance'] = self.chat_instance
    if self.data is not None:
      d['data'] = self.data
    return d

