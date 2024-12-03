import pytest
import logging
from src.optimRecipes.functions import prepare_directories
from src.optimRecipes.logger import Logger
from src.optimRecipes.config import Config

def test_logger():
    cfg = Config()
    prepare_directories(cfg=cfg)
    log_module = Logger(cfg=cfg)
    assert isinstance(
        log_module.logger, logging.Logger), "log_module should have a logger object."