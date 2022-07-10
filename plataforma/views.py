from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants

#Função que serve para validar se esta logado
from django.views.decorators.csrf import csrf_exempt

from plataforma.models import Pacientes, DadosPaciente, Refeicao, Opcao


@login_required(login_url='/auth/logar/')
def pacientes(request):
	if request.method == "GET":
		pacientes = Pacientes.objects.filter(nutri=request.user) #Trazer os pacientes da nutricionista logado
		return render(request, 'pacientes.html', {'pacientes': pacientes})

	elif request.method == "POST":
		#Vindo do HTML
		nome = request.POST.get('nome')
		sexo = request.POST.get('sexo')
		idade = request.POST.get('idade')
		email = request.POST.get('email')
		telefone = request.POST.get('telefone')


		#tirar todos os espaços em brancos
		if (len(nome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0):
			messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
			return redirect('/pacientes/')

		if not idade.isnumeric():
			messages.add_message(request, constants.ERROR, 'Digite uma idade válida')
			return redirect('/pacientes/')

		pacientes = Pacientes.objects.filter(email=email)

		if pacientes.exists():
			messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse E-mail')
			return redirect('/pacientes/')

		try:
			paciente = Pacientes(nome=nome,
			                     sexo=sexo,
			                     idade=idade,
			                     email=email,
			                     telefone=telefone,
			                     nutri=request.user) # ultimo para  trazer o usuario logado
			paciente.save()
			messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso')
			return redirect('/pacientes/')

		except:
			messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
			return redirect('/pacientes/')

	return render(request, 'pacientes.html')

#Listar o dados dos pacientes ao abrir ele
@login_required(login_url='/auth/logar/')
def dados_paciente_listar(request):
	if request.method == "GET":
		pacientes = Pacientes.objects.filter(nutri=request.user)
		return render(request, 'dados_paciente_listar.html', {'pacientes': pacientes})

	return render(request,'dados_paciente_listar.html')

#Essa função serve para acessar pelo ID do paciente
@login_required(login_url='/auth/logar/')
def dados_paciente(request, id):
	#busca um paciente no banco de dados, caso não ache, retorna ERRO 404
	paciente = get_object_or_404(Pacientes, id=id)
	#Evitar acessar pacientes de outro nutricionista
	if not paciente.nutri == request.user:
		messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
		return redirect('/dados_paciente/')
	#Renderizar os dados
	if request.method == "GET":
		dados_paciente = DadosPaciente.objects.filter(paciente=paciente)

		return render(request, 'dados_paciente.html', {'paciente': paciente,'dados_paciente':dados_paciente})
	elif request.method == "POST":
		peso = request.POST.get('peso')
		altura = request.POST.get('altura')
		gordura = request.POST.get('gordura')
		musculo = request.POST.get('musculo')
		hdl = request.POST.get('hdl')
		ldl = request.POST.get('ldl')
		colesterol_total = request.POST.get('ctotal')
		triglicerídios = request.POST.get('triglicerídios')

		paciente = DadosPaciente(paciente=paciente,
		                         data=datetime.now(),
		                         peso=peso,
		                         altura=altura,
		                         percentual_gordura=gordura,
		                         percentual_musculo=musculo,
		                         colesterol_hdl=hdl,
		                         colesterol_ldl=ldl,

		colesterol_total = colesterol_total,
		                   trigliceridios = triglicerídios)
		paciente.save()
		messages.add_message(request, constants.SUCCESS, 'Dados cadastrado com sucesso')

		return redirect('/dados_paciente/')


#Função que mostra um grafico do peso e a evolução, criando uma API
@login_required(login_url='/auth/logar/')
@csrf_exempt
def grafico_peso(request, id): #recebe o ID do paciente
	paciente = Pacientes.objects.get(id=id)
	dados = DadosPaciente.objects.filter(paciente=paciente).order_by("data") #buscando todos os dados do paciente ordedando pela data
	pesos = [dado.peso for dado in dados]
	labels = list(range(len(pesos))) #Mostrando todas as vezes que coletou
	data = {'peso': pesos,
	'labels': labels}
	return JsonResponse(data) #Json e usado toda vez que cria uma API

#Listar o plano alimentar do paciente
def plano_alimentar_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'plano_alimentar_listar.html', {'pacientes': pacientes})

def plano_alimentar(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/plano_alimentar_listar/')

    if request.method == "GET":
	    r1 = Refeicao.objects.filter(paciente=paciente).order_by('horario')
	    opcao = Opcao.objects.all()
	    return render(request, 'plano_alimentar.html', {'paciente': paciente, 'refeicao': r1, 'opcao': opcao})


def refeicao(request, id_paciente):
    paciente = get_object_or_404(Pacientes, id=id_paciente) #Verificar o paciente
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

    if request.method == "POST":
        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        carboidratos = request.POST.get('carboidratos')
        proteinas = request.POST.get('proteinas')
        gorduras = request.POST.get('gorduras')
		#Salvar as informações da refeição
        r1 = Refeicao(paciente=paciente,
                      titulo=titulo,
                      horario=horario,
                      carboidratos=carboidratos,
                      proteinas=proteinas,
                      gorduras=gorduras)
		#Salvando no banco de dados
        r1.save()

        messages.add_message(request, constants.SUCCESS, 'Refeição cadastrada')
        return redirect(f'/plano_alimentar/{id_paciente}')

def opcao(request, id_paciente):
    if request.method == "POST":
        id_refeicao = request.POST.get('refeicao')
        imagem = request.FILES.get('imagem') #Inves de POST vira FILE por causa que recebe um arquivo
        descricao = request.POST.get("descricao")

        o1 = Opcao(refeicao_id=id_refeicao,
                   imagem=imagem,
                   descricao=descricao)

        o1.save()

        messages.add_message(request, constants.SUCCESS, 'Opção cadastrada')
        return redirect(f'/plano_alimentar/{id_paciente}')







