import os
import yaml


class Config(object):

    config = None

    @staticmethod
    def get(key):
        if Config.config is None:
            config_path = os.path.join(os.path.abspath(os.getcwd()), 'config.yml')
            Config.config = yaml.load(open(config_path))

        return Config.config[key]