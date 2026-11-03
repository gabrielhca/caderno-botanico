"""Esquema do banco SQLite e controle de versão."""

import sqlite3

SCHEMA_VERSION = 1

_CRIAR_TABELA_CADERNOS = """
CREATE TABLE IF NOT EXISTS cadernos (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    nome             TEXT NOT NULL,
    nome_normalizado TEXT NOT NULL UNIQUE,
    descricao        TEXT NOT NULL DEFAULT '',
    criado_em        TEXT NOT NULL
)
"""


def create_schema(connection: sqlite3.Connection) -> None:
    """Cria as tabelas se o banco ainda não estiver na versão atual. Pode ser chamada sempre."""
    versao_atual = connection.execute("PRAGMA user_version").fetchone()[0]
    if versao_atual >= SCHEMA_VERSION:
        return
    with connection:
        connection.execute(_CRIAR_TABELA_CADERNOS)
        connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
