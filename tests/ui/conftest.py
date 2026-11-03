"""Fixtures dos testes de interface (Qt)."""

import pytest
from PySide6.QtCore import QCoreApplication


@pytest.fixture(scope="session")
def qapp():
    """Instância única do aplicativo Qt, necessária para objetos QObject nos testes."""
    return QCoreApplication.instance() or QCoreApplication([])
