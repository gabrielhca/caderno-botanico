"""Testes do CadernoService (cenários da spec caderno-cultivo)."""

import pytest

from caderno_botanico.domain.erros import (
    CadernoNaoEncontradoError,
    NomeDuplicadoError,
    NomeInvalidoError,
)


def test_criar_com_nome_e_descricao(service):
    caderno = service.criar("Horta dos fundos", "Hortaliças e legumes")

    assert caderno.id is not None
    assert caderno.nome == "Horta dos fundos"
    assert caderno.descricao == "Hortaliças e legumes"
    assert [c.nome for c in service.listar()] == ["Horta dos fundos"]


def test_criar_apenas_com_nome(service):
    assert service.criar("Jardim da frente").descricao == ""


def test_criar_com_nome_vazio_nao_salva_nada(service):
    with pytest.raises(NomeInvalidoError):
        service.criar("   ")

    assert service.listar() == []


@pytest.mark.parametrize("nome_repetido", ["Horta", "horta", "  hORTA "])
def test_criar_com_nome_ja_existente_e_rejeitado(service, nome_repetido):
    service.criar("Horta")

    with pytest.raises(NomeDuplicadoError, match="Já existe um caderno"):
        service.criar(nome_repetido)

    assert len(service.listar()) == 1


def test_editar_apenas_a_descricao_mantem_nome_e_data(service):
    criado = service.criar("Horta")

    editado = service.editar(criado.id, "Horta", "Canteiros elevados")

    assert editado.nome == "Horta"
    assert editado.descricao == "Canteiros elevados"
    assert editado.criado_em == criado.criado_em


def test_editar_sem_mudar_o_nome_nao_acusa_duplicado(service):
    criado = service.criar("Horta")

    service.editar(criado.id, "  horta ", "")  # mesmo nome, só com outra caixa


def test_renomear_para_o_nome_de_outro_caderno_e_rejeitado(service):
    service.criar("Horta")
    jardim = service.criar("Jardim")

    with pytest.raises(NomeDuplicadoError):
        service.editar(jardim.id, "horta", "")

    assert sorted(c.nome for c in service.listar()) == ["Horta", "Jardim"]


def test_editar_com_nome_invalido_nao_altera_nada(service):
    criado = service.criar("Horta", "Original")

    with pytest.raises(NomeInvalidoError):
        service.editar(criado.id, "   ", "Outra")

    salvo = service.listar()[0]
    assert (salvo.nome, salvo.descricao) == ("Horta", "Original")


def test_editar_caderno_inexistente(service):
    with pytest.raises(CadernoNaoEncontradoError):
        service.editar(999, "Horta", "")


def test_listar_em_ordem_alfabetica_sem_diferenciar_caixa(service):
    for nome in ["Varanda", "horta", "Jardim"]:
        service.criar(nome)

    assert [c.nome for c in service.listar()] == ["horta", "Jardim", "Varanda"]


def test_listar_sem_cadernos_devolve_lista_vazia(service):
    assert service.listar() == []
