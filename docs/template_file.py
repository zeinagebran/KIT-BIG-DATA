"""<Description courte>.

<description longue ...>

#Pour un module :
Classes:
    ...

Functions:
    ...
Vérification de code : python -m pylama -l all --pydocstyle-convention pep257 *.py
"""
__authors__ = ('Prénom Nom', 'Prénom Nom')
__date__ = '04/10/2024'
__version__ = '0.1'

###############################################################################
# IMPORTS :

# """/* Standard includes. */"""
import os
import sys

# """/* Extern modules */"""
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# import seaborn as sns

# """/* Intern modules */"""
# import my_package

###############################################################################
# CONSTANTES :

NBARG_MIN = 1  # nombre minimun d'arguments pris par le programme
NBARG_MAX = 2  # nombre maximum d'arguments pris par le programme
NBARG_INFINI = False
# Exit values define
EXIT_OK = 0
EXIT_BAD_ARG_FEW = -1
EXIT_BAD_ARG_TOO = -2
# define EXIT_BAD_OPEN_FILE_R    -3


###############################################################################
# FONCTIONS :

def myfonction():
    """exemple si un seul fichier, sinon, classe dans autre fichier."""
    return None


"""------------------------------------------------------------------------------------------"""
# --- Fonctions spécifiques pour l'entrée d'un programme ---------------------


def asking_help(s: str) -> bool:
    """Vérifie si l'utilisateur demande de l'aide.

    :param str s: argument du programme
    :return bool: Vrai si aide demandé
    """
    if len(s) <= 2:
        return False
    # end if
    if s[0] == '-' or s[0] == '/':
        if s[1:] in ('?', 'help', 'aide'):
            return True
        # end if
    # end if
    return False
# end def asking_help


def print_help() -> None:
    """Affiche l'aide."""
    name = os.path.basename(sys.argv[0])
    print(f'{name} [<JSON_path> <CSV_path> <OSH_path> <templates_path> '
          '<param_file.json>] [--action=x[,y]]\n'
          '\t JSON_path\t[défaut=JSON] dossier IN des JSON, doit exister\n'
          '\t CSV_path\t[défaut=CSV] dossier OUT futur des CSV\n'
          '\t OSH_path\t[défaut=OSH] dossier OUT futur des OSH\n'
          '\t templates_path\t[défaut=JSON/_template] dossier IN des templates des JSON, doit exister\n'
          '\t param_file\t[défaut=param_file.json] fichier IN de configuration des JSON pour OSH\n'
          '\t --action=x,...\t [défaut=all] nombre qui spécifie la ou les actions (séparé par une virgule) à exécuter\n'
          '\t\tall = exécution de toutes les actions du programme\n'
          '\t\t1 = ACTION 1 : suppression du contenu du répertoire CSV sauf dataExterne\n'
          '\t\t2 = ACTION 2 : normalisation des JSON (remplacer sicl par sicl2)\n'
          '\t\t3 = ACTION 3 : exécution du module json_to_csv (convertion des JSON en CSV)\n'
          '\t\t4 = ACTION 4 : exécution du module dqm_csv_create_osh (création des OSH et du schéma SQL)\n'
          '\t\t5 = ACTION 5 : exécution du script spécifique SICLADE (création SQL pour les timestamp)\n'
          '\t\texemple : --action=1,3,5 / --action=all\n')
# end def print_help


def run_process() -> int:
    """Fonction principale de l'algorithme.

    :return None
    """
    # Code d'erreur par défaut
    return_code = EXIT_OK

    # du code
    myfonction()

    return return_code
# end def run_process


def main() -> int:
    """Entrée du module.

    Gestion des arguments puis lancement du programme central.

    :return int: Code de retour du programme.
    """
    return_code: int = EXIT_OK

    # Vérification des arguments
    if len(sys.argv) < NBARG_MIN:
        print('Nombre d\'argument insuffisant:\n', file=sys.stderr)
        return_code = EXIT_BAD_ARG_FEW
    # end if
    if not NBARG_INFINI and len(sys.argv) >= NBARG_MAX:
        print('Nombre d\'argument insuffisant:\n', file=sys.stderr)
        return_code = EXIT_BAD_ARG_TOO
    # end if

    if return_code != EXIT_OK or asking_help(sys.argv[1]) is True:
        print_help()
    else:
        return_code = run_process()
    # end if

    return return_code
# end def main


###############################################################################

if __name__ == '__main__':
    print(sys.argv)
    sys.exit(main())
# end if
