"""Testes do ponto de montagem e da tela QML principal."""

import pytest
from PySide6.QtCore import QObject
from PySide6.QtQml import QQmlApplicationEngine

from caderno_botanico.app import carregar_interface, criar_controller
from caderno_botanico.storage.database import EM_MEMORIA, open_database


@pytest.fixture
def controller(qapp):
    connection = open_database(EM_MEMORIA)
    yield criar_controller(connection)
    connection.close()


def test_controller_montado_persiste_no_sqlite(controller):
    assert controller.criar("Horta", "Hortaliças") is True
    assert controller.total == 1


def test_tela_qml_carrega_sem_erros(qapp, controller):
    engine = QQmlApplicationEngine()

    assert carregar_interface(engine, controller) is True

    janela = engine.rootObjects()[0]
    assert janela.property("title") == "Caderno Botânico"


def test_tela_qml_cria_caderno_pelo_formulario(qapp, controller):
    engine = QQmlApplicationEngine()
    carregar_interface(engine, controller)
    janela = engine.rootObjects()[0]
    campo_nome = janela.findChild(QObject, "campoNome")
    botao_salvar = janela.findChild(QObject, "botaoSalvar")

    campo_nome.setProperty("text", "Jardim da frente")
    botao_salvar.clicked.emit()

    assert controller.total == 1
    assert campo_nome.property("text") == ""  # formulário limpo após salvar


def test_tela_qml_mostra_erro_de_nome_vazio(qapp, controller):
    engine = QQmlApplicationEngine()
    carregar_interface(engine, controller)
    janela = engine.rootObjects()[0]

    janela.findChild(QObject, "botaoSalvar").clicked.emit()

    mensagem = janela.findChild(QObject, "mensagemErro").property("text")
    assert mensagem == "O nome do caderno é obrigatório."
    assert controller.total == 0
