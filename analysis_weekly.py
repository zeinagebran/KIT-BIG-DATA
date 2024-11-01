import streamlit as st
from functions import DataExtractor, WeeklyAnalysis

from config import Config

class weekly_analysis_module:
    def __init__(self, interactions_df, cfg: Config):
        self.cfg = cfg
        self.interactions_df = interactions_df

    def run(self):
        st.title("Weekly User Interaction Analysis")
        st.markdown("Analyze user interactions based on the day of the week.")

        # Initialize WeeklyAnalysis
        weekly_analysis = WeeklyAnalysis(self.interactions_df)

        # Add a toggle to view the average or a specific year
        view_avg = st.checkbox("Show Average Interactions Across All Years")

        if view_avg:
            # Show average interactions across all years
            fig = weekly_analysis.plot_mean_interactions()
            st.pyplot(fig)
        else:
            # Dropdown to select the year
            years_available = sorted(self.interactions_df['year'].unique())
            selected_year = st.selectbox(
                "Select the Year", options=years_available)

            # Automatically update the plot for the selected year
            fig = weekly_analysis.plot_interactions_for_year(selected_year)
            st.pyplot(fig)
