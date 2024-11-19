import pytest
import pandas as pd
from src.optimRecipes.functions import CommonWordsAnalysis, TopRecipesAnalysis
from wordcloud import WordCloud
import itertools


@pytest.fixture
def sample_recipes():
    data = {
        'id': [1, 2, 3],
        'name': ['Recipe with sugar', 'Egg milk delight', 'Butter salt mix'],
        'submitted': ['2024-01-01', '2024-01-15', '2024-02-15'],
        'ingredients': ['sugar, flour', 'eggs, milk', 'salt, butter'],
        'nutrition': ['[100, 5, 50, 10, 2, 20]', '[200, 10, 40, 15, 3, 30]', '[150, 7, 30, 8, 2, 25]']
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_interactions():
    data = {
        'recipe_id': [1, 2, 3, 1, 2],
        'rating': [5, 4, 3, 5, 4],
        'user_id': [101, 102, 103, 104, 105]
    }
    return pd.DataFrame(data)


@pytest.fixture
def config():
    class Config:
    return Config()


def test_process_name(config, sample_recipes, sample_interactions):
    top_recipes_analysis = TopRecipesAnalysis(sample_recipes, sample_interactions)
    top_recipes = top_recipes_analysis.display_popular_recipes_and_visualizations(return_top_recipes=True, mcw_flag=True)
    analysis = CommonWordsAnalysis(top_recipes, config)
    processed_name = analysis.process_name('Recipe with sugar')
    assert 'with' not in processed_name, "Common stopwords should be removed."


def test_compute_top_keywords(config, sample_recipes, sample_interactions):
    top_recipes_analysis = TopRecipesAnalysis(sample_recipes, sample_interactions)
    top_recipes = top_recipes_analysis.display_popular_recipes_and_visualizations(return_top_recipes=True, mcw_flag=True)
    analysis = CommonWordsAnalysis(top_recipes, config)
    text = analysis.compute_top_keywords()
    wordcloud = analysis.display_wordcloud(text)

    assert isinstance(
        wordcloud, WordCloud), "compute_top_keywords should return a WordCloud object."


#def test_common_words_analysis_edge_case_ratings(config, sample_recipes, sample_interactions):
#    # Test for recipes with ratings at the boundary of min_rating
#    analysis = CommonWordsAnalysis(sample_recipes, sample_interactions, config)
#    analysis.format_recipe(2024)
#    wordcloud = analysis.compute_top_keywords()
#    assert isinstance(
#        wordcloud, WordCloud), "Expected a WordCloud object even with boundary rating recipes"
#
#
#def test_common_words_with_empty_recipe_names(config, sample_interactions):
#    # Recipe name list with empty strings
#    recipes_with_empty_names = pd.DataFrame({
#        'id': [1, 2, 3],
#        'name': ['', 'Recipe without ingredients', ''],
#        'submitted': ['2024-01-01', '2024-01-15', '2024-02-15'],
#        'ingredients': ['', 'eggs, milk', '']
#    })
#    analysis = CommonWordsAnalysis(
#        recipes_with_empty_names, sample_interactions, config)
#    analysis.format_recipe(2024)
#    wordcloud = analysis.compute_top_keywords()
#    assert isinstance(
#        wordcloud, WordCloud), "Expected a WordCloud with empty recipe names"
