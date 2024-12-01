import streamlit as st
import pyrallis
import matplotlib.pyplot as plt

from functions import CommonWordsAnalysis
from config import Config
#from optimRecipes.config import Config


from logger import Logger


class most_common_words_module:
    def __init__(self, recipes_df, interactions_df, cfg: Config):
        """
        Initializes the MostCommonWordsModule with the given DataFrames and configuration.

        Args:
            recipes_df (pd.DataFrame): DataFrame containing recipe data.
            interactions_df (pd.DataFrame): DataFrame containing interactions data.
            cfg (Config): Configuration object with filtering and display parameters.
        """
        self.cfg = cfg
        self.recipes_df = recipes_df
        self.interactions_df = interactions_df

        # Setup parameters from configuration
        self.min_rating = cfg.min_rating
        self.min_num_ratings = cfg.min_num_ratings
        self.num_top_recipes = cfg.num_top_recipes
        self.min_year = cfg.min_year
        self.max_year = cfg.max_year

    def run(self):
        """
        Runs the module to display the most common words in popular recipes by year.
        """
        # Page title and introduction
        st.title("📜 Most Common Words in Popular Recipes")
        st.markdown("""
        Welcome to the **Most Common Words Analysis**! 🎉
        Here, you can explore the most popular words found in user-posted TOP recipe titles for any chosen year.
        This helps us understand what keywords make recipes appealing and trendy. 📈🍲
        """)

        # Year selection for analysis
        st.markdown("### 📅 Select the Year")
        year = st.selectbox("Choose a year to analyze:", [str(
            i) for i in range(self.min_year, self.max_year)])
        year = int(year)

        # Button to display the word cloud
        if st.button('🔍 Display Word Cloud'):
            with st.spinner(f"Analyzing the most common words in popular recipes for {year}..."):
                # Perform common words analysis
                cw_analysis = CommonWordsAnalysis(
                    self.recipes_df, self.interactions_df, self.cfg)
                cw_analysis.format_recipe(year)
                word_cloud = cw_analysis.compute_top_keywords()

                # Display word cloud
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.imshow(word_cloud, interpolation='bilinear')
                ax.axis("off")
                st.pyplot(fig)
                st.success("Word cloud generated successfully! 🌟")
