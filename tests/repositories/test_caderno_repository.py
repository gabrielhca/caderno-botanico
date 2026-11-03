"""Testes do repositório falso: ele precisa se comportar como um repositório de verdade."""

from caderno_botanico.domain.caderno import Caderno
from caderno_botanico.repositories.caderno_repository import CadernoRepository


def test_repositorio_falso_cumpre_a_interface(repository):
    assert isinstance(repository, CadernoRepository)


def test_add_define_o_id_e_permite_buscar(repository):
    salvo = repository.add(Caderno(nome="Horta"))

    assert salvo.id == 1
    assert repository.get_by_id(1).nome == "Horta"
    assert repository.get_by_id(99) is None


def test_alterar_o_objeto_em_maos_nao_muda_o_que_esta_salvo(repository):
    salvo = repository.add(Caderno(nome="Horta"))

    salvo.alterar(nome="Outro", descricao="")

    assert repository.get_by_id(salvo.id).nome == "Horta"


def test_update_grava_as_alteracoes(repository):
    salvo = repository.add(Caderno(nome="Horta"))
    salvo.alterar(nome="Horta nova", descricao="")

    repository.update(salvo)

    assert repository.get_by_id(salvo.id).nome == "Horta nova"


def test_exists_by_name_ignora_o_caderno_excluido(repository):
    salvo = repository.add(Caderno(nome="Horta"))

    assert repository.exists_by_name("horta") is True
    assert repository.exists_by_name("horta", exclude_id=salvo.id) is False
    assert repository.exists_by_name("jardim") is False
