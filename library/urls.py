from django.urls import  path
from . import views

urlpatterns = [
    path('', views.lib),
    path('<int:pk>/', views.book_detail),
]