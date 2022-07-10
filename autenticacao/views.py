
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .utils import password_is_valid, email_html
from django.shortcuts import redirect
from django.contrib.messages import constants
from django.contrib import messages, auth
import os
from django.conf import settings
from .models import Ativacao
#Biblioteca para fazer um hash
from hashlib import sha256

# Create your views here.


def cadastro(request):
    #Se a requisição que o usuario fez
    if request.method == "GET":
        #Verificar se o usuario ja esta autenticado
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'cadastro.html')

    elif request.method == "POST":
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')

        #Se algum requisito não for valido, vai retornar para pagina
        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('/auth/cadastro')

        try:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=senha,
                                            is_active=False)
            user.save()

            #Criação do Token
            #convertendo username and email for binary and hexdecimal
            token = sha256(f"{username}{email}".encode()).hexdigest()
            ativacao = Ativacao(token=token, user=user)
            #Salvando a ativação no banco de dados
            ativacao.save()

            #Enviar email
            path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/emails/cadastro_confirmado.html')
            email_html(path_template, 'Cadastro confirmado', [email,], username=username, link_ativacao=f"127.0.0.1:8000/auth/ativar_conta/{token}")

            messages.add_message(request, constants.SUCCESS,'Usuario cadastrado com sucesso')

            return redirect('/auth/logar')
        except: 
            messages.add_message(request, constants.ERROR, 'Erro interno no sistema')
            return redirect('/auth/cadastro')


def logar(request):
    if request.method == "GET":
        # Verificar se o usuario ja esta autenticado
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'logar.html') #retornando para logar
    if request.method == "POST": #se ela venho de um form
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')

        #Função que vai retornar true or false baseado se existe ou não no banco de dados
        usuario = auth.authenticate(username=username, password=senha)
    if not usuario:
        #Se o usuario não conseguiu fazer o login
        #Redirecionar o mesmo para logar
        messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
        return redirect('/auth/logar')
    else:
        #Se existe, autenticar
        auth.login(request, usuario)
        return redirect('/pacientes')

#Função para deslogar
def sair(request):
    auth.logout(request)
    messages.add_message(request, constants.WARNING, 'Deslogado')
    return redirect('/auth/logar')

def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)
    #verifica se ja esta ativo
    if token.ativo:
        messages.add_message(request, constants.WARNING, 'Essa token já foi usado')
        return redirect('/auth/logar')
    #Pega no banco de dados pelo usuario
    user = User.objects.get(username=token.user.username)
    #Usuario fica ativo
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso')
    return redirect('/auth/logar')

