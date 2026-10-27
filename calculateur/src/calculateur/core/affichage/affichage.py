import logging

from calculateur.core.action.action_type import ActionType
from calculateur.core.affichage.i_affichage import IAffichage
from calculateur.core.commun.erreur.commun_exception import CommunException
from calculateur.core.commun.erreur.error_type import ErrorType
from calculateur.core.commun.format_utils import decouper

log = logging.getLogger(__name__)


class Affichage(IAffichage):

    def commencer(self) -> None:
        log.info("=== Calculateur ===")
        log.info("Saisissez une opération (ex : 3 + 4), ou 'q' pour quitter ou 'r' "
                 "pour reutilisé le resultat dans un calcul.")
        log.info("choisir l'operande parmis : '+', '-', 'x,', '/'")

    def terminer(self) -> None:
        log.info("Fin du calcul ! Fin du programme !")

    def afficher(self, texte: str) -> None:
        log.info(texte)

    def verifier_action_user(self, ligne: str) -> ActionType:
        # Vérifier le caractère d'annulation.
        match ligne.lower():
            case "q":
                return ActionType.QUITTER
            case "s" | "r":
                return ActionType.RE_CALCULER
            case _:
                return ActionType.CALCULER

    def verifier_format_ok(self, ligne: str) -> bool:
        try:
            parties = decouper(ligne)
            if len(parties) in (2, 3):
                return True
            raise ValueError(f"Format incorrect : {ligne}")
        except (ValueError, IndexError) as e:
            raise CommunException(ErrorType.FORMAT_ERROR, e) from e
