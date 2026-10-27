import pytest

from calculateur.core.calcul.calculateur import Calculateur
from calculateur.core.calcul.i_calcul import ICalcul
from calculateur.core.calcul.operateur_type import OperateurType
from calculateur.core.calcul.operation import Operation
from calculateur.core.commun.erreur.commun_exception import CommunException

calculateur: ICalcul = Calculateur()


def test_additionner():
    assert calculateur.calculer(Operation(3, 4, OperateurType.ADDITION)).valeur == 7


def test_soustraire():
    assert calculateur.calculer(Operation(3, 4, OperateurType.SOUSTRACTION)).valeur == -1


def test_multiplier():
    assert calculateur.calculer(Operation(3, 4, OperateurType.MULTIPLICATION)).valeur == 12


def test_calculer_autre_operateur_multiplication():
    assert calculateur.calculer(Operation(3, 3, OperateurType.MULTIPLICATION_X)).valeur == 9


def test_diviser():
    assert calculateur.calculer(Operation(5, 2, OperateurType.DIVISION)).valeur == 2.5


# Exception centralisée
# Test : la division par zéro et l'opérateur inconnu.
def test_diviser_par_zero():
    with pytest.raises(CommunException):
        calculateur.calculer(Operation(1, 0, OperateurType.DIVISION))


def test_operateur_inconnu():
    with pytest.raises(CommunException):
        calculateur.calculer(Operation(1, 2, OperateurType.recherche_operateur("_")))
