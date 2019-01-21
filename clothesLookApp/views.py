from django.shortcuts import render,redirect
from .forms import UserCreateForm,UserChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from clothesLookApp.forms import ClothingForm, createLook, CommentForm
#from clothesLookApp.forms import  registrerLook
from django.http.response import HttpResponseRedirect
from clothesLookApp.models import Clothing, Look, User, Category, Comment
from django.conf import settings
from django.core.paginator import Paginator

# Create your views here.

#PAGINA DE INICIO
def inicio(request):
    return render(request,'inicio.html')

#PAGINA DE PRENDAS 
def clothing_create(request):     
    if request.user.is_authenticated:
        user = request.user   
        if request.method=='POST':
            form = ClothingForm(request.POST)
            if form.is_valid():   
                obj = form.save(commit=False)
                obj.user = user  
                obj.save()         
                return redirect('/clothing/listUser')
        else:
            form = ClothingForm()
    return render(request, 'clothing_create.html',{'form':form})
    
def clothes_list(request):
    clothes=Clothing.objects.all()

    paginator= Paginator(clothes,5)
    page=request.GET.get('page')
    # ?page=2
    clothes=paginator.get_page(page)

    return render(request,'clothes_list.html', {'clothes':clothes,'page':page,'MEDIA_URL': settings.MEDIA_URL})

def clothes_list_user(request):
    clothes = Clothing.objects.filter(user = request.user)
    paginator = Paginator(clothes, 5)
    page = request.GET.get('page')
    # ?page=2
    clothes = paginator.get_page(page)

    return render(request,'clothes_list.html', {'clothes':clothes,'page':page,'MEDIA_URL': settings.MEDIA_URL})

def display_clothing(request, id_clothing):
    clothing = get_object_or_404(Clothing, pk=id_clothing)
    return render(request,'display_clothing.html',{'clothing':clothing,'MEDIA_URL': settings.MEDIA_URL})
     
def filter_category_clothing(request):
    if request.method=='POST':
        categorySelect = request.POST['category']  
        clothes=Clothing.objects.filter(category  = categorySelect)       
        return render(request,'clothes_list.html', {'clothes':clothes,'MEDIA_URL': settings.MEDIA_URL})
    else:
        categories = Category.objects.all()
        return render(request,'filter_category_clothing.html', {'categories':categories,'MEDIA_URL': settings.MEDIA_URL})

def delete_clothing(request, id_clothing):
    clothing = Clothing.objects.get(id=id_clothing)
    if request.method == "POST":
        clothing.delete()
        return redirect('../../../clothing/list')
    return render(request,'delete_clothing.html', {'clothing':clothing})

def edit_clothing(request,id_clothing):
    clothing = Clothing.objects.get(id=id_clothing)
    if request.method == 'GET':
        form=ClothingForm(instance=clothing)
    else:
        form=ClothingForm(request.POST,instance=clothing)
        if form.is_valid():
            form.save()
        return redirect('../../../clothing/list')
    return render(request, 'clothing_create.html', {'form': form})

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
    paginator= Paginator(looks,5)
    page=request.GET.get('page')
    looks=paginator.get_page(page)

    return render(request,'listaLooks.html', {'looks':looks,'page':page,'MEDIA_URL': settings.MEDIA_URL})

def lista_looks_usuario(request):
    looks=Look.objects.filter(user = request.user)
    paginator= Paginator(looks,5)
    page=request.GET.get('page')
    # ?page=2
    looks=paginator.get_page(page)
    return render(request,'listaLooks.html', {'looks':looks,'page':page,'MEDIA_URL': settings.MEDIA_URL})

def mostrar_look(request, id_look):
    look1 = get_object_or_404(Look, pk=id_look)
    comments = Comment.objects.filter(look = look1)
    return render(request,'mostrarLook.html',{'look':look1,'comments':comments,'MEDIA_URL': settings.MEDIA_URL})

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


#PAGINA DE COMENTARIOS 
def comment_create(request,id_look):     
    if request.user.is_authenticated:
        user = request.user   
        if request.method=='POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = user
                look = Look.objects.get(id=id_look)  
                obj.look = look 
                obj.save()         
                return redirect('../../../looks/list')
        else:
            form = CommentForm()
    return render(request, 'comment_create.html',{'form':form})