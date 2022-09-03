import telegram # this is from python-telegram-bot package
import django
django.setup()

from django.conf import settings
from django.template.loader import render_to_string
#settings.configure()
from verschenka.models import Event

def post_event_on_telegram(event):
    message_html = render_to_string('telegram_message.html', {
        'event': event
    })
    telegram_settings = settings.TELEGRAM
    bot = telegram.Bot(token=telegram_settings['bot_token'])
    bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
                     text=message_html, parse_mode=telegram.ParseMode.HTML)


from datetime import datetime

if __name__ == '__main__':
  event = Event(title='asdadsa')
  soon = datetime.now()
  event.start_date = soon
  post_event_on_telegram(event)
