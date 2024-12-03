"""Analysis of interaction throught time (nb recipes / nb reviews).

Analysis number of recipes or reviews by year/mouth

"""
__authors__ = 'Nicolas Allègre'
__date__ = '19/10/2024'
__version__ = '0.2'

###############################################################################
# IMPORTS :

# /* Standard includes. */
import datetime

# /* Extern modules */
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import streamlit as st

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
        (data[filename][row])
    :return (nb_by_year, nb_by_month): number of interaction by year/mouth in
        a dict[str, dict[int, int]] :
        nb_by_year: nb_by_year['filename'][year]: [int] = Count for the year
        nb_by_month: b_by_month['filename']['aaaa-mm']: [int] = Count for the mouth of a year
    """
    nb_by_year: dict[str, dict[int, int]] = {}
    nb_by_month: dict[str, dict[str, int]] = {}

    j_date_col = {DATA_FILES[0]: 2, DATA_FILES[1]: 4}
    for filename in DATA_FILES:
        nb_by_year[filename] = {}
        nb_by_month[filename] = {}
        j = j_date_col[filename]
        for i, row in enumerate(data[filename]):
            if i == 0:  # Pas de traitement sur les headers
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


def plot_matplotlib_version(nb_by_year, nb_by_month, show=True) -> any:
    """Version with matplotlib to print.

    Create visualisation for evolution recipes and interactions throug time.

    :param nb_by_year: count by year of recipes and interactions
    :param nb_by_mouth: count by mouth of each year of recipes and interactions
    :param show: for show graphical or not (Default True)
    :return matplotlib.figure.Figure: return matplotlib figure
    """
    plt_color = {DATA_FILES[0]: 'g', DATA_FILES[1]: 'b'}
    plt_label = {DATA_FILES[0]: 'NB review', DATA_FILES[1]: 'NB recipe'}
    fig_type = ['year', 'mouth']
    courbes = {'year': nb_by_year, 'mouth': nb_by_month}

    plt.close('all')
    fig = plt.figure()
    fig.suptitle('Nb recette et review')
    for i, graph in enumerate(fig_type):
        ax = fig.add_subplot(2, 1, i + 1)
        ax.set_title(f'Granularité : par {graph}')
        ax.set_xlabel('Temps')

        filename = DATA_FILES[0]
        x = list(courbes[graph][filename].keys())
        y = list(courbes[graph][filename].values())
        color = plt_color[filename]
        ax.set_ylabel(plt_label[filename], color=color)
        line_rev, = ax.plot(x, y, '-', color=color, label=f'{plt_label[filename]}')
        ax.tick_params(axis='y', labelcolor=color)

        filename = DATA_FILES[1]
        x = list(courbes[graph][filename].keys())
        y = list(courbes[graph][filename].values())
        color = plt_color[filename]
        ax2 = ax.twinx()  # instantiate a second Axes that shares the same x-axis
        ax2.set_ylabel(plt_label[filename], color=color)
        line_rec, = ax2.plot(x, y, '-', color=color, label=f'{plt_label[filename]}')
        ax2.tick_params(axis='y', labelcolor=color)

        ax.set_xticks(x)
        for label in ax.get_xticklabels():
            label.set_rotation(60)
            label.set_horizontalalignment('right')

        if graph == fig_type[1]:
            id_label = ax2.get_xticks()
            text_label = ax2.get_xticklabels()
            new_id_label = [x.get_position()[0]
                            for x in text_label if x.get_text().split('-')[1] == '01']
            new_id_label.append(id_label[-1])
            ax2.xaxis.set_major_locator(ticker.FixedLocator(new_id_label))

        ax.yaxis.set_major_locator(ticker.MaxNLocator(4))
        ax2.yaxis.set_major_locator(ticker.MaxNLocator(4))

    fig.legend(handles=[line_rev, line_rec])
    fig.tight_layout()
    if show is True:
        plt.show()

    return fig


class temporality_analysis_module:
    """Class to wrap this module functions to interact with webapp.

    This class is used by webapp streamlit for the analysis of interaction
    throught time (nb recipes / nb reviews) and construct the page and graphs.
    """

    def __init__(self, recipes_df, interactions_df):
        """Initialise the class with data.

        :param pandas.DataFrame recipes_df: data for the recipes
        :param pandas.DataFrame interactions_df: data for the recipes
        """
        self.recipes_df = recipes_df
        self.interactions_df = interactions_df

    def run(self):
        """Build analysis, and print result on a web streamlit page."""
        st.title("Evolution of recipes and actions over time")
        st.markdown(
            """
            ## 🌟 Discover temporality of recipes and actions over time!
            Here, we showcase the evolution over time of our original data from website Food.com :
            - Evolution throught time for recipe creation
            - Evolution throught time for interaction in recipes
            """
        )

        # TODO transforme to list or manipulate DataFrame
        data = {DATA_FILES[0]: self.interactions_df, DATA_FILES[1]: self.recipes_df}
        nb_by_year, nb_by_month = analysis_temporelle(data)
        fig = plot_matplotlib_version(nb_by_year, nb_by_month, show=False)
        st.pyplot(fig)
