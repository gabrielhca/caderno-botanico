"""Testes de arquitetura: garantem as regras de dependência do project.md.

Só imports absolutos são verificados; por isso o projeto usa sempre imports absolutos.
"""

import ast
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent / "src" / "caderno_botanico"

# O Domain não pode depender de infraestrutura nem de outras camadas.
PROIBIDOS_NO_DOMAIN = (
    "PySide6",
    "sqlite3",
    "caderno_botanico.ui",
    "caderno_botanico.services",
    "caderno_botanico.repositories",
    "caderno_botanico.storage",
)

# Só o Storage pode acessar o SQLite.
CAMADAS_SEM_SQLITE = ("ui", "services", "domain", "repositories")

# Só a UI pode usar o Qt: Services, Domain, Repositories e Storage são Python puro.
CAMADAS_SEM_QT = ("services", "domain", "repositories", "storage")


def _importacoes(arquivo: Path):
    arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            for alias in no.names:
                yield alias.name
        elif isinstance(no, ast.ImportFrom) and no.module:
            yield no.module


def _violacoes(camadas: tuple[str, ...], proibido: str) -> list[str]:
    violacoes = []
    for camada in camadas:
        for arquivo in (RAIZ / camada).rglob("*.py"):
            for modulo in _importacoes(arquivo):
                if modulo.startswith(proibido):
                    violacoes.append(f"{camada}/{arquivo.name}: {modulo}")
    return violacoes


def test_domain_nao_depende_de_outras_camadas():
    violacoes = []
    for arquivo in (RAIZ / "domain").rglob("*.py"):
        for modulo in _importacoes(arquivo):
            if modulo.startswith(PROIBIDOS_NO_DOMAIN):
                violacoes.append(f"{arquivo.name}: {modulo}")
    assert not violacoes, violacoes


def test_somente_storage_acessa_sqlite():
    assert not _violacoes(CAMADAS_SEM_SQLITE, "sqlite3")


def test_somente_ui_usa_pyside6():
    assert not _violacoes(CAMADAS_SEM_QT, "PySide6")
