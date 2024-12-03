import pytest
import logging
from src.optimRecipes.logger import Logger
from src.optimRecipes.config import Config

def test_logger():
    cfg = Config()
    log_module = Logger(cfg=cfg)
    assert isinstance(
        log_module.logger, logging.Logger), "log_module should have a logger object."