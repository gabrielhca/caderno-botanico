"""Ponto de montagem: liga as camadas e abre a interface."""

import os
import sqlite3
import sys
from pathlib import Path

from PySide6.QtCore import QStandardPaths, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from caderno_botanico.services.caderno_service import CadernoService
from caderno_botanico.storage.database import open_database
from caderno_botanico.storage.sqlite_caderno_repository import SqliteCadernoRepository
from caderno_botanico.ui.caderno_controller import CadernoController

QML_PRINCIPAL = Path(__file__).parent / "ui" / "qml" / "Main.qml"
NOME_DO_APLICATIVO = "caderno-botanico"
VARIAVEL_DO_BANCO = "CADERNO_BOTANICO_DB"  # permite usar outro banco em testes manuais


def caminho_do_banco() -> Path:
    """Onde o banco fica: pasta de dados do usuário, ou o caminho da variável de ambiente."""
    caminho_manual = os.environ.get(VARIAVEL_DO_BANCO)
    if caminho_manual:
        return Path(caminho_manual)
    pasta = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
    return Path(pasta) / "caderno_botanico.db"


def criar_controller(connection: sqlite3.Connection) -> CadernoController:
    """Monta repositório, service e controller a partir de uma conexão aberta."""
    repository = SqliteCadernoRepository(connection)
    service = CadernoService(repository)
    return CadernoController(service)


def carregar_interface(engine: QQmlApplicationEngine, controller: CadernoController) -> bool:
    """Carrega a tela principal. Devolve False se o QML não pôde ser carregado."""
    engine.setInitialProperties({"controller": controller})
    engine.load(QUrl.fromLocalFile(str(QML_PRINCIPAL)))
    return bool(engine.rootObjects())


def main() -> int:
    app = QGuiApplication(sys.argv)
    app.setApplicationName(NOME_DO_APLICATIVO)

    connection = open_database(caminho_do_banco())
    controller = criar_controller(connection)
    engine = QQmlApplicationEngine()
    if not carregar_interface(engine, controller):
        connection.close()
        return 1

    codigo = app.exec()
    connection.close()
    return codigo
