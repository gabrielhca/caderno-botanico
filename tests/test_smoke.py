"""Teste de fumaça: garante que o pacote e as camadas podem ser importados."""

import importlib

import pytest

CAMADAS = ["ui", "services", "domain", "repositories", "storage"]


@pytest.mark.parametrize("camada", CAMADAS)
def test_camada_pode_ser_importada(camada):
    modulo = importlib.import_module(f"caderno_botanico.{camada}")
    assert modulo is not None
