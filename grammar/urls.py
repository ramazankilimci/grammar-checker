from django.conf.urls import url
from django.urls import path
from django.urls.conf import include
from . import views

app_name='grammar'

urlpatterns = [
    path('', views.index, name='index'),
]
