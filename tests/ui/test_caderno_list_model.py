"""Testes do CadernoListModel: o contrato que o QML enxerga."""

from datetime import UTC, datetime

from caderno_botanico.domain.caderno import Caderno
from caderno_botanico.ui.caderno_list_model import CadernoListModel


def _modelo_com(*cadernos):
    modelo = CadernoListModel()
    modelo.set_cadernos(list(cadernos))
    return modelo


def test_modelo_novo_esta_vazio(qapp):
    assert CadernoListModel().rowCount() == 0


def test_row_count_acompanha_a_lista(qapp):
    modelo = _modelo_com(Caderno(nome="Horta"), Caderno(nome="Jardim"))

    assert modelo.rowCount() == 2


def test_papeis_expostos_ao_qml(qapp):
    nomes = {bytes(nome).decode() for nome in CadernoListModel().roleNames().values()}

    assert nomes == {"cadernoId", "nome", "descricao", "criadoEm"}


def test_data_devolve_cada_campo_pelo_papel(qapp):
    criado = datetime(2026, 11, 3, 12, 0, tzinfo=UTC)
    modelo = _modelo_com(Caderno(nome="Horta", descricao="Hortaliças", criado_em=criado, id=7))
    indice = modelo.index(0)

    assert modelo.data(indice, CadernoListModel.IdRole) == 7
    assert modelo.data(indice, CadernoListModel.NomeRole) == "Horta"
    assert modelo.data(indice, CadernoListModel.DescricaoRole) == "Hortaliças"
    assert modelo.data(indice, CadernoListModel.CriadoEmRole) == "03/11/2026"


def test_data_de_indice_invalido_devolve_none(qapp):
    modelo = _modelo_com(Caderno(nome="Horta"))

    assert modelo.data(modelo.index(5), CadernoListModel.NomeRole) is None


def test_set_cadernos_avisa_as_views(qapp):
    modelo = CadernoListModel()
    avisos = []
    modelo.modelReset.connect(lambda: avisos.append("reset"))

    modelo.set_cadernos([Caderno(nome="Horta")])

    assert avisos == ["reset"]
