"""Entidade Caderno e suas regras de negócio (capacidade caderno-cultivo)."""

from dataclasses import dataclass, field
from datetime import UTC, datetime

from caderno_botanico.domain.erros import NomeInvalidoError

TAMANHO_MAXIMO_NOME = 80


def normalizar_nome(nome: str) -> str:
    """Devolve o nome sem espaços nas pontas e sem diferenciar maiúsculas de minúsculas."""
    return nome.strip().casefold()


def validar_nome(nome: str) -> str:
    """Valida o nome e devolve a versão sem espaços nas pontas."""
    limpo = nome.strip()
    if not limpo:
        raise NomeInvalidoError("O nome do caderno é obrigatório.")
    if len(limpo) > TAMANHO_MAXIMO_NOME:
        raise NomeInvalidoError(
            f"O nome do caderno deve ter no máximo {TAMANHO_MAXIMO_NOME} caracteres."
        )
    return limpo


@dataclass
class Caderno:
    """Contêiner de plantas de um ambiente de cultivo."""

    nome: str
    descricao: str = ""
    criado_em: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: int | None = None  # definido pelo armazenamento ao salvar

    def __post_init__(self) -> None:
        self.nome = validar_nome(self.nome)
        self.descricao = self.descricao.strip()

    @property
    def nome_normalizado(self) -> str:
        """Forma do nome usada para comparar duplicidade."""
        return normalizar_nome(self.nome)

    def alterar(self, nome: str, descricao: str) -> None:
        """Altera nome e descrição com as mesmas regras da criação. A data de criação não muda."""
        novo_nome = validar_nome(nome)  # se for inválido, nada é alterado
        self.nome = novo_nome
        self.descricao = descricao.strip()
