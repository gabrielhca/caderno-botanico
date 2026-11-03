"""Fixtures dos testes de interface (Qt)."""

import os

import pytest

# Antes de criar o aplicativo Qt: sem janelas reais e sem placa de vídeo (serve também no CI).
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_BACKEND", "software")

from PySide6.QtGui import QGuiApplication  # noqa: E402


@pytest.fixture(scope="session")
def qapp():
    """Instância única do aplicativo Qt, necessária para objetos QObject e QML nos testes."""
    return QGuiApplication.instance() or QGuiApplication([])
