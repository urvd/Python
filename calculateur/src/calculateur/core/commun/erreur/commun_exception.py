from calculateur.core.commun.erreur.error_type import ErrorType


class CommunException(Exception):
    """Exception centralisée de l'application, porteuse d'un ErrorType."""

    def __init__(self, error_type: ErrorType, cause: BaseException) -> None:
        super().__init__(f"Calcul App Error type - {cause}")
        self.__cause__ = cause
        self._error_type = error_type

    @property
    def error_type(self) -> ErrorType:
        return self._error_type

    @error_type.setter
    def error_type(self, type_: ErrorType) -> None:
        self._error_type = type_
