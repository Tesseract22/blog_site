app_name = 'calculator'

from django.conf.urls import url
from . import factorio_views
# from . import satisfactory_views

urlpatterns = [
    url('factorio/main', factorio_views.main, name="factorio_main"),
    # url('satisfactory/main', satisfactory_views.main),
    url('factorio/update/', factorio_views.update),
    # url('satisfactory/update/', satisfactory_views.update),
    url('factorio/get_recipe/', factorio_views.get_recipe),
    # url('satisfactory/get_recipe/', satisfactory_views.get_recipe),
]
