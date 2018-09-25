import configparser
from os.path import expanduser


def get_param(path, section, key):
    config = configparser.ConfigParser()
    config.read(expanduser(path))
    value = config.get(section, key)
    return value