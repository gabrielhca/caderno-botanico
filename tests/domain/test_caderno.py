"""Testes da entidade Caderno (cenários da spec caderno-cultivo)."""

from datetime import UTC

import pytest

from caderno_botanico.domain.caderno import TAMANHO_MAXIMO_NOME, Caderno, normalizar_nome
from caderno_botanico.domain.erros import NomeInvalidoError


def test_cria_caderno_com_nome_e_descricao():
    caderno = Caderno(nome="Horta dos fundos", descricao="Hortaliças e legumes")

    assert caderno.nome == "Horta dos fundos"
    assert caderno.descricao == "Hortaliças e legumes"
    assert caderno.criado_em.tzinfo == UTC


def test_descricao_e_opcional():
    assert Caderno(nome="Jardim da frente").descricao == ""


@pytest.mark.parametrize("nome", ["", "   ", "\t\n"])
def test_nome_vazio_ou_so_espacos_e_rejeitado(nome):
    with pytest.raises(NomeInvalidoError, match="obrigatório"):
        Caderno(nome=nome)


def test_nome_no_limite_e_aceito():
    nome = "a" * TAMANHO_MAXIMO_NOME

    assert Caderno(nome=nome).nome == nome


def test_nome_acima_do_limite_e_rejeitado():
    with pytest.raises(NomeInvalidoError, match="máximo"):
        Caderno(nome="a" * (TAMANHO_MAXIMO_NOME + 1))


def test_espacos_nas_pontas_nao_contam_no_limite():
    caderno = Caderno(nome="  " + "a" * TAMANHO_MAXIMO_NOME + "  ")

    assert len(caderno.nome) == TAMANHO_MAXIMO_NOME


@pytest.mark.parametrize("nome", ["Horta", "horta", "  hORTA "])
def test_nome_normalizado_ignora_caixa_e_espacos(nome):
    assert normalizar_nome(nome) == "horta"


def test_nome_normalizado_considera_letras_acentuadas():
    assert normalizar_nome("Ágata") == normalizar_nome("ágata")


def test_alterar_mantem_a_data_de_criacao():
    caderno = Caderno(nome="Horta")
    criado_em = caderno.criado_em

    caderno.alterar(nome="Horta nova", descricao="Canteiros elevados")

    assert caderno.nome == "Horta nova"
    assert caderno.descricao == "Canteiros elevados"
    assert caderno.criado_em == criado_em


def test_alterar_aplica_as_regras_de_nome_sem_perder_o_que_havia():
    caderno = Caderno(nome="Horta", descricao="Original")

    with pytest.raises(NomeInvalidoError):
        caderno.alterar(nome="   ", descricao="Outra")

    assert caderno.nome == "Horta"
    assert caderno.descricao == "Original"
