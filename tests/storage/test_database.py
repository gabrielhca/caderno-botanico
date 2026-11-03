"""Testes da criação do esquema SQLite."""

from caderno_botanico.storage.database import EM_MEMORIA, open_database
from caderno_botanico.storage.schema import SCHEMA_VERSION


def _tabelas(connection):
    linhas = connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    return {linha[0] for linha in linhas}


def test_esquema_e_criado_em_banco_novo():
    connection = open_database(EM_MEMORIA)

    assert "cadernos" in _tabelas(connection)
    assert connection.execute("PRAGMA user_version").fetchone()[0] == SCHEMA_VERSION


def test_abrir_banco_existente_nao_recria_nem_apaga_dados(tmp_path):
    caminho = tmp_path / "dados" / "caderno.db"
    primeira = open_database(caminho)
    with primeira:
        primeira.execute(
            "INSERT INTO cadernos (nome, nome_normalizado, criado_em) "
            "VALUES ('Horta', 'horta', 'x')"
        )
    primeira.close()

    segunda = open_database(caminho)

    assert segunda.execute("SELECT COUNT(*) FROM cadernos").fetchone()[0] == 1
    segunda.close()
