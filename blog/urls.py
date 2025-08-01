# from single_pages.urls import urlpatterns

from django.urls import  path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:pk>/', views.detail),
    path('create/', views.create, name='blogcreate'), # name은 별명같은 것이다; url을 사용할 때, url이 변경되더라도 name을 사용하면 url을 찾을 수 있다.
    path('createfake/', views.createfake),
]