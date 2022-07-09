from django.contrib import admin
from django.urls import path, include #include serve para incluir alguma coisa

#Definir as rotas de navegação
from . import views

urlpatterns = [
	path('pacientes/', views.pacientes, name="pacientes"),
	path('dados_paciente/', views.dados_paciente_listar, name="dados_paciente_listar"),
	path('dados_paciente/<str:id>/', views.dados_paciente, name="dados_paciente"),
	path('grafico_peso/<str:id>/', views.grafico_peso, name="grafico_peso"),


]