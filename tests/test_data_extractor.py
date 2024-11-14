import pytest
import pandas as pd
from optimRecipes.functions import DataExtractor
# Set correct file path
ZIP_FILE_PATH = "test.zip"


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
        'recipe_id': [1, 2, 3],
        'name': ['Recipe 1', 'Recipe 2', 'Recipe 3'],
        'submitted': ['2024-01-01', '2024-01-15', '2024-02-15'],
        'ingredients': ['sugar, flour', 'eggs, milk', 'salt, butter']
    }
    return pd.DataFrame(data)


def test_data_extractor_initialization():
    extractor = DataExtractor(ZIP_FILE_PATH)
    assert extractor.zip_file_path == ZIP_FILE_PATH, "Path should be stored correctly."


def test_data_extractor_load(sample_interactions, sample_recipes, mocker):
    mocker.patch("optimRecipes.functions.pd.read_csv",
                 side_effect=[sample_interactions, sample_recipes])

    extractor = DataExtractor(ZIP_FILE_PATH)
    interactions_df, recipes_df = extractor.extract_and_load_data()
    assert not interactions_df.empty, "Interactions data should load correctly."
    assert not recipes_df.empty, "Recipes data should load correctly."
    assert 'date' in interactions_df.columns, "'date' column should be present in interactions data."
