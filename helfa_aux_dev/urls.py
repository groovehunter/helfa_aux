"""helfa_aux_dev URL Configuration

"""
from django.contrib import admin
from django.urls import path, include
from .views import index, page

app_name = 'helfa_aux_dev'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/', index, name='home'),
    path('', index, name='home'),
    path('page/<name>', page, name='page'),

    ### apps
    #path('verschenka/', include('verschenka.urls', namespace='verschenka')),
    path('verschenka/', include('verschenka.urls')),
    #path('/dj/verschenka/', include('verschenka.urls')), #, namespace='verschenka')),
    #path('/verschenka/', include('verschenka.urls')), #, namespace='verschenka')),

    path('users/', include('users.urls')),

]
