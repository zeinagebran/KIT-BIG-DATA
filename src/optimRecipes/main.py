"""optimRecipes/main.py file.

main entry for the optimRecipes app.

"""
###############################################################################
# IMPORTS :
# /* Standard includes. */
# /* Extern modules */
import nltk

# /* Intern modules */
from app import WebApp
from config import Config
from functions import prepare_directories
from logger import Logger


###############################################################################
# FUNCTIONS :
def main():
    """Entry point of the module."""
    nltk.download('stopwords')
    cfg = Config()
    prepare_directories(cfg=cfg)
    log_module = Logger(cfg=cfg)
    app = WebApp(log_module=log_module, cfg=cfg)
    app.run()


if __name__ == '__main__':
    main()
