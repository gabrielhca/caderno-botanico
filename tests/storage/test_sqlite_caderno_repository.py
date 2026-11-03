"""Testes do SqliteCadernoRepository, com SQLite de verdade (em memória e em arquivo)."""

import pytest

from caderno_botanico.domain.caderno import Caderno
from caderno_botanico.domain.erros import CadernoNaoEncontradoError, NomeDuplicadoError
from caderno_botanico.repositories.caderno_repository import CadernoRepository
from caderno_botanico.storage.database import EM_MEMORIA, open_database
from caderno_botanico.storage.sqlite_caderno_repository import SqliteCadernoRepository


@pytest.fixture
def sqlite_repository():
    connection = open_database(EM_MEMORIA)
    yield SqliteCadernoRepository(connection)
    connection.close()


def test_cumpre_a_interface(sqlite_repository):
    assert isinstance(sqlite_repository, CadernoRepository)


def test_add_define_o_id_e_guarda_todos_os_campos(sqlite_repository):
    original = Caderno(nome="Horta dos fundos", descricao="Hortaliças")

    salvo = sqlite_repository.add(original)
    lido = sqlite_repository.get_by_id(salvo.id)

    assert salvo.id is not None
    assert (lido.nome, lido.descricao) == ("Horta dos fundos", "Hortaliças")
    assert lido.criado_em == original.criado_em


def test_get_by_id_inexistente_devolve_none(sqlite_repository):
    assert sqlite_repository.get_by_id(999) is None


@pytest.mark.parametrize("repetido", ["Horta", "horta", "  hORTA "])
def test_add_com_nome_duplicado_vira_erro_de_negocio(sqlite_repository, repetido):
    sqlite_repository.add(Caderno(nome="Horta"))

    with pytest.raises(NomeDuplicadoError):
        sqlite_repository.add(Caderno(nome=repetido))


def test_duplicidade_considera_letras_acentuadas(sqlite_repository):
    sqlite_repository.add(Caderno(nome="Ágata"))

    with pytest.raises(NomeDuplicadoError):
        sqlite_repository.add(Caderno(nome="ágata"))


def test_update_grava_alteracoes_e_mantem_a_data(sqlite_repository):
    salvo = sqlite_repository.add(Caderno(nome="Horta"))
    salvo.alterar(nome="Horta nova", descricao="Canteiros")

    sqlite_repository.update(salvo)
    lido = sqlite_repository.get_by_id(salvo.id)

    assert (lido.nome, lido.descricao) == ("Horta nova", "Canteiros")
    assert lido.criado_em == salvo.criado_em


def test_update_para_nome_de_outro_caderno_vira_erro_de_negocio(sqlite_repository):
    sqlite_repository.add(Caderno(nome="Horta"))
    jardim = sqlite_repository.add(Caderno(nome="Jardim"))
    jardim.alterar(nome="horta", descricao="")

    with pytest.raises(NomeDuplicadoError):
        sqlite_repository.update(jardim)


def test_update_de_caderno_inexistente(sqlite_repository):
    with pytest.raises(CadernoNaoEncontradoError):
        sqlite_repository.update(Caderno(nome="Fantasma", id=999))


def test_list_all_devolve_todos(sqlite_repository):
    sqlite_repository.add(Caderno(nome="Horta"))
    sqlite_repository.add(Caderno(nome="Jardim"))

    assert [c.nome for c in sqlite_repository.list_all()] == ["Horta", "Jardim"]


def test_exists_by_name_ignora_o_caderno_excluido(sqlite_repository):
    salvo = sqlite_repository.add(Caderno(nome="Horta"))

    assert sqlite_repository.exists_by_name("horta") is True
    assert sqlite_repository.exists_by_name("horta", exclude_id=salvo.id) is False
    assert sqlite_repository.exists_by_name("jardim") is False


def test_cadernos_continuam_disponiveis_apos_reabrir_o_banco(tmp_path):
    caminho = tmp_path / "caderno.db"
    primeira = open_database(caminho)
    SqliteCadernoRepository(primeira).add(Caderno(nome="Horta", descricao="Persistida"))
    primeira.close()

    segunda = open_database(caminho)
    cadernos = SqliteCadernoRepository(segunda).list_all()
    segunda.close()

    assert [(c.nome, c.descricao) for c in cadernos] == [("Horta", "Persistida")]
