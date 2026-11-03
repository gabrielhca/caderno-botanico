"""Controlador que liga o QML ao CadernoService (ponte Qt/Python)."""

from collections.abc import Callable

from PySide6.QtCore import Property, QObject, Signal, Slot

from caderno_botanico.domain.erros import DomainError
from caderno_botanico.services.caderno_service import CadernoService
from caderno_botanico.ui.caderno_list_model import CadernoListModel


class CadernoController(QObject):
    """Expõe ao QML: o modelo da lista, o total, os slots criar/editar e os signals de resultado.

    Não contém regra de negócio: chama o Service e traduz o resultado para a tela.
    """

    totalChanged = Signal()
    cadernoSalvo = Signal()
    erroOcorrido = Signal(str)

    def __init__(self, service: CadernoService, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._service = service
        self._model = CadernoListModel(self)
        self._recarregar()

    @Property(QObject, constant=True)
    def cadernos(self) -> QObject:
        return self._model

    @Property(int, notify=totalChanged)
    def total(self) -> int:
        return self._model.rowCount()

    @Slot(str, str, result=bool)
    def criar(self, nome: str, descricao: str) -> bool:
        return self._executar(lambda: self._service.criar(nome, descricao))

    @Slot(int, str, str, result=bool)
    def editar(self, caderno_id: int, nome: str, descricao: str) -> bool:
        return self._executar(lambda: self._service.editar(caderno_id, nome, descricao))

    def _executar(self, acao: Callable[[], object]) -> bool:
        try:
            acao()
        except DomainError as erro:
            self.erroOcorrido.emit(str(erro))
            return False
        self._recarregar()
        self.cadernoSalvo.emit()
        return True

    def _recarregar(self) -> None:
        total_anterior = self._model.rowCount()
        self._model.set_cadernos(self._service.listar())
        if self._model.rowCount() != total_anterior:
            self.totalChanged.emit()
