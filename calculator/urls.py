app_name = 'article'

from django.conf.urls import url
from . import views


urlpatterns = [
    url('', views.calculator_main)

]
