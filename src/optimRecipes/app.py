import streamlit as st
from analysis_weekly import weekly_analysis_module
from analysis_seasonality import seasonality_analysis_module
from top_50_analysis import top_50_analysis_module
from most_common_words import most_common_words_module
from logger import Logger
from config import *
import pyrallis
from functions import DataExtractor


class WebApp:
    def __init__(self, cfg: Config):
        # setup home page
        self.setup_home_page()

        # Load data and initialize logger
        self.cfg = cfg
        self.zip_file_path = cfg.zip_file_path
        self.interactions_df, self.recipes_df = self.load_data()
        self.logger = Logger(cfg=cfg)

        # Initialize modules
        self.seasonality_analysis_module = seasonality_analysis_module(
            self.interactions_df, cfg)
        self.top_50_analysis_module = top_50_analysis_module(
            self.recipes_df, self.interactions_df, cfg)
        self.weekly_analysis_module = weekly_analysis_module(
            self.interactions_df, cfg)
        self.most_common_words_module = most_common_words_module(
            self.recipes_df, self.interactions_df, cfg)

    def load_data(self):
        Logger.log_info("Extracting data")
        # Load the interactions data
        data_extractor = DataExtractor(self.zip_file_path)
        interactions_df, recipes_df = data_extractor.extract_and_load_data()
        return interactions_df, recipes_df

    def setup_home_page(self):
        # Set page configuration
        st.set_page_config(page_title="Enhancing User Interaction",
                           page_icon="📊", layout="centered")
        # Sidebar for navigation
        st.sidebar.title("Navigation")
        self.section = st.sidebar.selectbox("Choose a section:", [
            "Home",
            "Weekly Interaction Analysis",
            "Seasonality Analysis",
            "Top 50 Most Popular Recipes Based on Ratings and Comments",
            "Most common words"
        ])

    def run(self):
        # Home Page
        if self.section == "Home":
            st.title("How to Improve User Interaction in Our Company")
            st.markdown("""
            Welcome to our **home page** dedicated to improving **user interactions**.
            Here are the analysis sections covered:
            """)
            st.markdown("""
            ### Analysis Sections:
            1. **Weekly User Interaction Analysis**: Understand when users are most active.
            2. **Top 50 Most Popular Recipes**: Explore the recipes that generate the most interest.
            3. **Characteristics of the Top Recipes**: Analyze features such as preparation time.
            4. **Most Frequent Words in Recipe Titles**: Identify trends in recipe titles.
            5. **Seasonality Analysis**: Analyze user interactions by month and season.
            """)

        # Weekly Interaction Analysis Page
        elif self.section == "Weekly Interaction Analysis":
            self.weekly_analysis_module.run()

        # Seasonality Analysis Page
        elif self.section == "Seasonality Analysis":
            self.seasonality_analysis_module.run()

        # Top Recipes Analysis Page
        elif self.section == "Top 50 Most Popular Recipes Based on Ratings and Comments":
            self.top_50_analysis_module.run()

        # Show most frequent words appearing in recipe titles
        elif self.section == "Most common words":
            self.most_common_words_module.run()

        # Footer
        st.markdown("---\nUse the sidebar to navigate through the analysis.")
