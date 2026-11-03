"""Interface de acesso aos cadernos. A implementação concreta fica na camada Storage."""

from abc import ABC, abstractmethod

from caderno_botanico.domain.caderno import Caderno


class CadernoRepository(ABC):
    """Contrato que qualquer armazenamento de cadernos precisa cumprir."""

    @abstractmethod
    def add(self, caderno: Caderno) -> Caderno:
        """Salva um caderno novo e devolve o caderno com o id definido."""

    @abstractmethod
    def update(self, caderno: Caderno) -> None:
        """Grava as alterações de um caderno que já existe."""

    @abstractmethod
    def get_by_id(self, caderno_id: int) -> Caderno | None:
        """Devolve o caderno com esse id, ou None se não existir."""

    @abstractmethod
    def list_all(self) -> list[Caderno]:
        """Devolve todos os cadernos, em ordem não especificada."""

    @abstractmethod
    def exists_by_name(self, nome_normalizado: str, exclude_id: int | None = None) -> bool:
        """Diz se já existe um caderno com esse nome normalizado.

        `exclude_id` ignora um caderno na checagem (usado ao editar o próprio caderno).
        """
