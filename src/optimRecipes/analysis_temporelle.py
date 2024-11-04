"""Analysis of interaction throug time (nb recipes / nb reviews).

Analysis number of recipes or reviews by year/mouth

"""
__authors__ = 'Nicolas Allègre'
__date__ = '19/10/2024'
__version__ = '0.1'

###############################################################################
# IMPORTS :

# /* Standard includes. */
import datetime

# /* Extern modules */
import matplotlib.pyplot as plt

# /* Intern modules */

###############################################################################
# CONSTANTES :
EXIT_OK = 0
DATA_FILES = ['RAW_interactions.csv', 'RAW_recipes.csv']


###############################################################################
# FONCTIONS :
def analysis_temporelle(data: dict[str, list[str]]) -> tuple[dict[str, dict[int, int]], dict[str, dict[str, int]]]:
    """Analyse the data and calculate sum of interaction by year and mouth.

    :param dict(str, list[str]) data: data loaded for each file
        data[filename][row]
    :return (nb_by_year, nb_by_year), dict(str, dict(str, int)): return
        number of interaction by year and by mouth for all data.
        nb_by_year: dict[str, dict[int, int]]
            nb_by_year['filename'] = object for the file
            nb_by_year['filename'][year]: [int] = Count for the year
        nb_by_month: dict[str, dict[int, int]]
            nb_by_month['filename'] = object for the file
            nb_by_month['filename']['aaaa-mm']: [int] = Count for the mouth of a year
    """
    nb_by_year: dict[str, dict[int, int]] = {}
    nb_by_month: dict[str, dict[str, int]] = {}
    for filename in DATA_FILES:
        nb_by_year[filename] = {}
        nb_by_month[filename] = {}

    j_date_col = {DATA_FILES[0]: 2, DATA_FILES[1]: 4}
    for filename in DATA_FILES:
        j = j_date_col[filename]
        for i, row in enumerate(data[filename]):
            if i == 0:  # Pas sur les header
                continue
            col = row[j]
            tmp = col.split('-')
            d = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
            if d.year in nb_by_year[filename].keys():
                nb_by_year[filename][d.year] += 1
            else:  # Initialisation
                nb_by_year[filename][d.year] = 1
            month = f'{d.year}-{d.month:02}'
            if month in nb_by_month[filename].keys():
                nb_by_month[filename][month] += 1
            else:  # Initialisation
                nb_by_month[filename][month] = 1

        for x in range(1999, 2019):
            if x not in nb_by_year[filename].keys():
                nb_by_year[filename][x] = 0
            for y in range(1, 13):
                mois = f'{y:02}'
                tmp_s = f'{x}-{mois}'
                if tmp_s not in nb_by_month[filename].keys():
                    nb_by_month[filename][tmp_s] = 0

        nb_by_year[filename] = dict(sorted(nb_by_year[filename].items()))
        nb_by_month[filename] = dict(sorted(nb_by_month[filename].items()))

    return nb_by_year, nb_by_month


def plot_matplotlib_version(nb_by_year, nb_by_month) -> None:
    """Version with matplotlib to print."""

    plt.close('all')
    fig = plt.figure()
    fig.suptitle('Nb recette et review')
    plt_color = {DATA_FILES[0]: 'g', DATA_FILES[1]: 'b'}
    # Par an :
    ax1 = fig.add_subplot(2, 1, 1)
    for filename in DATA_FILES:
        print(list(nb_by_year[filename].keys()))
        ax1.plot(list(nb_by_year[filename].keys()),
                 list(nb_by_year[filename].values()), '-',
                 color=plt_color[filename], label=f'{filename}')
    ax1.set_xlabel('Année')
    ax1.set_ylabel('NB')
    ax1.set_title('Par année')
    ax1.set_xticks(list(nb_by_year[filename].keys()))
    for label in ax1.get_xticklabels():
        label.set_rotation(40)
        label.set_horizontalalignment('right')
    ax1.legend()

    # Par an :
    ax2 = fig.add_subplot(2, 1, 2)
    for filename in DATA_FILES:
        ax2.plot(list(nb_by_month[filename].keys()),
                 list(nb_by_month[filename].values()), '-',
                 color=plt_color[filename], label=f'{filename}')
    ax2.set_xlabel('Mois')
    ax2.set_ylabel('NB')
    ax2.set_title('Par mois')

    # fig.legend()
    fig.tight_layout()
    plt.show()
