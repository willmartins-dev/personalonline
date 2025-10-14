from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_personal, name='login_personal'),
    path('register', views.register_personal, name='register_personal'), 
    path('register_cliente/<int:id>', views.register_cliente, name='register_cliente'), 
    path('logout', views.logout_personal, name='logout'), 
    path('inicio', views.inicio, name='inicio'),
    path('clientes', views.clientes, name='clientes'),
    path('cadastrar_senha/<int:id>', views.cadastrar_senha, name='cadastrar_senha'),
    path('treinamento/<int:id>', views.treinamento, name='treinamento'),
    path('microciclo/<int:id>', views.microciclo, name='microciclo'),
    path('add_exercicio/', views.add_exercicio, name='add_exercicio'),
    path('update_exercicios_cliente/<int:id>', views.update_exercicios_cliente, name='update_exercicios_cliente'),
    path('delete_exercicio_cliente/<int:id>', views.delete_exercicio_cliente, name='delete_exercicio_cliente'),
    path('buscar_exercicio/', views.buscar_exercicio, name='buscar_exercicio'),
    path('delete_mesociclo/<int:id>', views.delete_mesociclo, name='delete_mesociclo'),
    path('delete_microciclo/<int:id>', views.delete_microciclo, name='delete_microciclo'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('treinos/<int:id>', views.treinos, name='treinos'),
    path('exercicios/', views.exercicios, name='exercicios'),
    path('cadastro-exercicio/<int:id>', views.cadastro_exercicios, name='cadastro_exercicios'),
    path('delete_exercicio/<int:id>', views.delete_exercicio, name='delete_exercicio'),
    
]