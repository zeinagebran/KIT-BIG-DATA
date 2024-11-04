from optimRecipes.config import Config
from app import WebApp
from functions import prepare_directories
import pyrallis
import sys
from pathlib import Path


@pyrallis.wrap()
def main(cfg: Config):
    prepare_directories(cfg=cfg)
    app = WebApp(cfg=cfg)
    app.run()


if __name__ == '__main__':
    main()
