# analysis_seasonality.py
import streamlit as st
from functions import extract_and_load_data, plot_seasonality


def show_seasonality_analysis():
    # Title for the page
    st.title("Seasonality Analysis of User Interactions")
    st.markdown("""
    In this analysis, we study user interactions by month and season. This analysis allows us to identify trends and activity peaks during certain periods of the year.
    """)

    # Path to the ZIP file
    zip_file_path = "C:\\Users\\User\\Desktop\\MASTERE SPECIALISE IA\\KIT BIG DATA BGDIA700\\RESOURCES PROJET\\archive.zip"

    # Load the interactions data
    try:
        interactions_df = extract_and_load_data(zip_file_path)
        fig = plot_seasonality(interactions_df)

        # Display the plot
        st.pyplot(fig)

        # Optional: Display a note about findings
        st.markdown("""
        **Note:** This analysis helps to pinpoint high-activity months and seasons, allowing for better planning and targeted content delivery.
        """)
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
