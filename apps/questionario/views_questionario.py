from django.http import JsonResponse, HttpResponseBadRequest,HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .service_questionario_escolar.escolar_questionario_service import criar_coleta,deletar_coleta,editar_coleta,listar_totais_por_escola_paginado,top_10_escolas_mais_pontos,bottom_5_escolas_menos_pontos
import json


@csrf_exempt  
def criar_coleta_view(request):
    if request.method != "POST":
        return HttpResponseBadRequest("metodo nao permitido, use POST.")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "json invalido."}, status=400)

    coleta, erro = criar_coleta(data)

    if erro:
        return JsonResponse({"error": erro}, status=400)
    resposta = {
        "id": coleta.id,
        "prefixo_caminhao": coleta.prefixo_caminhao,
        "data": coleta.data.isoformat(),
        "bairro": coleta.bairro,
        "motorista_nome": coleta.motorista_nome,
        "motorista_matricula": coleta.motorista_matricula,
        "coletor_nome": coleta.coletor_nome,
        "coletor_matricula": coleta.coletor_matricula,
        "escola_id": coleta.escola.id,
        "horario_chegada": coleta.horario_chegada.isoformat() if coleta.horario_chegada else None,
        "horario_saida": coleta.horario_saida.isoformat() if coleta.horario_saida else None,
        "bag_plastico": coleta.bag_plastico,
        "bag_papel": coleta.bag_papel,
        "bag_aluminio": coleta.bag_aluminio,
        "bag_eletronico": coleta.bag_eletronico,
        "bag_vazio": coleta.bag_vazio,
        "bag_semi_cheio": coleta.bag_semi_cheio,
        "bag_cheio": coleta.bag_cheio,
        "assinatura_responsavel": coleta.assinatura_responsavel,
        "telefone_responsavel": coleta.telefone_responsavel,
        "cpf_responsavel": coleta.cpf_responsavel,
        "escola":coleta.escola.nome_escola
    }
    return JsonResponse(resposta, status=201)


@csrf_exempt

def deletar_coleta_view(request, id):
    if request.method == "DELETE":
        sucesso, erro = deletar_coleta(id)
        if sucesso:
            return JsonResponse({"message": f"coleta {id} deletada com sucesso."})
        else:
            return JsonResponse({"error": erro}, status=400)
    else:
        return JsonResponse({"error": "metodo nao permitido."}, status=405)






@csrf_exempt
def editar_coleta_view(request, id):
    if request.method not in ["PUT", "PATCH"]:
        return HttpResponseNotAllowed(["PUT", "PATCH"])

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "json invalido."}, status=400)

    coleta, erro = editar_coleta(id, data)

    if erro:
        return JsonResponse({"error": erro}, status=404 if "nao encontrada" in erro else 400)

    return JsonResponse(coleta, status=200)



@csrf_exempt
def listar_totais_por_escola_view(request):

    try:
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 1777))
    except ValueError:
        return JsonResponse({"error": "parametros page e page_size devem ser inteiros."}, status=400)

    resultado = listar_totais_por_escola_paginado(page=page, page_size=page_size)

    return JsonResponse(resultado, status=200)




@csrf_exempt
def top_10_escolas_view(request):
    resultado = top_10_escolas_mais_pontos()
    return JsonResponse({"top_10_escolas": resultado}, status=200)


@csrf_exempt
def bottom_5_escolas_view(request):
    resultado = bottom_5_escolas_menos_pontos()
    return JsonResponse({"bottom_5_escolas": resultado}, status=200)
