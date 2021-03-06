from django.contrib.auth.models import User
from django.db import models

# Create your models here for data base table
# Criar e armazenar uma tabela no banco de dados
class Pacientes(models.Model):
	choices_sexo = (('F', 'Feminino'),
	                ('M', 'Maculino'))
	nome = models.CharField(max_length=50)
	sexo = models.CharField(max_length=1, choices=choices_sexo)
	idade = models.IntegerField()
	email = models.EmailField()
	telefone = models.CharField(max_length=19)
	#para diferenciar os pacientes de cada nutricionista
	nutri = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.nome

class DadosPaciente(models.Model):
	paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
	data = models.DateTimeField()
	peso = models.IntegerField()
	altura = models.IntegerField()
	percentual_gordura = models.IntegerField()
	percentual_musculo = models.IntegerField()
	colesterol_hdl = models.IntegerField()
	colesterol_ldl = models.IntegerField()
	colesterol_total = models.IntegerField()
	trigliceridios = models.IntegerField()
	def __str__(self):
		return f"Paciente({self.paciente.nome}, {self.peso})"


#Criar tabela refeicao para armazenar as refeições do paciente
class Refeicao(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    horario = models.TimeField()
    carboidratos = models.IntegerField()
    proteinas = models.IntegerField()
    gorduras = models.IntegerField()

    def __str__(self):
        return self.titulo

#Opção da refeição, por exemplo: 100g de banana para jantar ou almoço?
class Opcao(models.Model):
    refeicao = models.ForeignKey(Refeicao, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to="opcao")#Importante para funcionar arquivo
    descricao = models.TextField()

    def __str__(self):
        return self.descricao

