import pytest

from calculateur.core.commun.erreur.commun_exception import CommunException
from calculateur.core.commun.erreur.error_type import ErrorType
from calculateur.core.commun.format_utils import convertir_en_nombre


@pytest.mark.parametrize("texte, attendu", [
    ("42", 42),          # entier
    ("3.5", 3.5),        # décimal
    ("-7", -7),          # négatif
    ("0", 0),            # zéro
    ("1.5e3", 1500),     # notation scientifique
    (" 12 ", 12),        # espaces autour
])
def test_convertir(texte, attendu):
    assert convertir_en_nombre(texte) == attendu


# Exception centralisée
# Test : les saisies non numériques donnent une NUMBER_FORMAT_ERROR.
@pytest.mark.parametrize("texte", ["abc", "3,5", "+", "", "1_000"])
def test_saisie_non_numerique(texte):
    with pytest.raises(CommunException) as exc:
        convertir_en_nombre(texte)
    assert exc.value.error_type == ErrorType.NUMBER_FORMAT_ERROR


def test_texte_none():
    """Comportement actuel : None n'est pas converti en CommunException,
    l'erreur native remonte telle quelle (NullPointerException en Java)."""
    with pytest.raises(TypeError):
        convertir_en_nombre(None)
