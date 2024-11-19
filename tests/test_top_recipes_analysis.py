import pytest
import pandas as pd
from optimRecipes.functions import TopRecipesAnalysis


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
    grouped_df = top_recipes._group_by_attribute_count(
        sample_recipes, ['recipe_id'])
    # For coverage; actual output not verified
    top_recipes._plot_wordcloud(grouped_df, sample_recipes)
