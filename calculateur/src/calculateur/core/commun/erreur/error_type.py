from enum import Enum


class ErrorType(Enum):
    FORMAT_ERROR = "Format de saisie incorrect"
    NUMBER_FORMAT_ERROR = "Erreur de format numérique !"
    ARITHMETIC_ERROR = "Erreur arithmétique !"
    ARRAY_INDEX_OUT_OF_BOUNDS_ERROR = "Saisie invalide !"
    ILLEGAL_ARGUMENT_ERROR = "Argument invalide !"
    UNDEFINED_ERROR = "Erreur indéfinie !"

    @property
    def message(self) -> str:
        return self.value
