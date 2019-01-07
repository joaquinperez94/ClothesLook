from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from django.contrib.auth.models import User

# Create your views here.

#PAGINA DE INICIO
def inicio(request):
    return render(request,'inicio.html')

#PAGINA DE PRENDAS
def prendas(request):
    return render(request,'prendas.html')

#PAGINA DE LOOKS
def looks(request):
    return render(request,'looks.html')

#PAGINA DE PROFILE
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'profile.html', {"user": user})

#PAGINA DE REGISTRO
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('/inicio/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})