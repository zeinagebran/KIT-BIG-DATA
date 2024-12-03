"""optimRecipes/analysis_seasonality.py file.

Sub-module Streamlit for page seasonality_analysis.

"""
###############################################################################
# IMPORTS :
# /* Standard includes. */
# /* Extern modules */
import streamlit as st

# /* Intern modules */
from functions import SeasonalityAnalysis


###############################################################################
# CLASS :
class seasonality_analysis_module:
    """Manage streamlit page for most_common_words."""

    def __init__(self, interactions_df, log_module, cfg):
        """Initialize seasonality_analysis_module."""
        self.cfg = cfg
        self.interactions_df = interactions_df
        self.log_module = log_module

    def run(self):
        """Run the module to display the analysis of seasonality."""
        self.log_module.log_info("Starting seasonality_analysis_module")

        st.title("🌦️ Seasonality Analysis of User Interactions")
        st.markdown("""
        ## 📅 Discover Monthly and Seasonal Trends!

        Ever wondered how user interactions fluctuate with the seasons? This section dives into monthly and seasonal patterns in user engagement, helping you uncover **when users are most active**. 📈

        ### Toggle Your View:
        - **Show Average Interactions**: View overall monthly and seasonal trends across all years.
        - **Select a Specific Year**: See how interactions vary in a particular year.

        ---
        """)

        # Initialize SeasonalityAnalysis
        seasonality_analysis = SeasonalityAnalysis(self.interactions_df)

        # Add a toggle to view the average or a specific year
        view_avg = st.checkbox("🌐 Show Average Interactions Across All Years")

        if view_avg:
            st.markdown("""
            ### 🌍 Average Seasonal Activity
            Here’s a look at the **average monthly and seasonal user interactions**. See if you can spot any recurring patterns throughout the year! 🌞🍂❄️🌸
            """)
            # Show average interactions across all years
            fig = seasonality_analysis.plot_seasonality()
            st.pyplot(fig)
        else:
            # Dropdown to select the year
            years_available = sorted(self.interactions_df['date'].dt.year.unique())
            selected_year = st.selectbox(
                "📅 Select a Year to Explore", options=years_available)

            st.markdown(f"""
            ### 🗓️ Monthly and Seasonal Activity for {selected_year}
            Let’s dive into the details of **{selected_year}** and explore how user interactions fluctuate each month and season. Does this year show any unique trends?
            """)
            # Automatically update the plot for the selected year
            fig = seasonality_analysis.plot_seasonality_for_year(selected_year)
            st.pyplot(fig)
