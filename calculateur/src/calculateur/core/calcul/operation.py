from dataclasses import dataclass

from calculateur.core.calcul.operateur_type import OperateurType


@dataclass(frozen=True)
class Operation:
    operande1: float = 0
    operande2: float = 0
    operateur: OperateurType = OperateurType.ADDITION
