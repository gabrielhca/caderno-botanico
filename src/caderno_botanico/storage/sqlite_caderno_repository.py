"""Implementação do CadernoRepository em SQLite."""

import sqlite3
from datetime import datetime

from caderno_botanico.domain.caderno import Caderno
from caderno_botanico.domain.erros import CadernoNaoEncontradoError, NomeDuplicadoError
from caderno_botanico.repositories.caderno_repository import CadernoRepository

_COLUNAS = "id, nome, descricao, criado_em"


class SqliteCadernoRepository(CadernoRepository):
    """Guarda os cadernos na tabela `cadernos`. Só esta camada fala SQL."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add(self, caderno: Caderno) -> Caderno:
        try:
            with self._connection:
                cursor = self._connection.execute(
                    "INSERT INTO cadernos (nome, nome_normalizado, descricao, criado_em) "
                    "VALUES (?, ?, ?, ?)",
                    (
                        caderno.nome,
                        caderno.nome_normalizado,
                        caderno.descricao,
                        caderno.criado_em.isoformat(),
                    ),
                )
        except sqlite3.IntegrityError as erro:
            raise NomeDuplicadoError() from erro
        return Caderno(
            nome=caderno.nome,
            descricao=caderno.descricao,
            criado_em=caderno.criado_em,
            id=cursor.lastrowid,
        )

    def update(self, caderno: Caderno) -> None:
        try:
            with self._connection:
                cursor = self._connection.execute(
                    "UPDATE cadernos SET nome = ?, nome_normalizado = ?, descricao = ? "
                    "WHERE id = ?",
                    (caderno.nome, caderno.nome_normalizado, caderno.descricao, caderno.id),
                )
        except sqlite3.IntegrityError as erro:
            raise NomeDuplicadoError() from erro
        if cursor.rowcount == 0:
            raise CadernoNaoEncontradoError("O caderno não foi encontrado.")

    def get_by_id(self, caderno_id: int) -> Caderno | None:
        linha = self._connection.execute(
            f"SELECT {_COLUNAS} FROM cadernos WHERE id = ?", (caderno_id,)
        ).fetchone()
        return _para_caderno(linha) if linha else None

    def list_all(self) -> list[Caderno]:
        linhas = self._connection.execute(f"SELECT {_COLUNAS} FROM cadernos ORDER BY id")
        return [_para_caderno(linha) for linha in linhas]

    def exists_by_name(self, nome_normalizado: str, exclude_id: int | None = None) -> bool:
        linha = self._connection.execute(
            "SELECT 1 FROM cadernos WHERE nome_normalizado = ? AND (? IS NULL OR id != ?)",
            (nome_normalizado, exclude_id, exclude_id),
        ).fetchone()
        return linha is not None


def _para_caderno(linha: tuple) -> Caderno:
    caderno_id, nome, descricao, criado_em = linha
    return Caderno(
        nome=nome,
        descricao=descricao,
        criado_em=datetime.fromisoformat(criado_em),
        id=caderno_id,
    )
