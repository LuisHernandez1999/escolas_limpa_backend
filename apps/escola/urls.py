from django.urls import path
from . import views_escola

urlpatterns = [
    path('escolas/', views_escola.listar_escolas_view, name='listar_escolas'),
    path('escolas/criar/', views_escola.criar_escola_view, name='criar_escola'),
    path('escolas/<int:id>/atualizar/', views_escola.atualizar_escola_view, name='atualizar_escola'),
    path('escolas/<int:id>/deletar/', views_escola.deletar_escola_view, name='deletar_escola'),
]
