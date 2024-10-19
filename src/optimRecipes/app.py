import streamlit as st
from analysis_weekly import show_weekly_analysis
from analysis_seasonality import show_seasonality_analysis

# Set page configuration
st.set_page_config(page_title="Enhancing User Interaction",
                   page_icon="📊", layout="centered")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.selectbox("Choose a section:", [
    "Home",
    "Weekly Interaction Analysis",
    "Seasonality Analysis"
])

# Home Page
if section == "Home":
    st.title("How to Improve User Interaction in Our Company")
    st.markdown("""
    Welcome to our **home page** dedicated to improving **user interactions**.

    We will explore different aspects to better understand how our users interact with our platform and identify key areas for enhancing the user experience.

    Here are the analysis sections covered:
    """)
    st.markdown("""
    ### Analysis Sections:
    1. **Section 1: Weekly User Interaction Analysis**
       Understand when users are most active to adjust publication strategies.

    2. **Section 2: Top 50 Most Popular Recipes Based on Ratings and Comments**
       Identify the recipes that generate the most interest based on user ratings and the number of comments.

    3. **Section 3: Characteristics of the Top 50 Most Popular Recipes**
       Analyze features such as preparation time and the number of ingredients for popular recipes to understand user preferences.

    4. **Section 4: Most Frequent Words in Recipe Titles**
       Discover the most common words in recipe titles to identify naming trends that capture user attention.

    5. **Section 5: Seasonality Analysis**
       Analyze the distribution of user interactions by month and season to better understand the most active periods.
    """)

# Weekly Interaction Analysis Page
elif section == "Weekly Interaction Analysis":
    show_weekly_analysis()

# Seasonality Analysis Page
elif section == "Seasonality Analysis":
    show_seasonality_analysis()

# Footer for navigation
st.markdown("""
---
Use the sidebar on the left to explore the different parts of the analysis.
""")
