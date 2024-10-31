import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from functions import DataExtractor, WeeklyAnalysis


def show_weekly_analysis():
    st.title("Weekly User Interaction Analysis")
    st.markdown("Analyze user interactions based on the day of the week. Choose a year to see interactions for that specific year or view average interactions across all years.")

    # Load data
    zip_file_path = "C:\\Users\\User\\Desktop\\MASTERE SPECIALISE IA\\KIT BIG DATA BGDIA700\\RESOURCES PROJET\\archive.zip"
    data_extractor = DataExtractor(zip_file_path)
    interactions_df, _ = data_extractor.extract_and_load_data()

    # Initialize WeeklyAnalysis
    weekly_analysis = WeeklyAnalysis(interactions_df)

    # Add a toggle to view the average or a specific year
    view_avg = st.checkbox("Show Average Interactions Across All Years")

    if view_avg:
        # Show average interactions across all years
        fig = weekly_analysis.plot_mean_interactions()
        st.pyplot(fig)
    else:
        # Dropdown to select the year
        years_available = sorted(interactions_df['year'].unique())
        selected_year = st.selectbox(
            "Select the Year", options=years_available)

        # Automatically update the plot for the selected year
        fig = weekly_analysis.plot_interactions_for_year(selected_year)
        st.pyplot(fig)
