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
    path('admin/', admin.site.urls),
    path('inicio/', views.inicio,name='inicio'),

    path('prendas/list', views.lista_prendas,name='prendas'),
    path('prendas/listUser', views.lista_prendas_usuario,name='prendasUsuario'),
    path('prendas/create', views.prendas_create,name='Crear prendas'),
    path('prendas/filtrarCategory', views.filtrar_category_prenda , name='Filtrar prendas por categoria'),
    re_path(r'mostrarPrenda/(?P<id_prenda>\d+)',views.mostrar_prenda),

    path('looks/list', views.lista_looks,name='looks'),
    path('looks/listUser', views.lista_looks_usuario,name='looksUsuario'),
    path('looks/create', views.looks_create,name='Crear Looks'),
    path('looks/filtrarSeason', views.filtrar_season_look, name='Filtrar looks por temporada'),
    re_path(r'mostrarLook/(?P<id_look>\d+)',views.mostrar_look),

    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
