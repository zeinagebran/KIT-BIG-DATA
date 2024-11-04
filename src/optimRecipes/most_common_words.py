import streamlit as st
import pyrallis
import matplotlib.pyplot as plt

from functions import CommonWordsAnalysis
from config import Config
from logger import Logger


class most_common_words_module:
    def __init__(self, recipes_df, interactions_df, cfg: Config):
        self.cfg = cfg
        self.recipes_df = recipes_df
        self.interactions_df = interactions_df
        # Setup parameters
        self.min_rating = cfg.min_rating
        self.min_num_ratings = cfg.min_num_ratings
        self.num_top_recipes = cfg.num_top_recipes
        self.min_year = cfg.min_year
        self.max_year = cfg.max_year

    def run(self):
        # Title for the page
        st.title("Most common words found in user posted recipes")
        st.markdown("""
        For a given year, we identify the most common words found in the titles of popular recipes posted by users during that year. This helps in figuring out which keywords help make a recipe popular.
        """)

        #Year selection
        st.markdown(""" Select the year """)
        section = st.selectbox("Choose a section:", [str(i) for i in list(range(self.min_year, self.max_year))])
        year = int(section)

        if st.button('Display the wordcloud'):
            with st.spinner(f"Computing the most common words found in successful recipes in {year}"):
                cw_analysis = CommonWordsAnalysis(self.recipes_df, self.interactions_df, self.cfg)
                cw_analysis.format_recipe(year)
                wc = cw_analysis.compute_top_keywords()
                fig, ax = plt.subplots(1)
                ax = plt.imshow(wc, interpolation='bilinear')
                plt.axis("off")
                st.pyplot(fig)

