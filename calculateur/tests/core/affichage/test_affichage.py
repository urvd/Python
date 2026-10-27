import pytest

from calculateur.core.action.action_type import ActionType
from calculateur.core.affichage.affichage import Affichage
from calculateur.core.affichage.i_affichage import IAffichage
from calculateur.core.commun.erreur.commun_exception import CommunException

affichage: IAffichage = Affichage()
TEXTE_ANNULATION = "q"
TEXTE_RECALCULER = "r"
TEXTE_CALCULER = "c"
TEXTE_AUTRE = "p"
TEXTE_FORMAT_OK1 = "3 x 3"
TEXTE_FORMAT_OK2 = "L S U"
TEXTE_FORMAT_OK3 = "L S  U"
TEXTE_FORMAT_STR0 = " S U"
TEXTE_FORMAT_STR1 = "LSU"
TEXTE_FORMAT_STR2 = "L"
TEXTE_FORMAT_STR3 = "45-79"


def test_affichage_verification_annulation():
    assert affichage.verifier_action_user(TEXTE_ANNULATION) == ActionType.QUITTER


def test_affichage_verification_calculer():
    assert affichage.verifier_action_user(TEXTE_CALCULER) == ActionType.CALCULER
    assert affichage.verifier_action_user(TEXTE_AUTRE) == ActionType.CALCULER


def test_affichage_verification_recalculer():
    assert affichage.verifier_action_user(TEXTE_RECALCULER) == ActionType.RE_CALCULER


def test_affichage_verification_format_correct():
    assert affichage.verifier_format_ok(TEXTE_FORMAT_OK1)
    assert affichage.verifier_format_ok(TEXTE_FORMAT_OK2)
    assert affichage.verifier_format_ok(TEXTE_FORMAT_OK3)
    # 2 entités (ex : "+ 4") : format admis pour réutiliser le résultat précédent
    assert affichage.verifier_format_ok(TEXTE_FORMAT_STR0.strip())


@pytest.mark.parametrize("texte", [TEXTE_FORMAT_STR1, TEXTE_FORMAT_STR2, TEXTE_FORMAT_STR3])
def test_affichage_verification_format_non_correct(texte):
    with pytest.raises(CommunException):
        affichage.verifier_format_ok(texte)
