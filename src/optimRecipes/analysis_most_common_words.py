"""optimRecipes/analysis_most_commun_words.py file.

Sub-module Streamlit for page most_common_words.

"""
###############################################################################
# IMPORTS :
# /* Standard includes. */
# /* Extern modules */
import streamlit as st

# /* Intern modules */
from functions import CommonWordsAnalysis, TopRecipesAnalysis


###############################################################################
# CLASS :
class most_common_words_module:
    """Class to wrap this module functions to interact with webapp.

    This class is used by webapp streamlit for the analysis of the most commun
    words throught the recipes and reviews.
    """

    def __init__(self, recipes_df, interactions_df, log_module, cfg):
        """
        Initialize the MostCommonWordsModule with the given DataFrames and configuration.

        Args:
            recipes_df (pd.DataFrame): DataFrame containing recipe data.
            interactions_df (pd.DataFrame): DataFrame containing interactions data.
            cfg (Config): Configuration object with filtering and display parameters.
        """
        self.cfg = cfg
        self.recipes_df = recipes_df
        self.interactions_df = interactions_df
        self.min_year = cfg.min_year
        self.max_year = cfg.max_year
        self.log_module = log_module
        self.top_recipes = None

    def run(self):
        """Build analysis, and print result on a web streamlit page."""
        self.log_module.log_info("Starting most_common_words_module")
        # Page title and introduction
        st.title("📜 Most Common Words in Popular Recipes")
        st.markdown("""
        Welcome to the **Most Common Words Analysis**! 🎉
        Here, you can explore the most popular words found in user-posted TOP recipe titles for any chosen year.
        This helps us understand what keywords make recipes appealing and trendy. 📈🍲
        """)

        # Year selection for analysis
        st.markdown("### 📅 Select the Year")
        section = st.selectbox("Choose a section:",
                               ["All"] + [str(i) for i in list(range(self.min_year, self.max_year))])
        if section != "All":
            year = int(section)
            self.recipes_df["submitted"] = self.recipes_df["submitted"].apply(lambda x: int(x[0:4]))
            self.recipes_df = self.recipes_df[self.recipes_df["submitted"] == year]

        self.top_recipes = TopRecipesAnalysis(self.recipes_df, self.interactions_df)

        # Button to display the word cloud
        if st.button('🔍 Display Word Cloud'):
            with st.spinner("Computing the most common words"):
                top_recipes_df = self.top_recipes.display_popular_recipes_and_visualizations(return_top_recipes=True, mcw_flag=True)
                cw_analysis = CommonWordsAnalysis(top_recipes_df)
                text = cw_analysis.compute_top_keywords()
                cw_analysis.display_wordcloud(text)
