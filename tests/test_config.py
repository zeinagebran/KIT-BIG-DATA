import os
import pytest
from pathlib import Path
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


def test_logging_dir_creation(default_config, tmpdir):
    """
    Test if the logging directory can be set and exists.
    """
    config = default_config
    config.logging_dir = str(tmpdir / "test_logs")
    Path(config.logging_dir).mkdir(parents=True, exist_ok=True)

    assert Path(config.logging_dir).exists(), "logging_dir should exist after creation."


def test_prepare_directories():
    from optimRecipes.functions import prepare_directories
    from optimRecipes.config import Config

    cfg = Config()
    cfg.logging_dir = "test_logs"
    cfg.run_cfg_dir = "test_outputs"

    prepare_directories(cfg)

    assert os.path.exists(cfg.logging_dir), "Logging directory should exist."
    assert os.path.exists(cfg.run_cfg_dir), "Run configuration directory should exist."


def test_config_attribute_types():
    """
    Verify that all attributes in the Config class have the correct types.
    """
    config = Config()

    assert isinstance(config.zip_file_path, str), "zip_file_path should be a string."
    assert isinstance(config.logging_dir, str), "logging_dir should be a string."
    assert isinstance(config.run_cfg_dir, str), "run_cfg_dir should be a string."
    assert isinstance(config.min_rating, float), "min_rating should be a float."
    assert isinstance(config.min_num_ratings,
                      int), "min_num_ratings should be an integer."
    assert isinstance(config.num_top_recipes,
                      int), "num_top_recipes should be an integer."
    assert isinstance(config.min_year, int), "min_year should be an integer."
    assert isinstance(config.max_year, int), "max_year should be an integer."
