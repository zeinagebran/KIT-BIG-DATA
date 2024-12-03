import streamlit as st

from functions import TopRecipesAnalysis


class top_50_analysis_module:
    def __init__(self, recipes_df, interactions_df, log_module, cfg):
        self.cfg = cfg
        self.recipes_df = recipes_df
        self.interactions_df = interactions_df
        self.log_module = log_module

    def run(self):
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
