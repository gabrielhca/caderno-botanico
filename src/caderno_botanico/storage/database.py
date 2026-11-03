"""Abertura da conexão com o banco SQLite."""

import sqlite3
from pathlib import Path

from caderno_botanico.storage.schema import create_schema

EM_MEMORIA = ":memory:"


def open_database(path: str | Path) -> sqlite3.Connection:
    """Abre (e cria, se preciso) o banco no caminho informado, já com o esquema pronto.

    Use ":memory:" para um banco temporário, útil nos testes.
    """
    if str(path) != EM_MEMORIA:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    create_schema(connection)
    return connection
