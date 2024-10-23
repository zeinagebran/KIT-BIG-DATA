import streamlit as st
from functions import DataExtractor, SeasonalityAnalysis


def show_seasonality_analysis():
    st.title("Seasonality Analysis of User Interactions")
    st.markdown("Study user interactions by month and season.")

    zip_file_path = "C:\\Users\\User\\Desktop\\MASTERE SPECIALISE IA\\KIT BIG DATA BGDIA700\\RESOURCES PROJET\\archive.zip"
    data_extractor = DataExtractor(zip_file_path)
    interactions_df, _ = data_extractor.extract_and_load_data()

    seasonality_analysis = SeasonalityAnalysis(interactions_df)
    fig = seasonality_analysis.plot_seasonality()
    st.pyplot(fig)
