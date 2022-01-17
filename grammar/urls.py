from django.conf.urls import url
from django.urls import path
from django.urls.conf import include
from . import views

app_name='grammar'

urlpatterns = [
    path('', views.index, name='index'),
    path('spellings', views.spellings, name='spellings'),
    path('mistakes', views.most_made_mistakes, name='mistakes'),
    path('profile', views.profile, name='profile'),
    path('spelling/delete/', views.spelling_delete, name='spelling_delete'),
    path('language', views.language, name='language'),
    path('apiusage', views.apiusage, name='apiusage'),
]
