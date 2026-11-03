"""Testes do CadernoController: a ponte entre o QML e o Service."""

import pytest

from caderno_botanico.ui.caderno_controller import CadernoController
from caderno_botanico.ui.caderno_list_model import CadernoListModel


@pytest.fixture
def controller(qapp, service):
    return CadernoController(service)


def _nomes(controller):
    modelo = controller.cadernos
    return [
        modelo.data(modelo.index(i), CadernoListModel.NomeRole) for i in range(modelo.rowCount())
    ]


def test_inicia_carregando_os_cadernos_existentes(qapp, service):
    service.criar("Horta")

    controller = CadernoController(service)

    assert controller.total == 1
    assert _nomes(controller) == ["Horta"]


def test_criar_com_sucesso_atualiza_modelo_total_e_avisa(controller):
    eventos = []
    controller.cadernoSalvo.connect(lambda: eventos.append("salvo"))
    controller.totalChanged.connect(lambda: eventos.append("total"))

    resultado = controller.criar("Horta", "Hortaliças")

    assert resultado is True
    assert controller.total == 1
    assert _nomes(controller) == ["Horta"]
    assert "salvo" in eventos
    assert "total" in eventos


def test_criar_com_nome_vazio_emite_erro_em_portugues(controller):
    erros = []
    controller.erroOcorrido.connect(erros.append)

    resultado = controller.criar("   ", "")

    assert resultado is False
    assert erros == ["O nome do caderno é obrigatório."]
    assert controller.total == 0


def test_criar_com_nome_duplicado_emite_erro(controller):
    controller.criar("Horta", "")
    erros = []
    controller.erroOcorrido.connect(erros.append)

    resultado = controller.criar("horta", "")

    assert resultado is False
    assert erros == ["Já existe um caderno com esse nome."]
    assert controller.total == 1


def test_editar_atualiza_o_modelo(controller):
    controller.criar("Horta", "")
    caderno_id = controller.cadernos.data(controller.cadernos.index(0), CadernoListModel.IdRole)

    resultado = controller.editar(caderno_id, "Horta nova", "Canteiros")

    assert resultado is True
    assert _nomes(controller) == ["Horta nova"]


def test_editar_caderno_inexistente_emite_erro(controller):
    erros = []
    controller.erroOcorrido.connect(erros.append)

    assert controller.editar(999, "Horta", "") is False
    assert erros == ["O caderno não foi encontrado."]


def test_lista_segue_a_ordem_alfabetica_do_service(controller):
    for nome in ["Varanda", "horta", "Jardim"]:
        controller.criar(nome, "")

    assert _nomes(controller) == ["horta", "Jardim", "Varanda"]
