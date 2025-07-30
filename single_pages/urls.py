#from sesac_django_project.urls import urlpatterns

from django.urls import path
from . import views # 현재 디렉토리에 있는 것을 import 할 때는 . 을 사용한다.
from .views import landing

urlpatterns = [
    # http://127.0.0.1:8000/ -> landing.html 로 보내라
    path('', views.landing, name='landing'),
]