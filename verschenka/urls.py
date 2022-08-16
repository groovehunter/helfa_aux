from django.urls import path, re_path, include

from . import views

app_name = 'verschenka'


urlpatterns = [
#    path('grid', views.ItemListView.as_view()),
    path('index', views.ItemListView.as_view(), name='index'),
#    path('index', views.index),
]
