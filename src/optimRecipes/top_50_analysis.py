import streamlit as st
from functions import get_data, TopRecipesAnalysis


def show_top_50_analysis():
    st.title("Top 50 Most Popular Recipes")
    st.markdown(
        "Identify the recipes that users love the most based on ratings and comments."
    )

    zip_file_path = "C:\\Users\\User\\Desktop\\MASTERE SPECIALISE IA\\KIT BIG DATA BGDIA700\\RESOURCES PROJET\\archive.zip"
    interactions_df, recipes_df = get_data(zip_file_path)

    top_recipes_analysis = TopRecipesAnalysis(recipes_df, interactions_df)

    # Modify the method to only return the top recipes and wordcloud figures
    top_recipes_analysis.display_popular_recipes_and_visualizations()

    # Remove fig and fig_wordcloud unpacking since they're not returned anymore
