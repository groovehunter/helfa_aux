from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot
from django.utils.text import slugify
from django.conf import settings

import logging
lg = logging.getLogger('root')

from verschenka.models import Item, Category

"""
@processor(state_manager, from_states=state_types.All)
def hello_world(bot: TelegramBot, update: Update, state: TelegramState):
  result = bot.sendMessage(update.get_chat().get_id(), 'Hello!')
  lg.debug("type", update.type())
  lg.debug("descrition", result.description())
"""

def save_it():
  pass

@processor(state_manager, from_states=state_types.All)
def item_save(bot: TelegramBot, update: Update, state: TelegramState):
  type = update.type()
  lg.debug(type)
  #lg.debug( dir(type))
  if type == 'photo': #message_types.Photo:
    lg.debug('msg is photo')
  if type == 'message': #message_types.Text:
    message = update.get_message()
    text= message.get_text()
    author = getattr(message,'from')
    lg.debug(author.username)
    descr = ''
    if not "\n" in text:  #oneliner
      name = text
    else:
      descr = text
      name = text.split('\n')[0]
    item = Item()
    item.name = name
    item.descr = descr
    item.slug = slugify(name)
    item.save()
    item_url = settings.BASE_URL + item.get_absolute_url()
    """
    """
    #item_url = 'test'
    msg = 'Dein Inserat wurde auf der website eingetragen: ' + item_url
  else:
    msg = 'Es ist ein Fehler aufgetreten beim Speichern.'

  chat_id = update.get_chat().get_id()
  result = bot.sendMessage(chat_id, msg)
  lg.debug(chat_id, update.type())
  lg.debug(result)
