import streamlit as st
from functions import SeasonalityAnalysis

from optimRecipes.config import Config


class seasonality_analysis_module:
    def __init__(self, interactions_df, cfg: Config):
        self.cfg = cfg
        self.interactions_df = interactions_df

    def run(self):
        st.title("Seasonality Analysis of User Interactions")
        st.markdown("Study user interactions by month and season.")

        # Initialize SeasonalityAnalysis
        seasonality_analysis = SeasonalityAnalysis(self.interactions_df)
        # Add a toggle to view the average or a specific year
        view_avg = st.checkbox("Show Average Interactions Across All Years")

        if view_avg:
            # Show average interactions across all years
            fig = seasonality_analysis.plot_seasonality()
            st.pyplot(fig)
        else:
            # Dropdown to select the year
            years_available = sorted(
                self.interactions_df['date'].dt.year.unique())
            selected_year = st.selectbox(
                "Select the Year", options=years_available)

            # Automatically update the plot for the selected year
            fig = seasonality_analysis.plot_seasonality_for_year(selected_year)
            st.pyplot(fig)
