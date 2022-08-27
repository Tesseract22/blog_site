app_name = 'calculator'

from django.conf.urls import url
from . import factorio_views


urlpatterns = [
    url('factorio/', factorio_views.factorio),
    url('update/', factorio_views.update),
    url('get_recipe/', factorio_views.get_recipe),
]
