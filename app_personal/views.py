from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse

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
            is_superuser = 1
            )
        user.save()
        messages.success(request, "Conta criada!")
        return redirect('login_personal')
    
    return render(request, 'accounts/register.html')
