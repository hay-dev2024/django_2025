# from single_pages.urls import urlpatterns

from django.urls import  path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:pk>/', views.detail),
    path('create/', views.create, name='blogcreate'), # name은 별명같은 것이다; url을 사용할 때, url이 변경되더라도 name을 사용하면 url을 찾을 수 있다.
    path('createfake/', views.createfake),
    path('category/<slug>/', views.category, name='category'),
    path('<int:pk>/delete/', views.delete, name='blogdelete'),
    path('<int:pk>/update/', views.update, name='blogupdate'),
    # Comment 관련 URL
    path('<post_pk>/', views.detail, name='viewcomments'),
    path('<int:pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:pk>/comment_update/', views.comment_update, name='comment_update'),
    path('<int:pk>/comment_delete/', views.comment_delete, name='comment_delete'),

]