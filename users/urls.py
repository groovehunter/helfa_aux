from django.urls import path
from .views import SignUpView, LoginView, login, logout, tg_login, profile


app_name = 'users'

urlpatterns = [
    path('signup/',     SignUpView.as_view(), name='signup'),
    path('login', login, name='login'),
    path('tg_login', tg_login),
    path('logout', logout, name='out'),
    path('profile', profile),
#    path('telegram_auth/<m>', tg_auth),

#    path('login', LoginView.as_view())
]
