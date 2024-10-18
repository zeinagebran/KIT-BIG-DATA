# analysis_weekly.py
import streamlit as st
from functions import extract_and_load_data, plot_mean_interactions


def show_weekly_analysis():
    st.title("Weekly User Interaction Analysis")
    st.markdown("""
    In this analysis, we examine user interactions based on the day of the week. This helps us understand which days users are most active so we can adjust our publishing strategy and maximize engagement.
    """)
    zip_file_path = "C:\\Users\\User\\Desktop\\MASTERE SPECIALISE IA\\KIT BIG DATA BGDIA700\\RESOURCES PROJET\\archive.zip"
    interactions_df = extract_and_load_data(zip_file_path)
    fig = plot_mean_interactions(interactions_df)
    st.pyplot(fig)
