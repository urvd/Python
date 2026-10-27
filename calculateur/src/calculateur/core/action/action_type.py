from enum import Enum


class ActionType(Enum):
    INITIALISATION = "i"
    CALCULER = "c"
    RE_CALCULER = "r"
    SAUVEGUARDER = "s"
    QUITTER = "q"

    @property
    def action(self) -> str:
        return self.value
