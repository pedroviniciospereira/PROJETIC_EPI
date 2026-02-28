import pytest
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.test import Client

from colaboradores.models import Colaborador
from equipamentos.models import Equipamento
from emprestimos.models import Emprestimo, ItemEmprestado, HistoricoDevolucao


# ==========================================================
# CT-001 Cadastro de Colaborador
# ==========================================================
@pytest.mark.django_db
def test_ct_001_cadastro_colaborador():
    colaborador = Colaborador.objects.create(
        nome_completo="Nicoly Bourdot",
        matricula="123",
        funcao="Técnica"
    )

    assert colaborador.nome_completo == "Nicoly Bourdot"
    assert colaborador.status == "Ativo"


# ==========================================================
# CT-002 Cadastro de Equipamento
# ==========================================================
@pytest.mark.django_db
def test_ct_002_cadastro_equipamento():
    equipamento = Equipamento.objects.create(
        nome="Capacete",
        categoria="CABECA",
        ca="98765",
        estoque_total=10
    )

    assert equipamento.estoque_total == 10
    assert equipamento.estoque_disponivel == 10


# ==========================================================
# CT-003 Cadastro de Empréstimo
# ==========================================================
@pytest.mark.django_db
def test_ct_003_cadastro_emprestimo():
    colaborador = Colaborador.objects.create(
        nome_completo="João Silva",
        matricula="222",
        funcao="Operador"
    )

    emprestimo = Emprestimo.objects.create(
        colaborador=colaborador,
        data_prevista_devolucao=timezone.now().date()
    )

    assert emprestimo.status == "ATIVO"


# ==========================================================
# CT-004 Estoque insuficiente (quantidade 0)
# ==========================================================
@pytest.mark.django_db
def test_ct_004_estoque_zero():
    equipamento = Equipamento.objects.create(
        nome="Luva",
        estoque_total=0
    )

    assert equipamento.estoque_disponivel == 0


# ==========================================================
# CT-005 Login
# ==========================================================
@pytest.mark.django_db
def test_ct_005_login_usuario():
    client = Client()

    User.objects.create_user(username="nico", password="123456")

    login = client.login(username="nico", password="123456")

    assert login is True


# ==========================================================
# CT-006 Atualização de estoque (simulação manual)
# ==========================================================
@pytest.mark.django_db
def test_ct_006_baixa_manual_estoque():
    equipamento = Equipamento.objects.create(
        nome="Óculos",
        estoque_total=10
    )

    equipamento.estoque_disponivel -= 1
    equipamento.save()

    assert equipamento.estoque_disponivel == 9


# ==========================================================
# CT-007 Devolução aumenta estoque (usando histórico)
# ==========================================================
@pytest.mark.django_db
def test_ct_007_devolucao_com_historico():
    colaborador = Colaborador.objects.create(
        nome_completo="Carlos",
        matricula="333",
        funcao="Auxiliar"
    )

    equipamento = Equipamento.objects.create(
        nome="Bota",
        estoque_total=5
    )

    emprestimo = Emprestimo.objects.create(
        colaborador=colaborador,
        data_prevista_devolucao=timezone.now().date()
    )

    item = ItemEmprestado.objects.create(
        emprestimo=emprestimo,
        equipamento=equipamento,
        quantidade_emprestada=2
    )

    HistoricoDevolucao.objects.create(
        item_emprestado=item,
        quantidade_devolvida=1,
        status_devolucao="DEVOLVIDO"
    )

    assert item.get_quantidade_pendente() == 1


# ==========================================================
# CT-008 Matrícula duplicada
# ==========================================================
@pytest.mark.django_db
def test_ct_008_matricula_duplicada():
    Colaborador.objects.create(
        nome_completo="Original",
        matricula="999",
        funcao="Operador"
    )

    with pytest.raises(IntegrityError):
        Colaborador.objects.create(
            nome_completo="Duplicado",
            matricula="999",
            funcao="Auxiliar"
        )


# ==========================================================
# CT-009 Histórico por colaborador
# ==========================================================
@pytest.mark.django_db
def test_ct_009_historico_colaborador():
    colaborador = Colaborador.objects.create(
        nome_completo="Marcos",
        matricula="555",
        funcao="Técnico"
    )

    Emprestimo.objects.create(
        colaborador=colaborador,
        data_prevista_devolucao=timezone.now().date()
    )

    assert colaborador.emprestimos.count() == 1


# ==========================================================
# CT-010 Equipamento duplicado
# ==========================================================
@pytest.mark.django_db
def test_ct_010_equipamento_duplicado():
    Equipamento.objects.create(
        nome="Capacete Classe B",
        estoque_total=5
    )

    with pytest.raises(IntegrityError):
        Equipamento.objects.create(
            nome="Capacete Classe B",
            estoque_total=3
        )