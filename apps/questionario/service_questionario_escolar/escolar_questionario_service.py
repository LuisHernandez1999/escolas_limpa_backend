from ..models import Questionario_coleta_escolar
from apps.escola.models import Escola
from django.db.models import Sum
from django.db.models import F, IntegerField, ExpressionWrapper,Max
from datetime import datetime
from django.db import transaction


@transaction.atomic
def criar_coleta(data):
    nome_escola = data.get("escola")
    if not nome_escola:
        return None, "campo 'escola' obrigatório."

    try:
        escola = Escola.objects.only("id").get(nome_escola=nome_escola)
    except Escola.DoesNotExist:
        return None, f"escola com nome '{nome_escola}' nao encontrada."

    data_str = data.get("data")
    if isinstance(data_str, str):
        try:
            data_convertida = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            return None, f"data '{data_str}' invalida, use o formato YYYY-MM-DD"
    else:
        data_convertida = data_str

    def parse_time(horario):
        if isinstance(horario, str):
            try:
                return datetime.strptime(horario, "%H:%M").time()
            except ValueError:
                return None
        return horario

    horario_chegada = parse_time(data.get("horario_chegada"))
    horario_saida = parse_time(data.get("horario_saida"))

    try:
        int_fields = [
            "bag_plastico", "bag_papel", "bag_aluminio", "bag_eletronico",
            "bag_vazio", "bag_semi_cheio", "bag_cheio"
        ]
        for f in int_fields:
            data[f] = int(data.get(f, 0) or 0)

        coleta = Questionario_coleta_escolar.objects.create(
            prefixo_caminhao=data.get("prefixo_caminhao"),
            data=data_convertida,
            bairro=data.get("bairro"),
            motorista_nome=data.get("motorista_nome"),
            motorista_matricula=data.get("motorista_matricula"),
            coletor_nome=data.get("coletor_nome"),
            coletor_matricula=data.get("coletor_matricula"),
            escola=escola,
            horario_chegada=horario_chegada,
            horario_saida=horario_saida,
            bag_plastico=data["bag_plastico"],
            bag_papel=data["bag_papel"],
            bag_aluminio=data["bag_aluminio"],
            bag_eletronico=data["bag_eletronico"],
            bag_vazio=data["bag_vazio"],
            bag_semi_cheio=data["bag_semi_cheio"],
            bag_cheio=data["bag_cheio"],
            assinatura_responsavel=data.get("assinatura_responsavel"),
            telefone_responsavel=data.get("telefone_responsavel"),
            cpf_responsavel=data.get("cpf_responsavel"),
        )
        return coleta, None

    except Exception as e:
        return None, f"erro ao criar coleta: {e}"
    

def deletar_coleta(coleta_id):
    try:
        deleted, _ = Questionario_coleta_escolar.objects.filter(pk=coleta_id).delete()
        if deleted == 0:
            return False, f"coleta com ID {coleta_id} nao encontrada."
        return True, None
    except Exception as e:
        return False, f"erro ao deletar coleta: {e}"
    

def editar_coleta(id, data):
    try:

        data.pop("id", None)

        int_fields = [
            "bag_plastico", "bag_papel", "bag_aluminio", "bag_eletronico",
            "bag_vazio", "bag_semi_cheio", "bag_cheio"
        ]
        for f in int_fields:
            if f in data:
                data[f] = int(data[f] or 0)

        if "escola" in data:
            nome_escola = data.pop("escola")
            try:
                escola = Escola.objects.get(nome_escola=nome_escola)
                data["escola_id"] = escola.id
            except Escola.DoesNotExist:
                return None, f"escola com nome '{nome_escola}' nao encontrada."

        updated = Questionario_coleta_escolar.objects.filter(id=id)
        if not updated.exists():
            return None, f"coleta com ID {id} nao encontrada."

        updated.update(**data)
        coleta = updated.select_related("escola").values(
            "id", "prefixo_caminhao", "data", "bairro",
            "motorista_nome", "motorista_matricula",
            "coletor_nome", "coletor_matricula",
            "escola__id", "escola__nome_escola",
            "horario_chegada", "horario_saida",
            "bag_plastico", "bag_papel", "bag_aluminio", "bag_eletronico",
            "bag_vazio", "bag_semi_cheio", "bag_cheio",
            "assinatura_responsavel", "telefone_responsavel", "cpf_responsavel"
        ).first()

        if coleta:
            coleta["escola"] = {
                "id": coleta.pop("escola__id"),
                "nome": coleta.pop("escola__nome_escola"),
            }
            pontos = (
                coleta["bag_plastico"] + coleta["bag_papel"] +
                coleta["bag_aluminio"] + coleta["bag_eletronico"] +
                coleta["bag_vazio"] + coleta["bag_semi_cheio"] + coleta["bag_cheio"]
            )
            coleta["pontos"] = pontos
        return coleta, None

    except Exception as e:
        return None, f"erro ao editar coleta: {e}"

    

def listar_totais_por_escola_paginado(page=1, page_size=1777):
    offset = (page - 1) * page_size
    limit = offset + page_size

  
    pontos_expr = (
        F("bag_plastico") + F("bag_papel") + F("bag_aluminio") +
        F("bag_eletronico") + F("bag_vazio") + F("bag_semi_cheio") + F("bag_cheio")
    )

    qs = (
        Questionario_coleta_escolar.objects
        .annotate(pontos=ExpressionWrapper(pontos_expr, output_field=IntegerField()))
        .values("escola__nome_escola")
        .annotate(
            bag_plastico_total=Sum("bag_plastico"),
            bag_papel_total=Sum("bag_papel"),
            bag_aluminio_total=Sum("bag_aluminio"),
            bag_eletronico_total=Sum("bag_eletronico"),
            bag_vazio_total=Sum("bag_vazio"),
            bag_semi_cheio_total=Sum("bag_semi_cheio"),
            bag_cheio_total=Sum("bag_cheio"),
            pontos_total=Sum("pontos"),
            data_mais_recente=Max("data"),  
        )
        .order_by("-data_mais_recente")  #
    )

    total_escolas = len(qs)
    escolas_page = list(qs[offset:limit])

    return {
        "total_escolas": total_escolas,
        "page": page,
        "page_size": page_size,
        "results": escolas_page,
    }



def top_10_escolas_mais_pontos():
    pontos_expr = (
        F('bag_plastico') + F('bag_papel') + F('bag_aluminio') + F('bag_eletronico') +
        F('bag_vazio') + F('bag_semi_cheio') + F('bag_cheio')
    )
    pontos_expr = ExpressionWrapper(pontos_expr, output_field=IntegerField())

    qs = (
        Questionario_coleta_escolar.objects
        .select_related('escola')
        .annotate(pontos=pontos_expr)
        .order_by('-pontos')[:10]
        .values('escola__nome_escola', 'pontos')  
    )
    resultado = [{"escola_nome": c["escola__nome_escola"], "pontos": c["pontos"]} for c in qs]

    return resultado



def bottom_5_escolas_menos_pontos():
    pontos = (
        F('bag_plastico') + F('bag_papel') + F('bag_aluminio') + F('bag_eletronico') +
        F('bag_vazio') + F('bag_semi_cheio') + F('bag_cheio')
    )
    pontos = ExpressionWrapper(pontos, output_field=IntegerField())

    qs = (
        Questionario_coleta_escolar.objects
        .values('escola__nome_escola') 
        .annotate(pontos=pontos)
        .order_by('pontos')[:5]
    )

    return [{"escola_nome": c["escola__nome_escola"], "pontos": c["pontos"]} for c in qs]



def ranking_escolas_pontos():
    pontos_expr = (
        F('bag_plastico') + F('bag_papel') + F('bag_aluminio') + F('bag_eletronico') +
        F('bag_vazio') + F('bag_semi_cheio') + F('bag_cheio')
    )

    qs_agrupado = (
        Questionario_coleta_escolar.objects
        .values('escola__nome_escola')
        .annotate(total_pontos=Sum(pontos_expr, output_field=IntegerField()))
    )

    top_10 = qs_agrupado.order_by('-total_pontos')[:10]
    bottom_5 = qs_agrupado.order_by('total_pontos')[:5]

    return {
        "top_10_escolas": [
            {"escola_nome": item["escola__nome_escola"], "pontos": item["total_pontos"]}
            for item in top_10
        ],
        "bottom_5_escolas": [
            {"escola_nome": item["escola__nome_escola"], "pontos": item["total_pontos"]}
            for item in bottom_5
        ],
    }