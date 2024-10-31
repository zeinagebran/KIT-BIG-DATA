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

        weekly_analysis = WeeklyAnalysis(self.interactions_df)
        fig = weekly_analysis.plot_mean_interactions()
        st.pyplot(fig)
