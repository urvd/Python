import re

from calculateur.core.commun.erreur.commun_exception import CommunException
from calculateur.core.commun.erreur.error_type import ErrorType

_ESPACES = re.compile(r"\s+")


def convertir_en_nombre(texte: str) -> float:
    """Convertit un texte en nombre (équivalent de Double.parseDouble)."""
    try:
        # float() accepte « 1_000 », Double.parseDouble non : on le refuse aussi.
        if "_" in texte:
            raise ValueError(f"nombre invalide : {texte!r}")
        return float(texte)
    except ValueError as e:
        raise CommunException(ErrorType.NUMBER_FORMAT_ERROR, e) from e


def decouper(texte: str) -> list[str]:
    """Découpe sur les espaces comme String.split("\\s+") en Java."""
    parties = _ESPACES.split(texte)
    while len(parties) > 1 and parties[-1] == "":
        parties.pop()
    return parties
