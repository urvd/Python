from enum import Enum


class OperateurType(Enum):
    ADDITION = "+"
    SOUSTRACTION = "-"
    MULTIPLICATION = "*"
    MULTIPLICATION_X = "x"
    DIVISION = "/"
    NOT_AN_OPERATEUR = ""

    @property
    def symbole(self) -> str:
        return self.value

    @classmethod
    def recherche_operateur(cls, symbole: str) -> "OperateurType":
        for operateur in cls:
            if operateur.symbole == symbole:
                return operateur
        return cls.NOT_AN_OPERATEUR
