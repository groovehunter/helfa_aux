from django.urls import path, re_path, include

from . import views

app_name = 'verschenka'


urlpatterns = [
#    path('grid', views.ItemListView.as_view()),
    path('index', views.ItemListView.as_view(), name='index'),
#    path('index', views.index),
    path('cats', views.CategoryListView.as_view() , name='category-list'),
    path('cat/<str:slug>/', views.ItemsByCategoryView.as_view() , name='items-by-category'),
    path('item/<str:slug>/', views.ItemDetailView.as_view(), name='item-detail'),
    #path('cat/<str:slug>/', views.ItemsByCategoryView.as_view() , name='category-detail'),
]
