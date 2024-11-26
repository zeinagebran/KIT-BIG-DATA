import pytest
from pathlib import Path
# Assuming the Config class is part of optimRecipes.functions
from optimRecipes.config import Config


@pytest.fixture
def default_config():
    return Config()


def test_config_initialization(default_config):
    """
    Test if the configuration initializes correctly with expected values.
    """
    config = default_config
    config.zip_file_path = 'tests/test.zip'

    assert isinstance(config.zip_file_path, str), "zip_file_path should be a string."
    assert config.zip_file_path.endswith(
        ".zip"), "zip_file_path should point to a .zip file."
    assert Path(config.zip_file_path).exists(), "zip_file_path should exist."

    assert isinstance(config.logging_dir, str), "logging_dir should be a string."
    assert config.logging_dir == "logs", "logging_dir should default to 'logs'."

    assert isinstance(config.run_cfg_dir, str), "run_cfg_dir should be a string."
    assert config.run_cfg_dir == "outputs", "run_cfg_dir should default to 'outputs'."

    assert isinstance(config.min_rating, float), "min_rating should be a float."
    assert config.min_rating == 4.5, "min_rating should be initialized to 4.5."

    assert isinstance(config.min_num_ratings,
                      int), "min_num_ratings should be an integer."
    assert config.min_num_ratings == 0, "min_num_ratings should default to 0."

    assert isinstance(config.num_top_recipes,
                      int), "num_top_recipes should be an integer."
    assert config.num_top_recipes == 20, "num_top_recipes should be initialized to 20."

    assert isinstance(config.min_year, int), "min_year should be an integer."
    assert config.min_year == 1999, "min_year should default to 1999."

    assert isinstance(config.max_year, int), "max_year should be an integer."
    assert config.max_year == 2019, "max_year should default to 2019."


def test_invalid_paths_handling(default_config):
    """
    Test handling of invalid paths.
    """
    config = default_config
    config.zip_file_path = "invalid_path.zip"

    assert not Path(config.zip_file_path).exists(), "Invalid path should not exist."


def test_update_config_attributes(default_config):
    """
    Test updating attributes of the config.
    """
    config = default_config

    # Update min_rating and verify
    config.min_rating = 4.0
    assert config.min_rating == 4.0, "min_rating should update correctly."

    # Update num_top_recipes and verify
    config.num_top_recipes = 50
    assert config.num_top_recipes == 50, "num_top_recipes should update correctly."


def test_logging_dir_creation(default_config, tmpdir):
    """
    Test if the logging directory can be set and exists.
    """
    config = default_config
    config.logging_dir = str(tmpdir / "test_logs")
    Path(config.logging_dir).mkdir(parents=True, exist_ok=True)

    assert Path(config.logging_dir).exists(), "logging_dir should exist after creation."
