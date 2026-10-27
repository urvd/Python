from abc import ABC, abstractmethod

from calculateur.core.calcul.operation import Operation
from calculateur.core.resultat.resultat import Resultat


class ICalcul(ABC):
    @abstractmethod
    def calculer(self, operation: Operation) -> Resultat: ...
