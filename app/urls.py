from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('pre-cadastro/', views.pre_cadastro, name='pre_cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('dados-iniciais/', views.dados_iniciais, name='dados_iniciais'),
    path('update-dados/', views.update_dados, name='update_dados'),
    path('anamnese/', views.anamnese, name='anamnese'),
    path('treino/', views.treino, name='treino'),
    path('treino-micro/<int:id>', views.treino_micro, name='treino_micro'),
    path('comecar/<int:id>', views.comecar, name='comecar'),
    path('delete_some/', views.delete_some, name='delete_some'),
    
]
