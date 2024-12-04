import logging
import os
import pytest
from pathlib import Path

from optimRecipes.functions import prepare_directories
from optimRecipes.logger import Logger
from optimRecipes.config import Config


def test_logger():
    cfg = Config()
    prepare_directories(cfg=cfg)
    log_module = Logger(cfg=cfg)
    assert isinstance(log_module.logger,
                      logging.Logger), "log_module should have a logger object."
    
    assert Path(os.path.join(log_module.cfg.logging_dir, 'app.log')).exists(),"log file should exist."

    log_module.log_critical('Message level crital')
    log_module.log_warning('Message level warning')
    log_module.log_info('Message level info')
    log_module.log_warning('Message level warning')
    log_module.log_debug('Message level debug')
