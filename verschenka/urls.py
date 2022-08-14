from django.urls import path, re_path, include

from . import views


urlpatterns = [
#    path('grid', views.ItemListView.as_view()),
    path('', views.ItemListView.as_view()),
#    path('index', views.index),
]
