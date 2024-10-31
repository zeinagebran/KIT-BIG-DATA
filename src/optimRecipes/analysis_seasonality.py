import streamlit as st
from functions import DataExtractor, SeasonalityAnalysis

from config import Config

class seasonality_analysis_module:
    def __init__(self, interactions_df, cfg: Config):
        self.cfg = cfg
        self.interactions_df = interactions_df

    def run(self):
        st.title("Seasonality Analysis of User Interactions")
        st.markdown("Study user interactions by month and season.")

        seasonality_analysis = SeasonalityAnalysis(self.interactions_df)
        fig = seasonality_analysis.plot_seasonality()
        st.pyplot(fig)
