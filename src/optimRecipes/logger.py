import logging

import yaml


class Logger:
    def __init__(self, cfg):
        self.cfg = cfg
        config_dict = vars(self.cfg)
        self.formatted_config = "\n".join([f"{key}: {value}" for key, value in config_dict.items()])

        self.logger = logging.getLogger('logger')
        if not len(self.logger.handlers):
            self.logger.setLevel(logging.DEBUG)
            # create file handler which logs even debug messages
            fh = logging.FileHandler(self.cfg.logging_dir + '/app.log')
            fh.setLevel(logging.DEBUG)
            # create console handler with a higher log level
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            # create formatter and add it to the handlers
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            ch.setFormatter(formatter)
            fh.setFormatter(formatter)
            # add the handlers to logger
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)

        self.logger.info("-----------------------NEW RUN STARTED-----------------------")
        self.logger.info(f"Configuration \n{self.formatted_config}")
        self.save_config_to_yaml()

    def save_config_to_yaml(self):
        # Convert the class attributes to a dictionary
        config_dict = self.cfg.__dict__
        # Save to a YAML file
        with open(self.cfg.run_cfg_dir + "/config.yml", "w") as file:
            yaml.dump(config_dict, file, default_flow_style=False)

    def log_debug(self, msg: str):
        self.logger.debug(msg)

    def log_info(self, msg: str):
        self.logger.info(msg)

    def log_warning(self, msg: str):
        self.logger.warning(msg)

    def log_critical(self, msg: str):
        self.logger.critical(msg)
