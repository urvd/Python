# Object : Projet Python, pour simuler le comportement d'une calculatrice simple
> [!NOTE]
> ### Technos : Python 3.12.2, pytest.

Portage Python du projet Maven [calculateur](https://github.com/urvd/Java/tree/main/calculateur).

## Structure

```
calculateur/
├── pyproject.toml
├── src/calculateur/
│   ├── __main__.py                 # permet « python -m calculateur »
│   ├── app.py                      # point d'entrée (App.java)
│   └── core/
│       ├── action/action_type.py   # ActionType
│       ├── affichage/              # IAffichage, Affichage
│       ├── calcul/                 # ICalcul, Calculateur, OperateurType, Operation
│       ├── commun/format_utils.py  # FormatUtils
│       ├── commun/erreur/          # CommunException, ErrorType
│       └── resultat/resultat.py    # Resultat
└── tests/                          # mêmes tests que src/test/java
```

## Info utiles :

### Lancer un programme :

#### Exemple 1 :
* `cd calculateur`
* `python3.12 -m venv .venv && source .venv/bin/activate` (Windows : `.venv\Scripts\activate`)
* `pip install -e .`
* `calculateur` (ou `python -m calculateur`)

#### Exemple 2 (sans installation) :
* `cd calculateur`
* `PYTHONPATH=src python -m calculateur` (Windows PowerShell : `$env:PYTHONPATH="src"; python -m calculateur`)

#### Exemple 3 :
Depuis un éditeur comme VSCode ou PyCharm : lancer le module `calculateur.app`
avec des configurations si nécessaire (dossier source : `src`).

### Utilisation

```
Saisir >
2 + 3
Resultat =  {5.0}
Saisir >
r
Saisir (5.0) >
* 2
Resultat =  {10.0}
Saisir >
q
```

* `a op b` : calcule, opérateurs `+`, `-`, `*` ou `x`, `/`
* `r` ou `s` : la saisie suivante (`op b`) réutilise le résultat précédent
* `q` : quitter

### Lancer des tests et ouvrir les rapports sur un navigateur par défaut :

* `pip install -e ".[dev]"`
* `pytest`
* `pytest --cov=calculateur --cov-report=html`
* `open htmlcov/index.html`
