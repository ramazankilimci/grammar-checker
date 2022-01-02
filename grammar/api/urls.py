from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'grammar'

# router = routers.DefaultRouter()
# router.register(r'spell', views.SpellViewSet)

urlpatterns = [
    path('spell_check/', views.spell_check),
    # path('', include(router.urls)),
]

