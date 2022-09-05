from django.urls import path
from .views import SignUpView, LoginView, login, logout, tg_login
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/',     SignUpView.as_view(), name='signup'),
    path('login', login,      name='login'),
    path('tg_login', tg_login,name='tg_login'),
    path('logout', logout,    name='out'),
    path('profile/<str:username>', views.UserDetailView.as_view(), name='profile'),
    path('index', views.UserListView.as_view(), name='index'),
#    path('telegram_auth/<m>', tg_auth),

#    path('login', LoginView.as_view())
]
