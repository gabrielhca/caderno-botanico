"""Modelo de lista de cadernos para o QML (Model/View)."""

from PySide6.QtCore import QAbstractListModel, QModelIndex, QObject, Qt

from caderno_botanico.domain.caderno import Caderno


class CadernoListModel(QAbstractListModel):
    """Expõe uma lista de cadernos ao QML, uma linha por caderno.

    O QML lê cada campo pelo nome do papel (role): `cadernoId`, `nome`, `descricao` e `criadoEm`.
    """

    IdRole = Qt.ItemDataRole.UserRole + 1
    NomeRole = Qt.ItemDataRole.UserRole + 2
    DescricaoRole = Qt.ItemDataRole.UserRole + 3
    CriadoEmRole = Qt.ItemDataRole.UserRole + 4

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._cadernos: list[Caderno] = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: B008
        return 0 if parent.isValid() else len(self._cadernos)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < len(self._cadernos):
            return None
        caderno = self._cadernos[index.row()]
        if role == self.IdRole:
            return caderno.id
        if role in (self.NomeRole, Qt.ItemDataRole.DisplayRole):
            return caderno.nome
        if role == self.DescricaoRole:
            return caderno.descricao
        if role == self.CriadoEmRole:
            return caderno.criado_em.astimezone().strftime("%d/%m/%Y")
        return None

    def roleNames(self) -> dict:
        return {
            self.IdRole: b"cadernoId",
            self.NomeRole: b"nome",
            self.DescricaoRole: b"descricao",
            self.CriadoEmRole: b"criadoEm",
        }

    def set_cadernos(self, cadernos: list[Caderno]) -> None:
        """Troca o conteúdo inteiro do modelo e avisa as views para se atualizarem."""
        self.beginResetModel()
        self._cadernos = list(cadernos)
        self.endResetModel()
