from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_personal, name='login_personal'),
    path('register', views.register_personal, name='register_personal'), 
    path('logout', views.logout_personal, name='logout'), 
    path('inicio', views.inicio, name='inicio'),
]