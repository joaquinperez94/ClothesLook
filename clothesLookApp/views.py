from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User
from clothesLookApp.forms import registrerClote
from django.http.response import HttpResponseRedirect
from clothesLookApp.models import Clothing
from django.conf import settings

# Create your views here.

#PAGINA DE INICIO
def inicio(request):
    return render(request,'inicio.html')

#PAGINA DE PRENDAS
def prendas(request):    
    if request.method=='POST':
        form = registrerClote(request.POST)
        if form.is_valid():   
            form.save()         
        return redirect('/prendas/')
    else:
        form = registrerClote()
    
    return render(request, 'prendas.html',{'form':form})

def lista_prendas(request):
    prendas=Clothing.objects.all()
    return render(request,'listaPrendas.html', {'clothes':prendas,'MEDIA_URL': settings.MEDIA_URL})

def mostrar_prenda(request, id_prenda):
    prenda = get_object_or_404(Clothing, pk=id_prenda)
    return render(request,'mostrarPrenda.html',{'prenda':prenda,'MEDIA_URL': settings.MEDIA_URL})
    

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