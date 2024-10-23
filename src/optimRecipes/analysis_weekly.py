import streamlit as st
from functions import DataExtractor, WeeklyAnalysis


def show_weekly_analysis():
    st.title("Weekly User Interaction Analysis")
    st.markdown("Analyze user interactions based on the day of the week.")

    zip_file_path = "C:\\Users\\User\\Desktop\\MASTERE SPECIALISE IA\\KIT BIG DATA BGDIA700\\RESOURCES PROJET\\archive.zip"
    data_extractor = DataExtractor(zip_file_path)
    interactions_df, _ = data_extractor.extract_and_load_data()

    weekly_analysis = WeeklyAnalysis(interactions_df)
    fig = weekly_analysis.plot_mean_interactions()
    st.pyplot(fig)
