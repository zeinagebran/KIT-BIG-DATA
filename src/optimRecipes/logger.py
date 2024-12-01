import sys
import pyrallis
from loguru import logger
from config import Config
#from optimRecipes.config import Config



class Logger:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.configure_loguru()
        self.log_config()

    def configure_loguru(self):
        logger.remove()
        format = '<green>{time:YYYY-MM-DD HH:mm:ss}</green> <level>{message}</level>'
        logger.add(sys.stdout, colorize=True, format=format)
        logger.add(self.cfg.logging_dir / 'log.txt',
                   colorize=False, format=format)

    def log_config(self):
        with (self.cfg.run_cfg_dir / 'config.yaml').open('w') as f:
            pyrallis.dump(self.cfg, f)
        self.log_info('\n' + pyrallis.dump(self.cfg))

    @staticmethod
    def log_info(msg: str):
        logger.info(msg)

    @staticmethod
    def log_error(msg: str):
        logger.error(msg)
