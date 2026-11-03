"""Casos de uso dos cadernos (US01 e US02). Python puro: sem Qt e sem SQLite."""

from caderno_botanico.domain.caderno import Caderno, normalizar_nome, validar_nome
from caderno_botanico.domain.erros import CadernoNaoEncontradoError, NomeDuplicadoError
from caderno_botanico.repositories.caderno_repository import CadernoRepository

MENSAGEM_NOME_DUPLICADO = "Já existe um caderno com esse nome."


class CadernoService:
    """Orquestra a criação, edição e listagem de cadernos."""

    def __init__(self, repository: CadernoRepository) -> None:
        self._repository = repository

    def criar(self, nome: str, descricao: str = "") -> Caderno:
        caderno = Caderno(nome=nome, descricao=descricao)  # valida o nome
        self._garantir_nome_livre(caderno.nome_normalizado)
        return self._repository.add(caderno)

    def editar(self, caderno_id: int, nome: str, descricao: str) -> Caderno:
        caderno = self._repository.get_by_id(caderno_id)
        if caderno is None:
            raise CadernoNaoEncontradoError("O caderno não foi encontrado.")

        nome_valido = validar_nome(nome)
        self._garantir_nome_livre(normalizar_nome(nome_valido), ignorar_id=caderno_id)

        caderno.alterar(nome_valido, descricao)
        self._repository.update(caderno)
        return caderno

    def listar(self) -> list[Caderno]:
        """Devolve os cadernos em ordem alfabética, sem diferenciar maiúsculas de minúsculas."""
        return sorted(self._repository.list_all(), key=lambda caderno: caderno.nome_normalizado)

    def _garantir_nome_livre(self, nome_normalizado: str, ignorar_id: int | None = None) -> None:
        if self._repository.exists_by_name(nome_normalizado, exclude_id=ignorar_id):
            raise NomeDuplicadoError(MENSAGEM_NOME_DUPLICADO)
