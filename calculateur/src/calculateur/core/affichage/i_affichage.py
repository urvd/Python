from abc import ABC, abstractmethod

from calculateur.core.action.action_type import ActionType


class IAffichage(ABC):
    @abstractmethod
    def commencer(self) -> None: ...

    @abstractmethod
    def terminer(self) -> None: ...

    @abstractmethod
    def afficher(self, texte: str) -> None: ...

    @abstractmethod
    def verifier_action_user(self, ligne: str) -> ActionType: ...

    @abstractmethod
    def verifier_format_ok(self, ligne: str) -> bool: ...
