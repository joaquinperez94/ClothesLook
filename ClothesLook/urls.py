"""ClothesLook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from clothesLookApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.inicio,name='inicio'),
    path('admin/', admin.site.urls),
    path('inicio/', views.inicio,name='inicio'),

    path('clothing/list', views.clothes_list,name='clothing'),
    path('clothing/listUser', views.clothes_list_user,name='clothingUser'),
    path('clothing/create', views.clothing_create,name='Create clothing'),
    path('clothing/filterCategory', views.filter_category_clothing , name='Filter clothing per category'),
    re_path(r'display/(?P<id_clothing>\d+)',views.display_clothing),
    re_path(r'delete/(?P<id_clothing>\d+)',views.delete_clothing),

    path('looks/list', views.lista_looks,name='looks'),
    path('looks/listUser', views.lista_looks_usuario,name='looksUsuario'),
    path('looks/create', views.looks_create,name='Crear Looks'),
    path('looks/filtrarSeason', views.filtrar_season_look, name='Filtrar looks por temporada'),
    re_path(r'mostrarLook/(?P<id_look>\d+)',views.mostrar_look),

    re_path(r'edit_user/(?P<id_user>\d+)',views.edit_user),
    re_path(r'delete_user/(?P<id_user>\d+)',views.delete_user),
    path('looks/', views.inicio),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
