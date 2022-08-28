app_name = 'article'

from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url('view/', views.main),
    path('view-article/<int:id>/', views.view_article, name="view-article"),
]
