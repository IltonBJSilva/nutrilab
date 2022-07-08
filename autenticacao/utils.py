import re
from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def password_is_valid(request, password, confirm_password):

	#Valida o tamanho da senha
	if len(password) < 6:
		messages.add_message(request, constants.ERROR, 'Sua senha deve conter 6 ou mais caractertes')
		return False

	#Valida a senha com a confirmação se forem iguais
	if not password == confirm_password:
		messages.add_message(request, constants.ERROR, 'As senhas não coincidem!')
		return False

	#Valida pra ver se a senha contem letra maiúsculas
	#Usando expressões irregulares
	if not re.search('[A-Z]', password):
		messages.add_message(request, constants.ERROR, 'Sua senha não contem letras maiúsculas')
		return False

	#Valida pra ver se a senha contem letra minuscula
	if not re.search('[a-z]', password):
		messages.add_message(request, constants.ERROR, 'Sua senha não contem letras minúsculas')
		return False
	#Valida se contem numeros
	if not re.search('[1-9]', password):
		messages.add_message(request, constants.ERROR, 'Sua senha não contém números')
		return False

	return True


#Função para validação de email
def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:

	#Transformar o HTML em algo que o email consiga entender
	html_content = render_to_string(path_template, kwargs)
	#tirando as tags do html
	text_content = strip_tags(html_content)

	#Oque vai enviar
	email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)

	#Oque estou enviando
	email.attach_alternative(html_content, "text/html")
	#Enviando ao usuario
	email.send()
	return {'status': 1} #Validação para saber se deu certo
