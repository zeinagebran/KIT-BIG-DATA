import streamlit as st
from functions import get_data, TopRecipesAnalysis

from config import Config

class top_50_analysis_module:
    def __init__(self, recipes_df, interactions_df, cfg: Config):
        self.cfg = cfg
        self.recipes_df = recipes_df
        self.interactions_df = interactions_df

    def run(self):
        st.title("Top 50 Most Popular Recipes")
        st.markdown(
            "Identify the recipes that users love the most based on ratings and comments."
        )

        top_recipes_analysis = TopRecipesAnalysis(self.recipes_df, self.interactions_df)
        # Modify the method to only return the top recipes and wordcloud figures
        top_recipes_analysis.display_popular_recipes_and_visualizations()
        # Remove fig and fig_wordcloud unpacking since they're not returned anymore
