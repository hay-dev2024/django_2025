# from single_pages.urls import urlpatterns

from django.urls import  path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:pk>/', views.detail),
    path('create/', views.create, name='blogcreate'), # name은 별명같은 것이다
    path('createfake/', views.createfake),
]