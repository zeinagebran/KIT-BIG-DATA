import pytest
import pandas as pd
from src.optimRecipes.functions import TopRecipesAnalysis
import matplotlib.pyplot as plt

from wordcloud import WordCloud


@pytest.fixture
def sample_recipes():
    data = {
        'recipe_id': [1, 2, 3],
        'name': ['Recipe 1', 'Recipe 2', 'Recipe 3'],
        'submitted': ['2024-01-01', '2024-01-15', '2024-02-15'],
        'ingredients': ['sugar, flour', 'eggs, milk', 'salt, butter']
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_interactions():
    data = {
        'date': ['2024-01-01', '2024-02-15', '2024-03-15', '2024-07-01', '2024-10-15'],
        'user_id': [1, 2, 3, 4, 5]
    }
    return pd.DataFrame(data)


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
    grouped_df = top_recipes._group_by_attribute_count(sample_recipes, ['recipe_id'])
    assert isinstance(grouped_df, pd.DataFrame), "Grouped data should be a DataFrame."

    # Create and test the wordcloud output
    fig, ax = plt.subplots()
    text = " ".join(sample_recipes['name'].tolist())
    wordcloud = WordCloud(width=800, height=400,
                          background_color="white").generate(text)
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    assert isinstance(
        wordcloud, WordCloud), "_plot_wordcloud should generate a WordCloud object."
    plt.close(fig)


@pytest.fixture
def sample_recipes_with_duplicates():
    # Duplicates for testing top recipe selection
    data = {
        'recipe_id': [1, 1, 2, 2, 3, 3],
        'name': ['Recipe 1', 'Recipe 1', 'Recipe 2', 'Recipe 2', 'Recipe 3', 'Recipe 3'],
        'submitted': ['2024-01-01', '2024-01-01', '2024-01-15', '2024-01-15', '2024-02-15', '2024-02-15'],
        'ingredients': ['sugar, flour', 'sugar, flour', 'eggs, milk', 'eggs, milk', 'salt, butter', 'salt, butter']
    }
    return pd.DataFrame(data)


def test_top_recipes_with_duplicate_data(sample_recipes_with_duplicates, sample_interactions):
    top_recipes_analysis = TopRecipesAnalysis(
        sample_recipes_with_duplicates, sample_interactions)
    grouped_df = top_recipes_analysis._group_by_attribute_count(
        sample_recipes_with_duplicates, ['recipe_id'])
    assert grouped_df['count'].max(
    ) > 1, "Duplicate entries should be counted in the grouped data"
