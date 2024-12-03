"""optimRecipes/analysis_top_15.py file.

Sub-module Streamlit for page top_50_analysis.

"""
###############################################################################
# IMPORTS :
# /* Standard includes. */
# /* Extern modules */
import streamlit as st

# /* Intern modules */
from functions import TopRecipesAnalysis


###############################################################################
# CLASS :
class top_50_analysis_module:
    """Class to wrap this module functions to interact with webapp.

    This class is used by webapp streamlit for the analysis of the most popularity
    recipes.
    """

    def __init__(self, recipes_df, interactions_df, log_module, cfg):
        """Initialize the class with the data."""
        self.cfg = cfg
        self.recipes_df = recipes_df
        self.interactions_df = interactions_df
        self.log_module = log_module

    def run(self):
        """Build analysis, and print result on a web streamlit page."""
        st.title("🍲 Top 15 Most Popular Recipes")
        st.markdown(
            """
            ## 🌟 Discover the User Favorites!
            Here, we showcase the recipes that have captured users' hearts. This analysis is based on **ratings** and **comments**, allowing you to explore:
            - 🍴 Recipes with the highest popularity over the years
            - 🎉 Top recipes for specific time periods
            """
        )

        self.log_module.log_info("Starting top_50_analysis_module")
        # Initialize the analysis
        top_recipes_analysis = TopRecipesAnalysis(self.recipes_df, self.interactions_df)
        top_recipes_analysis.display_popular_recipes_and_visualizations()
