from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from .services_escolas.crud_escolas_service import criar_escola,listar_escolas,deletar_escola,atualizar_escola


@csrf_exempt
@require_http_methods(["GET"])
def listar_escolas_view(request):
    escolas = listar_escolas()
    return JsonResponse({
        'mensagem': f'{len(escolas)} escolas encontradas.',
        'escolas': escolas
    }, safe=False)



@csrf_exempt
@require_http_methods(["POST"])
def criar_escola_view(request):
    data = JSONParser().parse(request)
    escola, errors = criar_escola(data)
    if errors:
        return JsonResponse(errors, status=400)
    return JsonResponse({
        'mensagem': f"escola '{escola['nome_escola']}' criada com sucesso",
        'escola': escola
    }, status=201)



@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def atualizar_escola_view(request, id):
    data = JSONParser().parse(request)
    escola, errors = atualizar_escola(id, data)
    if errors:
        return JsonResponse(errors, status=400)

    response_data = {
        "mensagem": "escola atualizada com sucesso",
        "nome_escola": escola.get("nome_escola")  
    }

    return JsonResponse(response_data)

@csrf_exempt
@require_http_methods(["DELETE"])
def deletar_escola_view(request, id):
    escola, errors = deletar_escola(id)
    if errors:
        return JsonResponse(errors, status=404)
    
    response_data = {
        "mensagem": "Escola deletada com sucesso",
        "nome_escola": escola.get("nome_escola")  # escola é um dict aqui
    }
    return JsonResponse(response_data, status=200)