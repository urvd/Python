from calculateur.core.calcul.i_calcul import ICalcul
from calculateur.core.calcul.operateur_type import OperateurType
from calculateur.core.calcul.operation import Operation
from calculateur.core.commun.erreur.commun_exception import CommunException
from calculateur.core.commun.erreur.error_type import ErrorType
from calculateur.core.resultat.resultat import Resultat


class Calculateur(ICalcul):
    """Calculateur simple proposant des opérations."""

    def _additionner(self, a: float, b: float) -> Resultat:
        return Resultat(a + b, True)

    def _soustraire(self, a: float, b: float) -> Resultat:
        return Resultat(a - b, True)

    def _multiplier(self, a: float, b: float) -> Resultat:
        return Resultat(a * b, True)

    def _diviser(self, a: float, b: float) -> Resultat:
        if b == 0:
            raise ZeroDivisionError("Division par zéro impossible")
        return Resultat(a / b, True)

    def calculer(self, operation: Operation) -> Resultat:
        """Applique l'opérateur donné (+, -, * ou x, /) aux deux opérandes."""
        a, b = float(operation.operande1), float(operation.operande2)
        try:
            match operation.operateur:
                case OperateurType.ADDITION:
                    return self._additionner(a, b)
                case OperateurType.SOUSTRACTION:
                    return self._soustraire(a, b)
                case OperateurType.MULTIPLICATION | OperateurType.MULTIPLICATION_X:
                    return self._multiplier(a, b)
                case OperateurType.DIVISION:
                    return self._diviser(a, b)
                case _:
                    raise ValueError(f"Opérateur inconnu : {operation.operateur.symbole}")
        except ArithmeticError as e:
            raise CommunException(ErrorType.ARITHMETIC_ERROR, e) from e
        except ValueError as e:
            raise CommunException(ErrorType.ILLEGAL_ARGUMENT_ERROR, e) from e
