from django.shortcuts import render

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

#PAGINA DE LOGIN
def login(request):
    return render(request,'login.html')