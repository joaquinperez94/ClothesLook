from django.shortcuts import render,redirect
from .forms import UserCreateForm,UserChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from clothesLookApp.forms import createClothe, filtrarCategory, createLook
#from clothesLookApp.forms import  registrerLook
from django.http.response import HttpResponseRedirect
from clothesLookApp.models import Clothing, Look, User, Category
from django.conf import settings

# Create your views here.

#PAGINA DE INICIO
def inicio(request):
    return render(request,'inicio.html')

#PAGINA DE PRENDAS 
def prendas_create(request):     
    if request.user.is_authenticated:
        user = request.user   
        if request.method=='POST':
            form = createClothe(request.POST)
            if form.is_valid():   
                form.save()         
                return redirect('/prendas/listUser')
        else:
            form = createClothe()
            return render(request, 'prendas.html',{'form':form})
    
def lista_prendas(request):
    prendas=Clothing.objects.all()
    return render(request,'listaPrendas.html', {'clothes':prendas,'MEDIA_URL': settings.MEDIA_URL})

def lista_prendas_usuario(request):
    prendas=Clothing.objects.filter(user = request.user)
    return render(request,'listaPrendas.html', {'clothes':prendas,'MEDIA_URL': settings.MEDIA_URL})  

def mostrar_prenda(request, id_prenda):
    prenda = get_object_or_404(Clothing, pk=id_prenda)
    return render(request,'mostrarPrenda.html',{'prenda':prenda,'MEDIA_URL': settings.MEDIA_URL})
     
# def lista_filtrada(request, categoria):
#     prendas=Clothing.objects.filter(category = categoria)
#     return render(request,'mostrarPrenda.html',{'prenda':prenda,'MEDIA_URL': settings.MEDIA_URL})
# 


def filtrar_category_prenda(request):
    if request.method=='POST':
        categoriaSelect = request.POST['category']  
        #asnum = filtrar_category_prenda(categoriaSelect)
        prendas=Clothing.objects.filter(category  = categoriaSelect)       
        return render(request,'listaPrendas.html', {'clothes':prendas,'MEDIA_URL': settings.MEDIA_URL})
    else:
        categorias = Category.objects.all()
        return render(request,'filtrarCategoriaPrendas.html', {'categorias':categorias,'MEDIA_URL': settings.MEDIA_URL})

# 
# def filtrar_category_prenda(categoriaSelect):
#     prendas=Clothing.objects.all();
#     a = 0
#     for prenda in prendas:        
#         if(prenda.category == categoriaSelect):
#             break
#         else:
#             a += a
#         
#     return a       
#         
#         


#PAGINA DE LOOKS
def looks_create(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method=='POST':
            form = createLook(request.POST)
            if form.is_valid():
                clothes=form.cleaned_data.get('clothes')
                obj=form.save(commit=False)
                obj.user=user
                obj.save()
                for clothe in clothes:
                    obj.clothes.add(clothe.id)
                return redirect('/looks/listUser')
        else:
            form = createLook()
    return render(request, 'looks.html',{'form':form})

def lista_looks(request):
    looks=Look.objects.all()
    return render(request,'listaLooks.html', {'looks':looks,'MEDIA_URL': settings.MEDIA_URL})

def lista_looks_usuario(request):
    looks=Look.objects.filter(user = request.user)
    return render(request,'listaLooks.html', {'looks':looks,'MEDIA_URL': settings.MEDIA_URL})

def mostrar_look(request, id_look):
    look = get_object_or_404(Look, pk=id_look)
    return render(request,'mostrarLook.html',{'look':look,'MEDIA_URL': settings.MEDIA_URL})

def filtrar_season_look(request):
    if request.method=='POST':
        seasonSelect = request.POST['season']
        looks=Look.objects.filter(season  = seasonSelect)
        return render(request,'listaLooks.html', {'looks':looks,'MEDIA_URL': settings.MEDIA_URL})
    else:
        return render(request,'filtrarSeasonLooks.html', {'MEDIA_URL': settings.MEDIA_URL})




#PAGINA DE PROFILE
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'profile.html', {"user": user})

def delete_user(request, id_user):
    User = get_user_model()
    user = User.objects.get(id=id_user)
    if request.method == "POST":
        user.delete()
        return render(request, 'inicio.html')
    context = {
        "User": user
    }
    return render(request, "user_delete.html", context)

def edit_user(request,id_user):
    User = get_user_model()
    user=User.objects.get(id=id_user)
    if request.method == 'GET':
        form=UserChangeForm(instance=user)
    else:
        form=UserChangeForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
        return render(request, 'profile.html', {"user": user})
    return render(request, 'edit_user.html', {'form': form})


#PAGINA DE REGISTRO
def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #auth_login(request, user)
            return redirect('/inicio/')
    else:
        form = UserCreateForm()
    return render(request, 'signup.html', {'form': form})