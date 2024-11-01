import streamlit as st
from analysis_weekly import show_weekly_analysis
from analysis_seasonality import show_seasonality_analysis
from top_50_analysis import show_top_50_analysis

# Set page configuration
st.set_page_config(page_title="Enhancing User Interaction",
                   page_icon="📊", layout="centered")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.selectbox("Choose a section:", [
    "Home",
    "Weekly Interaction Analysis",
    "Seasonality Analysis",
    "Top 50 Most Popular Recipes Based on Ratings and Comments"
])

# Home Page
if section == "Home":
    st.title("How to Improve User Interaction in Our Company")
    st.markdown("""
    Welcome to our **home page** dedicated to improving **user interactions**.
    Here are the analysis sections covered:
    """)
    st.markdown("""
    ### Analysis Sections:
    1. **Weekly User Interaction Analysis**: Understand when users are most active.
    2. **Seasonality Analysis**: Analyze user interactions by month and season.
    3. **Top 50 Most Popular Recipes**: Explore the recipes that generate the most interest.
    4. **Characteristics of the Top Recipes**: Analyze features such as preparation time.
    5. **Most Frequent Words in Recipe Titles**: Identify trends in recipe titles.
    """)

# Weekly Interaction Analysis Page
elif section == "Weekly Interaction Analysis":
    show_weekly_analysis()

# Seasonality Analysis Page
elif section == "Seasonality Analysis":
    show_seasonality_analysis()

# Top Recipes Analysis Page
elif section == "Top 50 Most Popular Recipes Based on Ratings and Comments":
    show_top_50_analysis()

# Footer
st.markdown("---\nUse the sidebar to navigate through the analysis.")
