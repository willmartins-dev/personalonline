from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from app_personal.models import Mesociclo, Microciclo, ExerciciosCliente
from django.contrib import messages
from django.urls import reverse
from .models import DadosIniciais
from .forms import AnamneseForm

def home(request):
    user_auth = request.user.is_authenticated
    user_id = request.user
    user_group = request.user.groups.all()
    
    if user_auth is None:
        return redirect('login_view')
    
    dados_iniciais_verificados = DadosIniciais.objects.filter(user_id = user_id)
    treino = Mesociclo.objects.filter(user_id=user_id)

    if not dados_iniciais_verificados:
        return redirect('dados_iniciais')
    else:    
        dados_iniciais = DadosIniciais.objects.get(user_id = user_id)
        context={
        'treino':treino,
        'grupo':user_group,
        'dados_iniciais':dados_iniciais,
        'calc_idade':dados_iniciais.Idade(),
        'calc_agua':dados_iniciais.calc_agua(),
        'tmb':dados_iniciais.calc_kcal()
    }
    return render(request, 'inicio/home.html', context)
  
def anamnese(request):

    if request.method == 'POST':
        form = AnamneseForm(request.POST)
        if form.is_valid:
            objeto_criado = form.save(commit=False)
            objeto_criado.user = request.user
            objeto_criado.save()
            return redirect('home')
    else:
        form = AnamneseForm()

    context={
        'form':form
    }
    return render(request, 'utilitarios/anamnese.html', {'form':form})         
       
def dados_iniciais(request):

    if request.method == 'GET':
            
        user_group = request.user.groups.all().first()
        personal = User.objects.get(username = user_group)
        context={
            'personal':personal.first_name,
        }
        return render(request, 'utilitarios/dados_iniciais.html', context)
    elif request.method == 'POST':
        update_dados = DadosIniciais(

            user_id = request.user,
            data_nascimento = request.POST.get('nascimento'),
            altura = request.POST.get('altura'),
            peso = request.POST.get('peso'),
            genero = request.POST.get('gender'),
        )
        update_dados.save()
        return redirect('home')
def update_dados(request):
    if request.method == 'GET':
        return render(request, 'configuracoes/update_dados.html')

def login_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if request.user.is_superuser == 0:
                login(request, user)
                return redirect('home')
            else:
                return redirect('login_view')
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
