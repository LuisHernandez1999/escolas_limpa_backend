from apps.escola.models import Escola
from apps.escola.serializer import EscolaSerializer
from django.db import transaction

def listar_escolas():
    escolas = Escola.objects.all()
    return EscolaSerializer(escolas, many=True).data

@transaction.atomic
def criar_escola(data):
    nome = data.get('nome_escola')
    if not nome:
        return None, {'nome_escola': ['este campo é obrigatório.']}

    if Escola.objects.filter(nome_escola__iexact=nome).exists():
        return None, {'nome_escola': ['já existe uma escola com esse nome.']}

    escola = Escola.objects.create(nome_escola=nome)
    return {'id': escola.id, 'nome_escola': escola.nome_escola}, None


def atualizar_escola(id, data):
    try:
        escola = Escola.objects.get(pk=id)
    except Escola.DoesNotExist:
        return None, {'erro': 'escola nao encontrada'}

    nome = data.get('nome_escola')
    if nome:
        escola.nome_escola = nome
        escola.save(update_fields=['nome_escola'])

    return {'id': escola.id, 'nome_escola': escola.nome_escola}, None

def deletar_escola(id):
    try:
        escola = Escola.objects.get(pk=id)
        nome = escola.nome_escola
        escola.delete()
        return {"nome_escola": nome}, None
    except Escola.DoesNotExist:
        return None, {"erro": "Escola não encontrada"}
    except Exception as e:
        return None, {"erro": str(e)}
