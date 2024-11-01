import pytest
import pandas as pd
from functions import TopRecipesAnalysis  # Importe ta classe

# Créer des DataFrames factices pour les tests
@pytest.fixture
def sample_data():
    recipes_data = pd.DataFrame({
        'recipe_id': [1, 2, 3],
        'name': ['Recipe1', 'Recipe2', 'Recipe3'],
        'submitted': ['2020-01-01', '2019-06-20', '2021-08-15'],
        'minutes': [30, 45, 25],
        'nutrition': ['[300, 20, 15, 10, 5, 50]', '[250, 30, 20, 8, 4, 40]', '[400, 25, 30, 15, 8, 60]']
    })
    
    interactions_data = pd.DataFrame({
        'recipe_id': [1, 1, 2, 3, 3],
        'date': ['2020-02-01', '2020-03-01', '2019-07-01', '2021-09-01', '2021-10-01'],
        'rating': [5, 4, 5, 3, 4],
        'review': ['Great', 'Good', 'Excellent', 'Okay', 'Nice']
    })
    
    return recipes_data, interactions_data

# Initialisation de la classe avec les données de test
@pytest.fixture
def analysis_instance(sample_data):
    recipes_df, interactions_df = sample_data
    return TopRecipesAnalysis(recipes_df, interactions_df)

def test_format_to_datetime(analysis_instance):
    df = analysis_instance._format_to_datetime(analysis_instance.recipes_df, 'submitted')
    assert pd.api.types.is_datetime64_any_dtype(df['submitted']), "La colonne 'submitted' devrait être de type datetime"

def test_rename_column(analysis_instance):
    df = analysis_instance._rename_column(analysis_instance.recipes_df, 'id', 'recipe_id')
    assert 'recipe_id' in df.columns, "La colonne 'id' devrait être renommée en 'recipe_id'"
    assert 'id' not in df.columns, "La colonne 'id' ne devrait plus exister"

def test_merge_with(analysis_instance):
    recipes_df = analysis_instance.recipes_df
    interactions_df = analysis_instance.interactions_df
    merged_df = analysis_instance._merge_with(recipes_df, interactions_df, 'recipe_id')
    assert 'recipe_id' in merged_df.columns, "La colonne 'recipe_id' doit être présente dans le DataFrame fusionné"
    assert merged_df.shape[0] > 0, "Le DataFrame fusionné doit contenir des données"

def test_format_to_numeric(analysis_instance):
    df = analysis_instance._format_to_numeric(analysis_instance.recipes_df, 'minutes')
    assert pd.api.types.is_numeric_dtype(df['minutes']), "La colonne 'minutes' devrait être de type numérique"

def test_filter_positive_ratings(analysis_instance):
    filtered_df = analysis_instance._filter_positive_ratings(analysis_instance.interactions_df, 'rating', threshold=4)
    assert all(filtered_df['rating'] >= 4), "Toutes les notations dans le DataFrame filtré devraient être supérieures ou égales à 4"

def test_get_top_n_recipes_by_ratings(analysis_instance):
    top_recipes = analysis_instance._get_top_n_recipes_by_ratings(
        analysis_instance.interactions_df, 'recipe_id', 'rating', n=2)
    assert len(top_recipes['recipe_id'].unique()) <= 2, "Le nombre de recettes obtenues doit être inférieur ou égal à 'n' spécifié"
    assert 'recipe_id' in top_recipes.columns, "La colonne 'recipe_id' doit être présente dans les recettes obtenues"

def test_group_by_attribute_count(analysis_instance):
    grouped_df = analysis_instance._group_by_attribute_count(
        analysis_instance.interactions_df, ['recipe_id', 'rating'])
    assert 'count' in grouped_df.columns, "La colonne 'count' devrait exister dans le DataFrame regroupé"
    assert grouped_df.shape[0] > 0, "Le DataFrame regroupé ne doit pas être vide"
