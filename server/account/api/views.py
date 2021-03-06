from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import HttpRequest

from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import api_view, permission_classes

#need to regex the username, email, and password
#probably should not return the error as it could give attacker info
@api_view(['GET', 'POST', ])
@permission_classes([])
def registration_view(request):
	if request.method == 'GET':
		return render(request, 'register/index.html')

	if request.method == 'POST':
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			#data = serializer.errors
			data['response'] = 'invalid login'
		return Response(data)

#need to regex the username and password
@api_view(['GET', 'POST'])
@permission_classes([])
def login_view(request):
	if request.method == 'GET':
		return render(request, 'login/index.html')

	elif request.method == 'POST':
		return obtain_auth_token(request._request)
