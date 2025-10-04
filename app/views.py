from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse

@login_required
def home(request):
    user = request.user.is_authenticated
    
    if user is None:
        return redirect('login_view')

    return render(request, 'inicio/home.html')       
       
    

def login_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuário inválido")
    
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('home'))
    
    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')

def register(request):
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
            )
        user.save()
        messages.success(request, "Conta criada!")
        return redirect('login_view')
    return render(request, 'login/register.html')
