from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import CategoriaExercicios, Exercicios, Mesociclo, Microciclo, ExerciciosCliente
import json

@login_required
def inicio(request):
    if request.method == 'GET':
        usuarios = User.objects.all()
        context={
            'usuarios':usuarios
        }
        return render(request, 'home/home.html', context)
def clientes(request):
    if request.method == 'GET':
        users = User.objects.all()
        context={
            'users':users
        }
        return render(request, 'gerenciar/clientes.html', context)
def treinamento(request, id):
    
    user = {
        'is_superuser':request.user.is_superuser,
        'is_authenticated':request.user.is_authenticated,
        'username':request.user.username,
    }
    if request.method == 'GET':
        clientes = User.objects.get(id=id)
        mesociclo = Mesociclo.objects.filter(user_id = id)
        if request.method == 'GET':
            context={
                'clientes':clientes,
                'user':user,
                'mesociclo':mesociclo,
                }
        return render(request, 'gerenciar/meso.html', context)    
    elif request.method == 'POST':
            mesociclo = Mesociclo(
                user_id = id,
                titulo = request.POST.get('titulo'),
                periodizacao = request.POST.get('periodizacao'),
                duracao = request.POST.get('duracao'),
            )
            mesociclo.save()
           
            return redirect('treinamento',id=id)
    
def microciclo(request,id):

    mesociclo = Mesociclo.objects.get(id=id)
    microciclo = Microciclo.objects.filter(mesociclo_id=mesociclo.id)
    if request.method == 'GET':
        context={
            'mesociclo':mesociclo,
            'microciclo':microciclo,
        }
        return render(request, 'gerenciar/micro.html', context)
    
    elif request.method == 'POST':
        microciclo = Microciclo(
            mesociclo_id = id,
            titulo = request.POST.get('titulo')
        )
        microciclo.save()
        return redirect('microciclo', id=id)
    

    
@csrf_exempt
def add_exercicio(request):
    if request.method == 'POST':
        add_exercicio = ExerciciosCliente(
            microciclo_id = request.POST.get('id_micro'),
            exercicio = request.POST.get('exercicio'),
            url_img = request.POST.get('url'),
        )
        add_exercicio.save()
            
    return HttpResponse('add_exercicio')

def buscar_exercicio(request):
    buscar = request.GET.get('buscar')
    id_sessao = request.GET.get('buscar')

    exercicios = Exercicios.objects.filter(exercicio__icontains = buscar).values('categoria','exercicio', 'url')
    context={
        'exercicios':exercicios,
        'id_sessao':id_sessao
    }
    return render(request, 'gerenciar/ajax/buscar_exercicio.html', context)

def delete_mesociclo(request, id):
    mesociclo = Mesociclo.objects.get(id=id)
    request.session['id_user'] = mesociclo.user_id
    mesociclo.delete()
    
    return redirect('treinamento',id=request.session['id_user'])

def delete_microciclo(request, id):
    microciclo = Microciclo.objects.get(id=id)
    request.session['id_user'] = microciclo.mesociclo_id
    microciclo.delete()
    
    return redirect('microciclo',id=request.session['id_user'])

def treinos(request, id):
    return render(request, 'treinos/treinos.html')

def exercicios(request):
    if request.method == 'POST':
        categoria = CategoriaExercicios(
            titulo = request.POST.get('titulo'),
            tipo = request.POST.get('tipo'),
            url = request.POST.get('url'),
        )
        categoria.save()
        return redirect('exercicios')
    
    if request.method == 'GET':
        categoria = CategoriaExercicios.objects.filter(tipo = 'Musculação')
        context={
            'categoria':categoria
        }
        return render(request, 'treinos/exercicios.html', context)
    
def cadastro_exercicios(request, id):
    categoria = CategoriaExercicios.objects.get(id=id)
    exercicios = Exercicios.objects.filter(categoria = categoria)
    if request.method == 'GET':
        context={
            'categoria':categoria,
            'exercicios':exercicios,
        }
        return render(request, 'treinos/cadastro_exercicios.html', context)
    elif request.method == 'POST':
        exercicios = Exercicios(
            categoria_id = id,
            exercicio = request.POST.get('exercicio'),
            url = request.POST.get('url'),
        )
        exercicios.save()
        return redirect('cadastro_exercicios', id=id)
def delete_exercicio(request,id):
    categoria = CategoriaExercicios.objects.get(id=id)
    categoria.delete()

    return redirect('exercicios')

def delete_user(request,id):
    user = User.objects.get(id=id)
    user.delete()

    return redirect('clientes')

def login_personal(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        is_superuser = int(1)
        user = authenticate(request, username=username, password=password, is_superuser=is_superuser)
        if user is not None:
            login(request, user)
            return redirect(reverse('inicio'))
        else:
            messages.error(request, "Usuário inválido")
    
    return render(request, 'accounts/login.html')

def logout_personal(request):
    logout(request)
    return redirect('login_personal')

def register_personal(request):
    if request.method == 'POST':

        first_name = request.POST['first_name']
        email=request.POST['email']
        username=request.POST['email']
        password=request.POST['password']
        
        user = User.objects.create_user(
            username=username, 
            password=password,
            email=email,
            first_name =first_name,
            is_superuser = 1,
            )
        user.save()
        messages.success(request, "Conta criada!")
        
    
    return render(request, 'accounts/register.html')
