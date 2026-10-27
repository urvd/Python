"""Point d'entrée : calculateur interactif en ligne de commande."""
import logging
import sys

from calculateur.core.action.action_type import ActionType
from calculateur.core.affichage.affichage import Affichage
from calculateur.core.affichage.i_affichage import IAffichage
from calculateur.core.calcul.calculateur import Calculateur
from calculateur.core.calcul.i_calcul import ICalcul
from calculateur.core.calcul.operateur_type import OperateurType
from calculateur.core.calcul.operation import Operation
from calculateur.core.commun.erreur.commun_exception import CommunException
from calculateur.core.commun.format_utils import convertir_en_nombre, decouper
from calculateur.core.resultat.resultat import Resultat


def configurer_logs() -> None:
    """Équivalent de slf4j-simple : niveau INFO, écriture sur stderr."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(threadName)s] %(levelname)s %(name)s - %(message)s",
        stream=sys.stderr,
        force=True,
    )


def main(args: list[str] | None = None) -> None:
    configurer_logs()
    calculateur: ICalcul = Calculateur()
    affichage: IAffichage = Affichage()
    current_action = ActionType.INITIALISATION
    resultat0 = Resultat(0.0, False)
    resultat_actual = Resultat(0.0, False)

    affichage.commencer()

    while current_action != ActionType.QUITTER:
        try:
            # 1er affichage avant saisie
            if current_action == ActionType.RE_CALCULER:
                affichage.afficher(f"Saisir ({resultat_actual.valeur}) >")
            else:
                if current_action == ActionType.INITIALISATION:
                    resultat_actual = resultat0
                affichage.afficher("Saisir > ")
            # Detection d'une saisie
            saisie = sys.stdin.readline()
            if not saisie:
                break
            ligne = saisie.strip()
            parties = decouper(ligne)
            affichage.afficher("[" + ", ".join(parties) + "]")
            # Vérification de l'action de l'utilisateur - cas d'annulation ou de recalcul
            current_action = affichage.verifier_action_user(ligne)
            if current_action == ActionType.QUITTER:
                break

            # 'r' ou 's' : pas de calcul, la prochaine saisie réutilise le résultat
            if current_action in (ActionType.SAUVEGUARDER, ActionType.RE_CALCULER):
                current_action = ActionType.RE_CALCULER
                continue

            if not affichage.verifier_format_ok(ligne):
                continue

            # Convertion en operation
            if len(parties) == 2:
                operation = _creer_operation_depuis(parties, resultat_actual.valeur)
            else:
                operation = _creer_operation(parties)

            # Calcul
            resultat_actual = calculateur.calculer(operation)

            affichage.afficher(f"Resultat =  {{{resultat_actual.valeur}}}")

        except CommunException as e:
            affichage.afficher(e.error_type.message)

    affichage.terminer()


def _creer_operation_depuis(parties: list[str], ex_valeur: float) -> Operation:
    return Operation(ex_valeur,
                     convertir_en_nombre(parties[1]),
                     OperateurType.recherche_operateur(parties[0]))


def _creer_operation(parties: list[str]) -> Operation:
    return Operation(convertir_en_nombre(parties[0]),
                     convertir_en_nombre(parties[2]),
                     OperateurType.recherche_operateur(parties[1]))


if __name__ == "__main__":
    main(sys.argv[1:])
