import pytest
import pandas as pd
import matplotlib.pyplot as plt
from unittest import mock
from wordcloud import WordCloud
from functions import DataExtractor, WeeklyAnalysis, SeasonalityAnalysis, TopRecipesAnalysis

# Set correct file path
ZIP_FILE_PATH = "C:\\Users\\User\\Desktop\\MASTERE SPECIALISE IA\\KIT BIG DATA BGDIA700\\RESOURCES PROJET\\archive.zip"

# Sample data for testing


@pytest.fixture
def sample_interactions():
    data = {
        'date': ['2024-01-01', '2024-02-15', '2024-03-15', '2024-07-01', '2024-10-15'],
        'user_id': [1, 2, 3, 4, 5]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_recipes():
    data = {
        'recipe_id': [1, 2, 3],  # Changed 'id' to 'recipe_id'
        'name': ['Recipe 1', 'Recipe 2', 'Recipe 3'],
        'submitted': ['2024-01-01', '2024-01-15', '2024-02-15'],
        'ingredients': ['sugar, flour', 'eggs, milk', 'salt, butter']
    }
    return pd.DataFrame(data)

# Test DataExtractor Class


def test_data_extractor_initialization():
    extractor = DataExtractor(ZIP_FILE_PATH)
    assert extractor.zip_file_path == ZIP_FILE_PATH, "Path should be stored correctly."


def test_data_extractor_load(sample_interactions, sample_recipes, mocker):
    # Mock read_csv to return the sample data for interactions and recipes
    mocker.patch("functions.pd.read_csv", side_effect=[
                 sample_interactions, sample_recipes])

    extractor = DataExtractor(ZIP_FILE_PATH)
    interactions_df, recipes_df = extractor.extract_and_load_data()

    # Assertions to confirm data loading
    assert not interactions_df.empty, "Interactions data should load correctly."
    assert not recipes_df.empty, "Recipes data should load correctly."
    assert 'date' in interactions_df.columns, "'date' column should be present in interactions data."


# Test WeeklyAnalysis Class
def test_weekly_analysis_initialization(sample_interactions):
    weekly_analysis = WeeklyAnalysis(sample_interactions)
    assert 'year' in weekly_analysis.interactions_df.columns, "Year column should be added."
    assert 'day_of_week' in weekly_analysis.interactions_df.columns, "Day of the week column should be added."


def test_weekly_plot_mean_interactions(sample_interactions):
    weekly_analysis = WeeklyAnalysis(sample_interactions)
    fig = weekly_analysis.plot_mean_interactions()
    assert isinstance(
        fig, plt.Figure), "plot_mean_interactions should return a matplotlib Figure."
    plt.close(fig)


def test_weekly_plot_interactions_for_year(sample_interactions):
    weekly_analysis = WeeklyAnalysis(sample_interactions)
    fig = weekly_analysis.plot_interactions_for_year(2024)
    assert isinstance(
        fig, plt.Figure), "plot_interactions_for_year should return a matplotlib Figure."
    plt.close(fig)

# Test SeasonalityAnalysis Class


def test_seasonality_initialization(sample_interactions):
    seasonality_analysis = SeasonalityAnalysis(sample_interactions)
    assert 'season' in seasonality_analysis.interactions_df.columns, "Season column should be added based on months."


def test_seasonality_plot(sample_interactions):
    seasonality_analysis = SeasonalityAnalysis(sample_interactions)
    fig = seasonality_analysis.plot_seasonality()
    assert isinstance(
        fig, plt.Figure), "plot_seasonality should return a matplotlib Figure."
    plt.close(fig)

# Test TopRecipesAnalysis Class


def test_top_recipes_initialization(sample_recipes, sample_interactions):
    top_recipes = TopRecipesAnalysis(sample_recipes, sample_interactions)
    assert isinstance(top_recipes.recipes_df,
                      pd.DataFrame), "Recipes dataframe should be stored."


def test_top_recipes_format_to_datetime(sample_recipes):
    top_recipes = TopRecipesAnalysis(sample_recipes, pd.DataFrame())
    result_df = top_recipes._format_to_datetime(sample_recipes, 'submitted')
    assert pd.api.types.is_datetime64_any_dtype(
        result_df['submitted']), "submitted column should be datetime."


def test_top_recipes_wordcloud(sample_recipes, sample_interactions):
    top_recipes = TopRecipesAnalysis(sample_recipes, sample_interactions)
    grouped_df = top_recipes._group_by_attribute_count(
        sample_recipes, ['recipe_id'])
    # Call for coverage; Streamlit test output not verified
    top_recipes._plot_wordcloud(grouped_df, sample_recipes)
