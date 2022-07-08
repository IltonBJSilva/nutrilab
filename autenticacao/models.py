from django.contrib.auth.models import User
from django.db import models

# Create your models here.

#Class para criar um campo no banco de dados para armazenar o token de ativação dos usuarios
class Ativacao(models.Model):
	token = models.CharField(max_length=64)
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	ativo = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username
