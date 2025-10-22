from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('dados-iniciais/', views.dados_iniciais, name='dados_iniciais'),
    path('update-dados/', views.update_dados, name='update_dados'),
    path('anamnese/', views.anamnese, name='anamnese'),
    path('treino/', views.treino, name='treino'),
    path('delete_some/', views.delete_some, name='delete_some'),
    
]
