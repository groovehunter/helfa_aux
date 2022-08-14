"""helfa_aux_dev URL Configuration

"""
from django.contrib import admin
from django.urls import path, include
from .views import index, page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('verschenka/', include('verschenka.urls')),
    path('users/', include('users.urls')),
    path('page/<name>', page),
]
