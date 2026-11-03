"""Fixtures compartilhadas pelos testes."""

import dataclasses

import pytest

from caderno_botanico.domain.caderno import Caderno
from caderno_botanico.repositories.caderno_repository import CadernoRepository
from caderno_botanico.services.caderno_service import CadernoService


class InMemoryCadernoRepository(CadernoRepository):
    """Repositório falso, só em memória, para testar o Service sem banco de dados.

    Guarda e devolve cópias, como um banco de verdade faria, para que alterar um objeto
    em mãos não mude o que está "salvo".
    """

    def __init__(self) -> None:
        self._items: dict[int, Caderno] = {}
        self._next_id = 1

    def add(self, caderno: Caderno) -> Caderno:
        salvo = dataclasses.replace(caderno, id=self._next_id)
        self._items[self._next_id] = salvo
        self._next_id += 1
        return dataclasses.replace(salvo)

    def update(self, caderno: Caderno) -> None:
        self._items[caderno.id] = dataclasses.replace(caderno)

    def get_by_id(self, caderno_id: int) -> Caderno | None:
        item = self._items.get(caderno_id)
        return dataclasses.replace(item) if item else None

    def list_all(self) -> list[Caderno]:
        return [dataclasses.replace(item) for item in self._items.values()]

    def exists_by_name(self, nome_normalizado: str, exclude_id: int | None = None) -> bool:
        return any(
            item.nome_normalizado == nome_normalizado and item.id != exclude_id
            for item in self._items.values()
        )


@pytest.fixture
def repository() -> InMemoryCadernoRepository:
    return InMemoryCadernoRepository()


@pytest.fixture
def service(repository: InMemoryCadernoRepository) -> CadernoService:
    return CadernoService(repository)
