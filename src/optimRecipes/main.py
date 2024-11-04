import pyrallis

from functions import prepare_directories

from app import WebApp

from config import Config


@pyrallis.wrap()
def main(cfg: Config):
    prepare_directories(cfg=cfg)
    app = WebApp(cfg=cfg)
    app.run()


if __name__ == '__main__':
    main()
