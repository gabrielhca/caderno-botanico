"""Exceções de regra de negócio do domínio."""


class DomainError(Exception):
    """Base de todos os erros de regra de negócio. A mensagem é mostrada ao usuário."""


class NomeInvalidoError(DomainError):
    """O nome informado não respeita as regras (vazio ou longo demais)."""


class NomeDuplicadoError(DomainError):
    """Já existe um caderno com esse nome."""


class CadernoNaoEncontradoError(DomainError):
    """O caderno pedido não existe."""
