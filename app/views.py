from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from app_personal.models import Mesociclo, Microciclo, ExerciciosCliente
from django.contrib import messages
from django.urls import reverse
from .models import DadosIniciais, preCadastro, Medidas
from .forms import AnamneseForm
from django.views.decorators.csrf import csrf_exempt
import re

def index(request):
    return render(request, 'publico/index.html')
def delete_dadosiniciais(request, id):
    dados = DadosIniciais.objects.get(id=id)
    dados.delete()
def home(request):
    user_auth = request.user.is_authenticated
    user_id = request.user.id
    user_group = request.user.groups.all()
    
    if not user_auth:
        return redirect('login_view')
    else:
        dados_iniciais_verificados = DadosIniciais.objects.filter(user_id = user_id)
        treino = Mesociclo.objects.filter(user_id=user_id).order_by('-id')[:1]
        medidas = Medidas.objects.filter(user_id=user_id)

        if not medidas:
            medidas = None
        

        if not dados_iniciais_verificados:
            return redirect('dados_iniciais')
        else:    
            
            dados_iniciais = DadosIniciais.objects.get(user_id = user_id)
            gorduras = Medidas.objects.filter(user_id=user_id).order_by('-id')
            dados_gordura=[]
            if gorduras:
                

                for g in gorduras:
                    dados_gordura.append({
                        'gordura': g.calcular_percentual_gordura(dados_iniciais.genero, dados_iniciais.altura),
                        'peso':g.peso
                    })
            else:
                dados_gordura=[{'gordura':0, 'peso':0}]

            context={
            'treino':treino,
            'grupo':user_group,
            'dados_iniciais':dados_iniciais,
            'calc_idade':dados_iniciais.Idade(),
            'calc_agua':dados_iniciais.calc_agua(),
            'tmb':dados_iniciais.calc_kcal(),
            'medidas':medidas,
            'gordura':dados_gordura[0]['gordura'],
            'peso':dados_gordura[0]['peso'],
            }
            
                
                
        
        return render(request, 'inicio/home.html', context)
    
@csrf_exempt
def comparar_medidas_aluno(request):
    user_id = request.user.id
    data_antiga = request.GET.get('data1')
    data_atual = request.GET.get('data2')

     #calculo gordura
    dados_iniciais = DadosIniciais.objects.get(user_id = user_id)
    gorduras1 = Medidas.objects.get(user_id=user_id, id=data_antiga)
    gorduras2 = Medidas.objects.get(user_id=user_id, id=data_atual)    

    g1 = gorduras1.calcular_percentual_gordura(dados_iniciais.genero, dados_iniciais.altura)
    g2 = gorduras2.calcular_percentual_gordura(dados_iniciais.genero, dados_iniciais.altura)

    if data_antiga and data_atual:
        # Buscamos os registros específicos
        medida_recente = Medidas.objects.get(id=data_antiga)
        medida_antiga = Medidas.objects.get(id=data_atual)

        campos = ['peso','torax', 'cintura', 'quadril', 'coxa_direita', 'coxa_esquerda', 'braco_direito', 'braco_esquerdo']
        comparativo = []
       
        for campo in campos:
            v_recente = getattr(medida_recente, campo)
            v_antigo = getattr(medida_antiga, campo)
            diff = v_recente - v_antigo

            comparativo.append({
                'label': campo.capitalize(),
                'v_antigo': v_antigo,
                'v_recente': v_recente,
                'diff': round(diff, 2),
                'status': 'Aumentou' if diff > 0 else 'Diminuiu' if diff < 0 else 'Manteve'
            })
        
        context={
            'comparativo': comparativo,
            'medida_recente': medida_recente,
            'medida_antiga': medida_antiga,
            'gordura1':g1,
            'gordura2':g2,
            'data1':gorduras1,
            'data2':gorduras2,
            
        }
 
    return render(request, 'inicio/ajax/comparar_medidas.html', context)
    
def update_peso(request,id):
    update_dados = DadosIniciais.objects.get(id=id)
    peso = request.POST.get('peso')
        
    update_dados.peso = peso.replace(',', '.')
        
    update_dados.save()
    
    return redirect('home')

def treino_micro(request, id):

    user_auth = request.user.is_authenticated

    if not user_auth:
        return redirect('login_view')

    Micro = Microciclo.objects.filter(mesociclo_id = id)
    exercicios = ExerciciosCliente.objects.filter(microciclo_id = id)

    context={
        'micro':Micro,
        'exercicios':exercicios
    }

    return render(request,'treino/treino-micro.html', context)

def treino(request):

    user_auth = request.user.is_authenticated

    if not user_auth:
        return redirect('login_view')

    Meso = Mesociclo.objects.filter(user_id=request.user)
    
    context={
        'meso':Meso
    }

    return render(request,'treino/treino.html', context)
def comecar(request, id):

    if request.method == 'GET':
        treino = ExerciciosCliente.objects.filter(microciclo_id=id)
        microciclo = Microciclo.objects.get(id=id)

        context = {
            'treino':treino,
            'micro':microciclo
        }

    return render(request, 'treino/comecar.html',context)

def medidas(request, id):

    if request.method == 'POST':
        
        peso_antigo = request.POST.get('peso')
        medidas = Medidas(
        user = request.user,
        mesociclo_id = id,
        peso = peso_antigo.replace(',', '.'),
        pescoco = request.POST.get('pescoco'),
        torax = request.POST.get('torax'),
        cintura = request.POST.get('cintura'),
        quadril = request.POST.get('quadril'),
        braco_direito = request.POST.get('b-d'),
        braco_esquerdo = request.POST.get('b-e'),
        coxa_direita = request.POST.get('c-d'),
        coxa_esquerda = request.POST.get('c-e'),
        )
        medidas.save()
        return redirect('medidas', id)
    else:        
        dados_medidas = Medidas.objects.filter(mesociclo_id = id)
        context = {
            'id_meso':id,
            'dados':dados_medidas
        }
        return render(request, 'inicio/medidas.html', context)
def delete_medidas(request, id):
    medidas = Medidas.objects.get(id=id)
    medidas.delete()
    #return HttpResponse(id)
    return redirect('medidas', id)

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

    user_auth = request.user.is_authenticated
    if not user_auth:
        return redirect('login_view')

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
            celular = re.sub(r'\D', '',request.POST.get('celular')),
        )
        update_dados.save()
        return redirect('home')
    
def delete_some(request):
    dados = DadosIniciais.objects.get(id=5)
    dados.delete()

def update_dados(request):
    dados = DadosIniciais.objects.get(user_id=request.user)
    if request.method == 'GET':

        context={
            'dados':dados
        }

        return render(request, 'configuracoes/update_dados.html', context)
    
    elif request.method == 'POST':

        peso_antigo = request.POST.get('peso')
        peso = peso_antigo.replace(',', '.')

        dados.genero = request.POST.get('genero')
        dados.data_nascimento = request.POST.get('nascimento')
        dados.celular = request.POST.get('celular')
        dados.peso = peso
        dados.altura = request.POST.get('altura')
        dados.save()

        return redirect('update_dados')


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

def pre_cadastro(request):
    if request.method == 'POST':
        
        pre_cadastro = preCadastro(
            personal = request.POST['personal'],
            nome = request.POST['nome'],
            email=request.POST['email'],
            celular=request.POST['celular'],
            genero=request.POST['genero'],
            data_nascimento=request.POST['nascimento'],
            peso=request.POST['peso'],
            altura=request.POST['altura'],
            objetivo=request.POST['objetivo'],
            frequencia=request.POST['frequencia'],
            nivel=request.POST['nivel'],
        )
        pre_cadastro.save()
        messages.success(request, "Conta criada!")
        return redirect('register_success')
    return render(request, 'login/register.html')

def register_success(request):
    return render(request, 'login/register-success.html')
