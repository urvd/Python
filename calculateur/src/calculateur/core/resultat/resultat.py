from dataclasses import dataclass


@dataclass(frozen=True)
class Resultat:
    valeur: float
    sauvegarde: bool
