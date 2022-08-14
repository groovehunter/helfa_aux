from django.conf import settings

bot_name = settings.TELEGRAM_BOT_NAME
bot_token = settings.TELEGRAM_BOT_TOKEN
redirect_url = settings.TELEGRAM_LOGIN_REDIRECT_URL
import logging
lg = logging.getLogger()

from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import (
    NotTelegramDataError,
    TelegramDataIsOutdatedError,
)

from django_telegram_login.widgets.constants import (
    SMALL,
    MEDIUM,
    LARGE,
    DISABLE_USER_PHOTO,
)
from django_telegram_login.widgets.generator import (
    create_callback_login_widget,
    create_redirect_login_widget,
)


def prepare_login_widget_callback():
  telegram_login_widget = create_callback_login_widget(
    bot_name, corner_radius=10, size=MEDIUM
  )

def prepare_login_widget_redirect():
  login_widget = create_redirect_login_widget(
    redirect_url, bot_name, size=LARGE, user_photo=DISABLE_USER_PHOTO
  )
  return login_widget

def prepare_login_widget():
  return prepare_login_widget_redirect()


def verify_tg(request_get):
  try:
    result = verify_telegram_authentication(bot_token=bot_token, request_data=request_get)
    return result

  except TelegramDataIsOutdatedError:
    return False
    # XXX better error


"""
def callback(request):
    telegram_login_widget = create_callback_login_widget(bot_name, size=SMALL)
    context = {'telegram_login_widget': telegram_login_widget}
    return render(request, 'telegram_auth/callback.html', context)


def redirect(request):
    telegram_login_widget = create_redirect_login_widget(
        redirect_url, bot_name, size=LARGE, user_photo=DISABLE_USER_PHOTO
    )
    context = {'telegram_login_widget': telegram_login_widget}
    return render(request, 'telegram_auth/redirect.html', context)

def tg_auth(request, m):
    if m == 'redirect':
      return redirect(request)
    if m == 'callback':
      return callback(request)

"""


