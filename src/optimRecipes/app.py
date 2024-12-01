import streamlit as st
from analysis_weekly import weekly_analysis_module
from analysis_seasonality import seasonality_analysis_module
from analysis_top_15 import top_50_analysis_module
from most_common_words import most_common_words_module
from logger import Logger
from config import Config
#from optimRecipes.config import Config

from functions import DataExtractor
import pyrallis

# Set page configuration
st.set_page_config(page_title="Enhancing User Interaction",
                   page_icon="📊", layout="centered")


class WebApp:
    def __init__(self, cfg: Config):
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

    def setup_navigation(self):
        # Sidebar for navigation with a dropdown selector for instant response
        st.sidebar.title("📍 Navigation")
        section = st.sidebar.selectbox(
            "Choose a section:",
            [
                "Home 🏠",
                "Weekly Interaction 📅",
                "Seasonality Analysis 🍂",
                "Top 15 Recipes ⭐",
                "Top Words 🔤"
            ],

        )
        return section

    def run(self):
        # Run navigation setup
        section = self.setup_navigation()

        # Home Page
        if section == "Home 🏠":
            st.title("Welcome to the Recipe Insights Hub! 🍲✨")

            st.markdown("""
            ## 👋 Hello, Data Enthusiast!

            We're here to help you **unlock the secrets** of user interactions in the world of recipes! Dive into our interactive analytics sections to see what makes a recipe popular, discover user behavior trends, and much more.

            ### 🌟 What's Cooking in This Dashboard?

            Here's a quick rundown of the tasty insights you'll find:

            1. **Weekly Interaction 📅**
            - **When are users most active?** Discover peak times and days when our community is buzzing with activity!

            2. **Top 15 Recipes ⭐**
            - **What's trending?** Uncover the most popular recipes based on ratings and comments.

            3. **Recipe Insights 🔍**
            - Get a deep dive into the **characteristics of top recipes**. Learn what makes these recipes stand out – from prep time to ingredients.

            4. **Top Words 🔤**
            - **Keyword Trends!** Identify the words that make recipes stand out, year by year. Who knew titles could be so revealing?

            5. **Seasonality 🍂**
            - **Year-round Flavor**: See how recipe interactions vary by month and season. What's popular in summer? What's cozy in winter?

            ---

            ### 🧭 How to Navigate?

            - Use the **sidebar on the left** to jump to any section you'd like.
            - **Explore** each analysis to gain insights and have fun along the way!

            Let's get cooking with some data! 🍳📊
            """)

        # Weekly Interaction Analysis Page
        elif section == "Weekly Interaction 📅":
            self.weekly_analysis_module.run()

        # Seasonality Analysis Page
        elif section == "Seasonality Analysis 🍂":
            self.seasonality_analysis_module.run()

        # Top Recipes Analysis Page
        elif section == "Top 15 Recipes ⭐":
            self.top_50_analysis_module.run()

        # Show most frequent words appearing in recipe titles
        elif section == "Top Words 🔤":
            self.most_common_words_module.run()

        # Footer
        st.markdown("---\nUse the sidebar to navigate through the analysis.")


# Entry-point with pyrallis wrapper
if __name__ == '__main__':
    import sys
    from optimRecipes.config import Config

    # pyrallis automatically wraps main() with the configuration
    @pyrallis.wrap()
    def main(cfg: Config):
        app = WebApp(cfg)
        app.run()

    main()
