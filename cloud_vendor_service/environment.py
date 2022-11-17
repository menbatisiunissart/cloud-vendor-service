
import os
from enum import auto, Flag

class ENV(Flag):
    LOCAL = auto()
    TEST = auto()
    PRODUCTION = auto()

class VENDOR(Flag):
    AWS = auto()
    GOOGLE = auto()

def get_env_var(var_name: str):
    try: 
        env_var = os.environ[var_name]
    except KeyError:
        env_var = ''
    return env_var

def get_env():
    env_var = get_env_var('ENV')
    if env_var == ENV.TEST.name:
        env = ENV.TEST
    elif env_var == ENV.PRODUCTION.name:
        env = ENV.PRODUCTION
    else:
        env = ENV.LOCAL
    return env

def get_vendor():
    env_var = get_env_var('VENDOR')
    if env_var == VENDOR.GOOGLE.name:
        env = VENDOR.GOOGLE
    else:
        env = VENDOR.AWS
    return env