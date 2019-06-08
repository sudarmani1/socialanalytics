from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User

# Create your views here.
class LoginView(View):
	def get(self,request):
		return render(request,'login.html')

	def post(self,request):
		email 	 = request.POST.get('email')
		password = request.POST.get('password')
		username = User.objects.get(email=email).username
		user = authenticate(username=username, password=password)
		if user:
			login(request,user)
			return HttpResponseRedirect(reverse('index'))
		else:
			return render(request,'login.html')


class RegisterView(View):
	def get(self,request):
		return render(request,'register.html')


class LogoutView(View):
	def get(self,request):
	    logout(request)
	    return HttpResponseRedirect(reverse('login-view'))