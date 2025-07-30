"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from apps.escola.views_escola import listar_escolas_view, criar_escola_view, atualizar_escola_view, deletar_escola_view
from apps.questionario.views_questionario import listar_totais_por_escola_view,criar_coleta_view,deletar_coleta_view,top_10_escolas_view,bottom_5_escolas_view,editar_coleta_view,ranking_escolas_pontos_view

urlpatterns = [
    path('api/escolas/', listar_escolas_view, name='listar_escolas'),
    path('api/escolas/criar/', criar_escola_view, name='criar_escola'),
    path('api/escolas/<int:id>/atualizar/', atualizar_escola_view, name='atualizar_escola'),
    path('api/escolas/<int:id>/deletar/', deletar_escola_view, name='deletar_escola'),
    path('api/form/lista_completa/',listar_totais_por_escola_view,name='listar_totais_por_escola'),
    path('api/form/criar_coleta/',criar_coleta_view,name='criar_coleta'),
    path('api/form/<int:id>/editar_coleta/',editar_coleta_view,name='editar_coleta'),
    path('api/form/<int:id>/deletar_coleta/',deletar_coleta_view,name='deletar'),
    path('api/form/top_10/',top_10_escolas_view,name='top_10'),
    path('api/form/bottom_5/',bottom_5_escolas_view,name='top_5_piores'),
    path('api/form/ranking/',ranking_escolas_pontos_view,name='ranking_escolas_pontos')
]

