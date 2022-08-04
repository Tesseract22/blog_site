app_name = 'calculator'

from django.conf.urls import url
from . import views


urlpatterns = [
    url('main/', views.calculator_main),
    url('update/', views.update),
]
