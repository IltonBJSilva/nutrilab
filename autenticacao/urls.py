from django.contrib import admin
from django.urls import path, include #include serve para incluir alguma coisa
from . import views
#Definir as rotas de navegação
urlpatterns = [
    #acessando uma função em views chamada cadastro e nomeando ela
    path('cadastro/', views.cadastro, name="cadastro"),
    path('logar/', views.logar, name="logar"),

]


