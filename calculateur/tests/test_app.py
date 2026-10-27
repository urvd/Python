"""Test de bout en bout : simule une saisie utilisateur et lit l'affichage
(les logs sont écrits sur sys.stderr)."""
import io

import pytest

from calculateur.app import main


@pytest.fixture
def lancer(monkeypatch, capsys):
    def _lancer(saisie: str) -> str:
        monkeypatch.setattr("sys.stdin", io.StringIO(saisie))
        main([])
        return capsys.readouterr().err
    return _lancer


def test_recalculer_avec_r(lancer):
    affichage = lancer("2 + 3\nr\n+ 4\nq\n")

    assert "Format de saisie incorrect" not in affichage
    assert "Saisir (5.0) >" in affichage
    assert "Resultat =  {9.0}" in affichage


def test_recalculer_avec_s(lancer):
    affichage = lancer("2 + 3\ns\n* 2\nq\n")

    assert "Format de saisie incorrect" not in affichage
    assert "Saisir (5.0) >" in affichage
    assert "Resultat =  {10.0}" in affichage


def test_format_incorrect(lancer):
    affichage = lancer("2\nq\n")

    assert "Format de saisie incorrect" in affichage


def test_fin_de_saisie_sans_quitter(lancer):
    affichage = lancer("2 + 3\n")

    assert "Resultat =  {5.0}" in affichage
    assert "Fin du programme" in affichage
