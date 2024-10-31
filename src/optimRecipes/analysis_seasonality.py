import streamlit as st
from functions import DataExtractor, SeasonalityAnalysis


def show_seasonality_analysis():
    st.title("Seasonality Analysis of User Interactions")
    st.markdown("Study user interactions by month and season. Choose a year to see interactions for that specific year or view average interactions across all years.")

    # Load data
    zip_file_path = "C:\\Users\\User\\Desktop\\MASTERE SPECIALISE IA\\KIT BIG DATA BGDIA700\\RESOURCES PROJET\\archive.zip"
    data_extractor = DataExtractor(zip_file_path)
    interactions_df, _ = data_extractor.extract_and_load_data()

    # Initialize SeasonalityAnalysis
    seasonality_analysis = SeasonalityAnalysis(interactions_df)

    # Add a toggle to view the average or a specific year
    view_avg = st.checkbox("Show Average Interactions Across All Years")

    if view_avg:
        # Show average interactions across all years
        fig = seasonality_analysis.plot_seasonality()
        st.pyplot(fig)
    else:
        # Dropdown to select the year
        years_available = sorted(interactions_df['date'].dt.year.unique())
        selected_year = st.selectbox(
            "Select the Year", options=years_available)

        # Automatically update the plot for the selected year
        fig = seasonality_analysis.plot_seasonality_for_year(selected_year)
        st.pyplot(fig)
